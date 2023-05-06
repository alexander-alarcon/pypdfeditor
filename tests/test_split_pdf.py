import logging

import pytest
from mock import patch

from pypdfeditor.type_definitions import SplitMode

LOGGER = logging.getLogger(__name__)

from pypdfeditor.editor import split_pdf


class TestSplitPdf:
    @patch("PyPDF2.PdfReader")
    @pytest.mark.parametrize(
        "page_range",
        ["10", "1-3,5,6,10", "50,51,1"],
    )
    def test_split_pdf_with_wrong_page_ranges(self, _, page_range: str) -> None:
        with pytest.raises(ValueError) as e:
            split_pdf(source_file="doc.pdf", page_range=page_range)
        assert (
            str(e.value)
            == "Error: The specified page range exceeds the number of pages in the PDF file."
        )

    @patch("PyPDF2.PdfReader")
    @pytest.mark.parametrize(
        "page_range, mode",
        [
            ("2-4", "split_unknown"),
            ("1-4", "whatever"),
            ("1,3-4", "lorem"),
            ("5", "unknown"),
        ],
    )
    def test_split_pdf_with_wrong_mode(
        self, _, page_range: str, mode: SplitMode
    ) -> None:
        with pytest.raises(ValueError) as e:
            split_pdf(source_file="doc.pdf", page_range=page_range, mode=mode)
        assert str(e.value) == f"Error: Unsupported split mode: {mode}"
