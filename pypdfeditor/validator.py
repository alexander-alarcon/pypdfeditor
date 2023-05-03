import mimetypes
import re
from argparse import ArgumentTypeError
from pathlib import Path
from typing import Optional

from type_definitions import Args, Command, SplitArgs


def file_exists(path: str) -> None:
    if not Path(path).exists():
        raise ArgumentTypeError("Error: Source file does not exist.")


def is_valid_pdf(path: str) -> None:
    mime_type: Optional[str]
    _: Optional[str]
    mime_type, _ = mimetypes.guess_type(path)
    if mime_type != "application/pdf":
        raise ArgumentTypeError("Error: Source file is not a PDF file.")


def is_valid_pages(pages: str) -> None:
    # pattern = r"^(?!0)((\d+(-\d+)?)(,(\d+(-\d+)?))*)$"
    # pattern = r"^((((([1-9]\d)*)|[1-9]+)-?)+\,?)+[^,\-]$"
    """
    should select valid page ranges such as:
    - 1-2,5
    - 1,2,5
    - 1-2,5-10
    - 1,2,5-10
    """
    pattern = r"^(((([1-9]\d*)|[1-9]+)-(([1-9]\d*)|[1-9]+))|(([1-9]\d*)|[1-9]+))(,(((([1-9]\d*)|[1-9]+)-(([1-9]\d*)|[1-9]+))|(([1-9]\d*)|[1-9]+))|(([1-9]\d*)|[1-9]+))*$"

    if not re.match(
        pattern,
        pages,
    ):
        raise ArgumentTypeError("Error: Invalid range format.")


def validate_split_args(args: SplitArgs) -> None:
    file_exists(args.source_file)
    is_valid_pdf(args.source_file)
    is_valid_pages(args.pages)


def validate_args(args: Args) -> None:
    match args.command:
        case Command.SPLIT:
            validate_split_args(args=args.options)
