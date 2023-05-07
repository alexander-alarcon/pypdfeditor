from functools import partial
from pathlib import Path
from typing import Callable

from PyPDF2 import PdfReader, PdfWriter
from type_definitions import SplitMode

from .parser import parse_page_range, parse_page_ranges


def print_result(pages: int) -> None:
    if pages == 1:
        print(f"The PDF file was successfully split into {pages} file")
    else:
        print(f"The PDF file was successfully split into {pages} files")


def split_pdf_file_by_pages(
    reader: PdfReader,
    filename: str,
    page_range: set[int],
) -> None:
    if max(page_range) > len(reader.pages):
        raise ValueError(
            "Error: The specified page range exceeds the number of pages in the PDF file."
        )

    for i, page in enumerate(page_range):
        output_filename: str = f"{filename}_{i+1}.pdf"
        with open(output_filename, "wb") as out_file:
            writer = PdfWriter()
            writer.add_page(reader.pages[page - 1])
            writer.write(out_file)

    print_result(len(page_range))


def split_pdf_file_by_ranges(
    reader: PdfReader,
    filename: str,
    page_ranges: list[set[int]],
) -> None:
    pages: list[int] = sorted(set.union(*page_ranges))
    if max(pages) > len(reader.pages):
        raise ValueError(
            "Error: The specified page range exceeds the number of pages in the PDF file."
        )

    for i, page_range in enumerate(page_ranges):
        output_filename: str = f"{filename}_{i+1}.pdf"
        with open(output_filename, "wb") as out_file:
            writer = PdfWriter()
            for page in sorted(page_range):
                writer.add_page(reader.pages[page - 1])
            writer.write(out_file)

    print_result(len(page_ranges))


def split_pdf_file(
    reader: PdfReader,
    filename: str,
    page_range: set[int],
) -> None:
    if max(page_range) > len(reader.pages):
        raise ValueError(
            "Error: The specified page range exceeds the number of pages in the PDF file."
        )

    with open(f"{filename}_split.pdf", "wb") as out_file:
        writer = PdfWriter()
        for page in page_range:
            writer.add_page(reader.pages[page - 1])
        writer.write(out_file)
    print_result(1)


def split_pdf(
    source_file: str,
    page_range: str,
    mode: SplitMode = SplitMode.SINGLE_FILE,
) -> None:
    reader: PdfReader = PdfReader(source_file)

    filename: str = Path(source_file).stem

    split_func: Callable[[PdfReader, str, set[int]], None] | Callable[
        [PdfReader, str, list[set[int]]], None
    ] | None = None

    match mode:
        case SplitMode.SINGLE_FILE:
            split_func = partial(
                split_pdf_file,
                page_range=parse_page_range(page_range),
            )
        case SplitMode.RANGE_FILES:
            split_func = partial(
                split_pdf_file_by_ranges,
                page_ranges=parse_page_ranges(page_range),
            )
        case SplitMode.MULTI_FILES:
            split_func = partial(
                split_pdf_file_by_pages,
                page_range=parse_page_range(page_range),
            )
        case _:
            raise ValueError(f"Error: Unsupported split mode: {mode}")

    split_func(reader=reader, filename=filename)
