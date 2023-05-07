from dataclasses import dataclass
from typing import Generic

from pypdfeditor.editor import merge_pdf, split_pdf
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
        merge_pdf(
            output_file=self.options.output_file,
            input_files=self.options.input_files,
        )
