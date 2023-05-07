from argparse import ArgumentTypeError
from pathlib import Path
from typing import Literal

import pytest
from pytest import MonkeyPatch

from pypdfeditor.type_definitions import SplitArgs
from pypdfeditor.validator import (
    validate_input_files,
    validate_output_file,
    validate_split_args,
)


class TestValidateSplitArgs:
    @pytest.mark.parametrize(
        "file",
        [
            "document1.pdf",
            "report.pdf",
            "ebook.pdf",
            "article.pdf",
            "manual.pdf",
            "guide.pdf",
            "brochure.pdf",
            "for.pdf",
            "catalog.pdf",
            "newsletter.pdf",
        ],
    )
    def test_validate_split_args_with_existing_pdf(
        self, monkeypatch: MonkeyPatch, file: str
    ) -> None:
        """
        Test case: `validate_split_args` does not raise an exception when provided with valid input.
        """

        def mock_exists(path) -> Literal[True]:
            return True

        monkeypatch.setattr(Path, "exists", mock_exists)
        args = SplitArgs(source_file=file, pages="1-3")
        assert validate_split_args(args) is None

    @pytest.mark.parametrize(
        "missing_file",
        [
            "missing_document1.pdf",
            "missing_report.pdf",
            "missing_ebook.pdf",
            "missing_article.pdf",
            "missing_manual.pdf",
            "missing_guide.pdf",
            "missing_brochure.pdf",
            "missing_forpdf",
            "missing_catalog.pdf",
            "missing_newsletter.pdf",
        ],
    )
    def test_validate_split_args_with_non_existing_pdf(
        self, monkeypatch: MonkeyPatch, missing_file: str
    ) -> None:
        """
        Test case: `validate_split_args` raise an exception when provided with invalid source file input.
        """

        def mock_exists(path) -> Literal[False]:
            return False

        monkeypatch.setattr(Path, "exists", mock_exists)
        args = SplitArgs(source_file=missing_file, pages="1-3")
        with pytest.raises(ArgumentTypeError) as e:
            validate_split_args(args)
        assert str(e.value) == "Error: Source file does not exist."

    @pytest.mark.parametrize(
        "file",
        [
            "missing.txt",
            "missing.png",
            "missing.jpg" "missing.html",
            "report.docx",
            "image.jpeg",
            "presentation.ppt",
            "audio.mp3",
            "video.mp4",
            "spreadsheet.xlsx",
            "text.txt",
            "code.py",
            "archive.zip",
            "executable.exe",
        ],
    )
    def test_validate_split_args_with_non_pdf_files(
        self, monkeypatch: MonkeyPatch, file: str
    ) -> None:
        """
        Test case: `validate_split_args` raise an exception when provided non pdf file input.
        """

        def mock_exists(path) -> Literal[True]:
            return True

        monkeypatch.setattr(Path, "exists", mock_exists)
        args = SplitArgs(source_file=file, pages="1-3")
        with pytest.raises(ArgumentTypeError) as e:
            validate_split_args(args)
        assert str(e.value) == "Error: Source file is not a PDF file."

    @pytest.mark.parametrize(
        "file, pages",
        [
            (
                "my_file.pdf",
                "1-10",
            ),
            (
                "my_file.pdf",
                "2-4,7,9-12",
            ),
            (
                "my_file.pdf",
                "1,4-7,10",
            ),
            (
                "my_file.pdf",
                "3-3",
            ),
            (
                "my_file.pdf",
                "1-1000,1001-2000,2001-2500",
            ),
            (
                "my_file.pdf",
                "1,3-5,7,10-12",
            ),
            (
                "my_file.pdf",
                "1-3,3-5,6-8",
            ),
            (
                "my_file.pdf",
                "1-2,2-2,2-3,3-3",
            ),
            (
                "my_file.pdf",
                "1-10,20,30-40,50-60,70,80-90,100",
            ),
        ],
    )
    def test_validate_split_args_with_valid_pages(
        self, monkeypatch: MonkeyPatch, file: str, pages: str
    ) -> None:
        """
        Test case: `validate_split_args` does not raise an exception when provided with valid pages input.
        """

        def mock_exists(path) -> Literal[True]:
            return True

        monkeypatch.setattr(Path, "exists", mock_exists)
        args = SplitArgs(source_file=file, pages=pages)
        assert validate_split_args(args) is None

    @pytest.mark.parametrize(
        "file, pages",
        [
            (
                "my_file.pdf",
                "1,2,3-",
            ),
            (
                "my_file.pdf",
                "-4,6,7",
            ),
            (
                "my_file.pdf",
                "1-5-7",
            ),
            (
                "my_file.pdf",
                "0",
            ),
            (
                "my_file.pdf",
                "1--5",
            ),
            (
                "my_file.pdf",
                "1-5-8,9-12",
            ),
            (
                "my_file.pdf",
                "1-5,0",
            ),
            (
                "my_file.pdf",
                "1-2,2-1,0",
            ),
            (
                "my_file.pdf",
                "1-3,3-5,",
            ),
        ],
    )
    def test_validate_split_args_with_invalid_pages(
        self, monkeypatch: MonkeyPatch, file: str, pages: str
    ) -> None:
        """
        Test case: `validate_split_args` does not raise an exception when provided with valid pages input.
        """

        def mock_exists(path) -> Literal[True]:
            return True

        monkeypatch.setattr(Path, "exists", mock_exists)
        args = SplitArgs(source_file=file, pages=pages)

        with pytest.raises(ArgumentTypeError) as e:
            validate_split_args(args)
        assert str(e.value) == "Error: Invalid range format."


