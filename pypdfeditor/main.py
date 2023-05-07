#!/usr/bin/env python3

from argparse import ArgumentError, ArgumentTypeError
from typing import Optional

from read_args import read_args
from type_definitions import Args, MergeArgs, SplitArgs

from pypdfeditor.commands import CliCommand, MergeCommand, SplitCommand
from pypdfeditor.validator import validate_args


def main() -> None:
    try:
        args: Args = read_args()
        validate_args(args=args)

        command: Optional[CliCommand] = None

        if isinstance(args.options, SplitArgs):
            command = SplitCommand(options=args.options)
        elif isinstance(args.options, MergeArgs):
            command = MergeCommand(options=args.options)
        else:
            raise ValueError(f"Invalid command {args.command}")

        if command is not None:
            command.execute()

    except (ArgumentTypeError, ArgumentError, ValueError) as e:
        print(str(e))


if __name__ == "__main__":
    main()
