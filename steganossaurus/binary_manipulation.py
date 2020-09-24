import numpy as np

from typing import Union, List


def substitute_lsb(origin: int, new: str) -> int:
    """Receives an origin number and replace the LSB (least significant bits)
    with the new string, converts back to integer and returns it.

    Args:
        origin (int): origin number
        new (str): bits that will be inserted into the origin number LSB's

    Raises:
        Raises ValueError if the length of new exceeds the maximum value for
        origin. e.g `substitute_lsb(4, '111111')`

        Raises TypeError if origin is not a number

    Returns:
        [int] operated number

    Example: `substitute_lsb(240, '0101')` returns `245`
    """
    binary_origin = bin(origin)
    binary_origin = binary_origin[2:]

    try:
        int(new, base=2)
    except TypeError:
        raise ValueError(
            "New value must be a string with a binary encoded number value."
        )

    if len(binary_origin) < len(new):
        raise ValueError(
            "New value is too big to be encoded inside origin value."
        )
    else:
        new_binary = binary_origin[: -len(new)] + new
        return int(new_binary, base=2)
      
      
def extract_lsb(origin: int, count: int) -> str:
    """Receives an integer number, converts it to it's binary representation (on string)
    and returns a string representation of the N least significant bits, with N equals to [count]

    Args:
        origin (int): integer number from which the LSB's will be extracted
        count (int): numbers of bits that shall be returned

    Returns:
        str: String binary representation of the N LSB's

    Example: extract_lsb(10, 2) returns '10'.

    First the function converts 10 to '1010' then returns the N last characters from the representation
    """
    if origin == 0:
        return "00"
    if origin == 1:
        return "01"
    binary_origin = bin(origin)
    binary_origin = binary_origin[-count:]

    return binary_origin


def message_to_binary(message: Union[str, bytes, int]) -> Union[str, List[str]]:
    """Converts the received message into an binary presentation

    Args:
        message (`Union[str, bytes, int]`): Message that shall be encoded

    Raises:
        TypeError: if message is not a supported type

    Returns:
        [Union[str, List[str]]]: Binary representation of the received message
    """
    if type(message) == str:
        return "".join([format(ord(i), "08b") for i in message])
    elif type(message) == bytes or type(message) == np.ndarray:
        return [format(i, "08b") for i in message]
    elif type(message) == int or type(message) == np.uint8:
        return format(message, "08b")
    else:
        raise TypeError("Input type not supported")
