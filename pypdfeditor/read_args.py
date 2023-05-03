from argparse import ArgumentError, ArgumentParser, Namespace, _SubParsersAction

from type_definitions import Args, Command, SplitArgs


def read_args() -> Args:
    parser = ArgumentParser(description="Python PDF editor")
    subparser: _SubParsersAction = parser.add_subparsers(
        dest="command",
        required=True,
    )

    split_parser: ArgumentParser = subparser.add_parser(
        Command.SPLIT, help="Split a PDF file into multiple files based on page ranges."
    )
    split_parser.add_argument("source_file", help="Path to the source PDF file")
    split_parser.add_argument(
        "-p",
        "--pages",
        help="Specify page ranges to split on (e.g. '1-5,8-10')",
        required=True,
    )

    args: Namespace = parser.parse_args()

    match args.command:
        case Command.SPLIT:
            return Args(
                command=args.command,
                options=SplitArgs(
                    source_file=args.source_file,
                    pages=args.pages,
                ),
            )
        case _:
            raise ArgumentError(None, "Error: Invalid command")
