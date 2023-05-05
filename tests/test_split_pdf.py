import pytest
from mock import patch

from pypdfeditor.editor import split_pdf


class TestSplitPdf:
    @patch("PyPDF2.PdfReader")
    @pytest.mark.parametrize(
        "page_range",
        [{10}, {1, 3, 5, 6, 10}, {50, 51, 1}],
    )
    def test_split_pdf_with_wrong_args(self, _, page_range: set[int]) -> None:
        print(page_range)
        with pytest.raises(ValueError):
            split_pdf(source_file="doc.pdf", page_range=page_range)
