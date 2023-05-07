from dataclasses import dataclass
from typing import Generic

from pypdfeditor.editor import split_pdf
from pypdfeditor.type_definitions import MergeArgs, SplitArgs, T


@dataclass
class CliCommand(Generic[T]):
    options: T

    def execute(self) -> None:
        pass


@dataclass
class SplitCommand(CliCommand[SplitArgs]):
    options: SplitArgs

    def execute(self) -> None:
        split_pdf(
            source_file=self.options.source_file,
            page_range=self.options.pages,
            mode=self.options.mode,
        )


@dataclass
class MergeCommand(CliCommand[MergeArgs]):
    options: MergeArgs

    def execute(self) -> None:
        print(self)
        pass
