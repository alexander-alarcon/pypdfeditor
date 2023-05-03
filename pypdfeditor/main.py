#!/usr/bin/env python3

from argparse import ArgumentError, ArgumentTypeError

from read_args import read_args
from type_definitions import Args


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
