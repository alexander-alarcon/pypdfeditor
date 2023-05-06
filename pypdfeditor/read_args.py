from argparse import (
    ArgumentError,
    ArgumentParser,
    Namespace,
    RawTextHelpFormatter,
    _SubParsersAction,
)

from type_definitions import Args, Command, SplitArgs, SplitMode


def read_args() -> Args:
    parser = ArgumentParser(description="Python PDF editor")
    subparser: _SubParsersAction = parser.add_subparsers(
        dest="command",
        required=True,
    )

    split_parser: ArgumentParser = subparser.add_parser(
        Command.SPLIT,
        help="Split a PDF file into multiple files based on page ranges.",
        formatter_class=RawTextHelpFormatter,
    )
    split_parser.add_argument("source_file", help="Path to the source PDF file")
    split_parser.add_argument(
        "-p",
        "--pages",
        help="Specify page ranges to split on (e.g. '1-5,8-10')",
        required=True,
        metavar="",
    )
    split_parser.add_argument(
        "-m",
        "--mode",
        help=f"""The splitting mode to use. Valid choices are: {', '.join(mode.value for mode in SplitMode)}.
    Defaults to {SplitMode.SINGLE_FILE}.

    Available modes:
    - single_file: Saves the selected pages in a single PDF file.
    - range_files: Splits the PDF into multiple files based on page ranges.
    - multi_files: Splits the PDF into multiple files, one page per file.""",
        choices=list(SplitMode),
        default=SplitMode.SINGLE_FILE,
        type=SplitMode,
        metavar="",
    )

    args: Namespace = parser.parse_args()

    match args.command:
        case Command.SPLIT:
            return Args(
                command=args.command,
                options=SplitArgs(
                    source_file=args.source_file,
                    pages=args.pages,
                    mode=args.mode,
                ),
            )
        case _:
            raise ArgumentError(None, "Error: Invalid command")
