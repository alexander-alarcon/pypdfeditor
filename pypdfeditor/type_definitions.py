from enum import StrEnum
from typing import NamedTuple


class Command(StrEnum):
    SPLIT = "split"


class SplitMode(StrEnum):
    SINGLE_FILE = "single_file"
    RANGE_FILES = "range_files"
    MULTI_FILES = "multi_files"


class SplitArgs(NamedTuple):
    source_file: str
    pages: str
    mode: SplitMode = SplitMode.SINGLE_FILE


class Args(NamedTuple):
    command: Command
    options: SplitArgs
