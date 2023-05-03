from enum import StrEnum
from typing import NamedTuple


class Command(StrEnum):
    SPLIT = "split"


class SplitArgs(NamedTuple):
    source_file: str
    pages: str


class Args(NamedTuple):
    command: Command
    options: SplitArgs
