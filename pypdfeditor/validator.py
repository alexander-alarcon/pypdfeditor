import mimetypes
import re
from argparse import ArgumentTypeError
from pathlib import Path
from typing import Optional

from type_definitions import Args, Command, MergeArgs, SplitArgs


def file_exists(path: str, error_message: str) -> None:
    if not Path(path).exists():
        raise ArgumentTypeError(error_message)


def is_valid_pdf(path: str) -> None:
    mime_type: Optional[str]
    _: Optional[str]
    mime_type, _ = mimetypes.guess_type(path)
    if mime_type != "application/pdf":
        raise ArgumentTypeError("Error: Source file is not a PDF file.")


def is_valid_pdf_name(name: str, error_message: str) -> None:
    pattern = r"^[\w\s-]+\.pdf$"
    if not re.match(pattern, name):
        raise ValueError(error_message)


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
    file_exists(args.source_file, "Error: Source file does not exist.")
    is_valid_pdf(args.source_file)
    is_valid_pages(args.pages)


def validate_output_file(output_file: str) -> None:
    is_valid_pdf_name(output_file, "Error: Invalid Output file name.")


def validate_input_files(input_files: list[str]) -> None:
    if len(input_files) < 2:
        raise ValueError("Error: At least 2 input files are required for merging.")

    for file in input_files:
        if ":" in file:
            filename: str
            page_range: str | None = None
            filename, page_range = file.split(":")
            input_file_error_message: str = (
                f"Error: Input file <{filename}>does not exist"
            )
            file_exists(filename, input_file_error_message)
            is_valid_pages(page_range)
        else:
            input_file_error_message: str = f"Error: Input file <{file}> does not exist"
            file_exists(file, input_file_error_message)


def validate_merge_args(args: MergeArgs) -> None:
    validate_output_file(args.output_file)
    validate_input_files(args.input_files)


def validate_args(args: Args) -> None:
    match args.command:
        case Command.SPLIT:
            validate_split_args(args=args.options)
        case Command.MERGE:
            validate_merge_args(args=args.options)
