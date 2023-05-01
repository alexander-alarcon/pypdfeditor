#!/usr/bin/env python3

import argparse

from typing import NamedTuple
from enum import StrEnum


class Command(StrEnum):
    SPLIT = "split"


class SplitArgs(NamedTuple):
    source_file: str
    pages: str


class Args(NamedTuple):
    command: Command
    options: SplitArgs


def read_args() -> Args:
    parser = argparse.ArgumentParser(description="Python PDF editor")
    subparser: argparse._SubParsersAction = parser.add_subparsers(
        dest="command",
        required=True,
    )

    split_parser: argparse.ArgumentParser = subparser.add_parser(
        Command.SPLIT, help="Split a PDF file into multiple files based on page ranges."
    )
    split_parser.add_argument("source_file", help="Path to the source PDF file")
    split_parser.add_argument(
        "-p",
        "--pages",
        help="Specify page ranges to split on (e.g. '1-5,8-10')",
        required=True,
    )

    args: argparse.Namespace = parser.parse_args()

    if args.command == Command.SPLIT:
        return Args(
            command=args.command,
            options=SplitArgs(
                source_file=args.source_file,
                pages=args.pages,
            ),
        )
    else:
        raise argparse.ArgumentError(None, "Error: Invalid command")


def main() -> None:
    try:
        args: Args = read_args()
        match args.command:
            case Command.SPLIT:
                print("Split command was selected")

    except argparse.ArgumentError as e:
        print(str(e))


if __name__ == "__main__":
    main()
