#!/usr/bin/env python
import click

from pathlib import Path
from io import TextIOWrapper
from .handlers import encode as encode_handler, decode as decode_handler


@click.command(name="Encode", help="Encodes text message into image")
@click.argument("input-file", type=click.File("r"))
@click.argument("input-image", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
def encode(input_file: TextIOWrapper, input_image: str, output: str):
    encode_handler(input_file, Path(input_image), Path(output))


@click.command(name="Encode", help="Decode image into text file")
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
def decode(input, output):
    decode_handler(Path(input), Path(output))


@click.group(commands={"encode": encode, "decode": decode})
def cli():
    pass


if __name__ == "__main__":
    cli()