class TestValidateMergeArgs:
    @pytest.mark.parametrize(
        "filename",
        [
            "document1.pdf",
            "report.pdf",
            "ebook.pdf",
            "article.pdf",
            "manual.pdf",
            "guide.pdf",
            "brochure.pdf",
            "document_2.pdf",
            "file with spaces.pdf",
            "my-file.pdf",
        ],
    )
    def test_validate_merge_args_output_file_valid(
        self,
        filename: str,
    ) -> None:
        """
        Test case: `validate_output_file` does not raise an exception when provided with valid input.
        """
        assert validate_output_file(filename) is None

    @pytest.mark.parametrize(
        "filename",
        [
            "document1",  # Missing ".pdf" extension
            "report.pdf.txt",  # Incorrect file extension
            "ebook",  # Missing ".pdf" extension
            "article.pdf.docx",  # Incorrect file extension
            "manual.pdf ",  # Trailing whitespace
            "guide*.pdf",  # Invalid characters (asterisk)
            "brochure/",  # Invalid character (slash)
            "document 2.png",  # Invalid extension
            "my file.jpg",  # Invalid extension
            "file?name.pdf",  # Invalid character (question mark)
        ],
    )
    def test_validate_merge_args_output_file_invalid(
        self,
        filename: str,
    ) -> None:
        """
        Test case: `validate_output_file` raise an exception when provided with invalid pdf file name.
        """
        with pytest.raises(ValueError) as e:
            validate_output_file(filename)
        assert str(e.value) == "Error: Invalid Output file name."

    @pytest.mark.parametrize("input_files", [["file.pdf"], []])
    def test_validate_merge_args_input_files_not_enough(
        self,
        input_files: list[str],
    ) -> None:
        """
        Test case: `validate_input_files` raises an exception when fewer than two input files are provided.
        """
        with pytest.raises(ValueError) as e:
            validate_input_files(input_files=input_files)
        assert str(e.value) == "Error: At least 2 input files are required for merging."

    @pytest.mark.parametrize(
        "input_files",
        [
            ["doc1.pdf", "doc2.pdf"],
            ["report1.pdf", "report2.pdf", "report3.pdf"],
            ["doc1.pdf:1-15", "doc2.pdf:1-3,5"],
            ["report1.pdf:1-5", "report2.pdf", "report3.pdf"],
        ],
    )
    def test_validate_merge_args_input_files_enough(
        self,
        monkeypatch: MonkeyPatch,
        input_files: list[str],
    ) -> None:
        """
        Test case: `validate_input_files` does not raise an exception when provided enough files.
        """

        def mock_exists(path) -> Literal[True]:
            return True

        monkeypatch.setattr(Path, "exists", mock_exists)

        assert validate_input_files(input_files=input_files) is None
