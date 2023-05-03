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
