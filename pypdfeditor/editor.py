from pathlib import Path

from PyPDF2 import PdfReader, PdfWriter


def print_result(pages: int) -> None:
    if pages == 1:
        print(f"The PDF file was successfully split into {pages} file")
    else:
        print(f"The PDF file was successfully split into {pages} files")


def split_pdf(source_file: str, page_range: set[int]) -> None:
    reader: PdfReader = PdfReader(source_file)

    if max(page_range) > len(reader.pages):
        raise ValueError(
            "Error: The specified page range exceeds the number of pages in the PDF file."
        )

    filename: str = Path(source_file).stem
    for i, page in enumerate(page_range):
        output_filename: str = f"{filename}_{i+1}.pdf"
        with open(output_filename, "wb") as out_file:
            writer = PdfWriter()
            writer.add_page(reader.pages[page - 1])
            writer.write(out_file)

    print_result(len(page_range))
