import math
import numpy as np

from io import TextIOWrapper, FileIO
from pathlib import Path
from imageio import imread, imwrite
from typing import List

from .binary_manipulation import substitute_lsb, extract_lsb, message_to_binary
from .utils import image_needed_size


def encode(
    input_message: TextIOWrapper,
    input_image: Path,
    output_path: Path,
    delimiter: str,
) -> None:
    """Encode a text file using LSB image steganography inside a provided image, storing
    the final image on the [output_path]

    Args:
        input_message (TextIOWrapper): [description]
        input_image (Path): [description]
        output_path (Path): [description]
        delimiter (str): [description]

    Raises:
        ValueError: if the message size is larger than the length of the provided image
    """
    message: str = input_message.read() + delimiter
    message: str = message_to_binary(message)
    message: List[str] = list(message)
    image = imread(input_image)

    max_possible_encoded_bits = len(image) * len(image[0]) * 3

    if len(message) > max_possible_encoded_bits:
        raise ValueError(
            "Message is too long for encoding in the provided image. Provide a larger image or a shorter message"
        )

    red, blue, green = 0, 1, 2
    data_index: int = 0

    for values in image:
        for pixels in values:
            if data_index < len(message):
                pixels[red] = substitute_lsb(pixels[red], message[data_index])
                data_index += 1
            if data_index < len(message):
                pixels[green] = substitute_lsb(pixels[green], message[data_index])
                data_index += 1
            if data_index < len(message):
                pixels[blue] = substitute_lsb(pixels[blue], message[data_index])
                data_index += 1
            if data_index >= len(message):
                break

    imwrite(output_path, image)
    print(f"Output image saved in {output_path}")


def decode(input_image: Path, output_message: Path, delimiter: str = "#####") -> None:
    """Decodes a previously encoded message in an provided image, searching for
    the [delimiter] at the message end.

    Args:
        input_image (Path): Path to source image
        output_message (Path): Path where the output message will be written
        delimiter (str): End of message delimiter.
    """
    image = imread(input_image)
    binary_data = ""
    red, blue, green = 0, 1, 2

    for values in image:
        for pixels in values:
            binary_data += extract_lsb(pixels[red], 1)
            binary_data += extract_lsb(pixels[green], 1)
            binary_data += extract_lsb(pixels[blue], 1)

    byte_data = [binary_data[i : i + 8] for i in range(0, len(binary_data), 8)]

    decoded_data = ""
    delimiter_found: bool = False

    for byte in byte_data:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-len(delimiter) :] == delimiter:
            delimiter_found = True
            break

    with open(output_message, "w") as fp:
        fp.write(decoded_data[: -len(delimiter)])

    if delimiter_found:
        print(f"Output text saved in {output_message}")
    else:
        print(
            f"Output text saved in {output_message}, but message delimiter could not been found, results may be a little odd."
        )
