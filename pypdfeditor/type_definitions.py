from enum import StrEnum
from typing import Generic, NamedTuple, TypeVar


class Command(StrEnum):
    SPLIT = "split"
    MERGE = "merge"


class SplitMode(StrEnum):
    SINGLE_FILE = "single_file"
    RANGE_FILES = "range_files"
    MULTI_FILES = "multi_files"


class SplitArgs(NamedTuple):
    source_file: str
    pages: str
    mode: SplitMode = SplitMode.SINGLE_FILE


class MergeArgs(NamedTuple):
    output_file: str
    input_files: list[str]


T = TypeVar("T", SplitArgs, MergeArgs)


class Args(NamedTuple, Generic[T]):
    command: Command
    options: T
