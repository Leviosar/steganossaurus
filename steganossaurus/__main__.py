#!/usr/bin/env python
import click

from pathlib import Path
from io import TextIOWrapper
from .handlers import encode as encode_handler, decode as decode_handler


@click.command(name="Encode", help="Encodes text message into image")
@click.argument("input-file", type=click.File("r"))
@click.argument("input-image", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
@click.option("--delimiter", default="#####", help="Delimiter used for message trailer")
def encode(input_file: TextIOWrapper, input_image: str, output: str, delimiter: str):
    encode_handler(input_file, Path(input_image), Path(output), delimiter)


@click.command(name="Decode", help="Decode image into text file")
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
@click.option("--delimiter", default="#####", help="Delimiter used for message trailer")
def decode(input: str, output: str, delimiter: str):
    decode_handler(Path(input), Path(output), delimiter)


@click.group(commands={"encode": encode, "decode": decode})
def cli():
    pass


if __name__ == "__main__":
    cli()
