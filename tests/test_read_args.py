import pytest
from pytest import MonkeyPatch

from pypdfeditor.read_args import read_args
from pypdfeditor.type_definitions import Args, Command, MergeArgs, SplitArgs


class TestReadArgs:
    @pytest.mark.parametrize(
        "invalid_command",
        [
            "lorem",
            "quotes",
            "ipsum",
            "dolor",
            "sit",
            "sitet",
        ],
    )
    def test_read_args_wrong_command(
        self, monkeypatch: MonkeyPatch, invalid_command: str
    ) -> None:
        """
        Test case: should raise exception when invalid command is provided
        """
        monkeypatch.setattr(
            "sys.argv",
            ["pypdfeditor", invalid_command],
        )
        with pytest.raises(SystemExit):
            read_args()

    def test_read_args_split_without_arguments(self, monkeypatch: MonkeyPatch) -> None:
        """
        Test case: should raise exception when split command is provided without required arguments
        """
        monkeypatch.setattr(
            "sys.argv",
            ["pypdfeditor", "split"],
        )
        with pytest.raises(SystemExit):
            read_args()

    def test_read_args_split_with_arguments(self, monkeypatch: MonkeyPatch) -> None:
        """
        Test case: should return Args object when split command is provided with required arguments
        """
        monkeypatch.setattr(
            "sys.argv",
            ["pypdfeditor", "split", "test.pdf", "-p", "1-3"],
        )
        args: Args = read_args()
        expected_args: Args = Args(
            command=Command.SPLIT,
            options=SplitArgs(source_file="test.pdf", pages="1-3"),
        )
        assert args == expected_args

    def test_read_args_merge_without_arguments(self, monkeypatch: MonkeyPatch) -> None:
        """
        Test case: should raise exception when merge command is provided without required arguments
        """
        monkeypatch.setattr(
            "sys.argv",
            ["pypdfeditor", "merge"],
        )
        with pytest.raises(SystemExit):
            read_args()

    def test_read_args_merge_with_arguments(self, monkeypatch: MonkeyPatch) -> None:
        """
        Test case: should return Args object when split command is provided with required arguments
        """
        monkeypatch.setattr(
            "sys.argv",
            [
                "pypdfeditor",
                "merge",
                "-o",
                "merged.pdf",
                "-i",
                "file1.pdf",
                "-i",
                "file2.pdf",
                "-i",
                "file3.pdf",
            ],
        )
        args: Args = read_args()
        expected_args: Args = Args(
            command=Command.MERGE,
            options=MergeArgs(
                output_file="merged.pdf",
                input_files=["file1.pdf", "file2.pdf", "file3.pdf"],
            ),
        )
        assert args == expected_args
