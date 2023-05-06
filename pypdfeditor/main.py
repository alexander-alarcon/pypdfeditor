#!/usr/bin/env python3

from argparse import ArgumentError, ArgumentTypeError

from read_args import read_args
from type_definitions import Args, Command, SplitMode

from pypdfeditor.editor import split_pdf
from pypdfeditor.validator import validate_args


def main() -> None:
    try:
        args: Args = read_args()
        validate_args(args=args)
        match args.command:
            case Command.SPLIT:
                split_pdf(
                    source_file=args.options.source_file,
                    page_range=args.options.pages,
                    mode=args.options.mode,
                )
            case _:
                raise ValueError(f"Invalid command {args.command}")
    except (ArgumentTypeError, ArgumentError, ValueError) as e:
        print(str(e))


if __name__ == "__main__":
    main()
