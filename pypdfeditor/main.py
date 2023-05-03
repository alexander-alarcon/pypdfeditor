#!/usr/bin/env python3

from argparse import ArgumentError, ArgumentTypeError

from read_args import read_args
from type_definitions import Args

from pypdfeditor.validator import validate_args


def main() -> None:
    try:
        args: Args = read_args()
        validate_args(args=args)
    except (ArgumentTypeError, ArgumentError) as e:
        print(str(e))


if __name__ == "__main__":
    main()
