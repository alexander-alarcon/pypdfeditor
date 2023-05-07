from argparse import (
    ArgumentError,
    ArgumentParser,
    Namespace,
    RawTextHelpFormatter,
    _SubParsersAction,
)

from type_definitions import Args, Command, MergeArgs, SplitArgs, SplitMode


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

    merge_parser: ArgumentParser = subparser.add_parser(
        Command.MERGE,
        help="Merge multiple PDF files into one PDF file",
        formatter_class=RawTextHelpFormatter,
    )
    merge_parser.add_argument(
        "-o",
        "--output-file",
        help="Specify the name of the resulting merged PDF file",
        required=True,
        metavar="FILE",
    )
    merge_parser.add_argument(
        "-i",
        "--input-files",
        help="""Specify two or more input PDF files to merge into a single PDF file. At least 2 input files are required.

    Available formats:
    - filename: Path to an existing PDF file.
    - filename:page_range: Path to an existing PDF file and a page range to merge from that file.

    Example usage:
    - file1.pdf
    - file2.pdf:1-3
    - file3.pdf:4,6-8
        """,
        required=True,
        action="append",
        metavar="FILE",
    )

    args: Namespace = parser.parse_args()

    match args.command:
        case Command.SPLIT:
            return Args[SplitArgs](
                command=args.command,
                options=SplitArgs(
                    source_file=args.source_file,
                    pages=args.pages,
                    mode=args.mode,
                ),
            )
        case Command.MERGE:
            return Args[MergeArgs](
                command=args.command,
                options=MergeArgs(
                    input_files=args.input_files,
                    output_file=args.output_file,
                ),
            )
        case _:
            raise ArgumentError(None, "Error: Invalid command")
