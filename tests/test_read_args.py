import pytest

from pytest import MonkeyPatch

from pypdfeditor.type_definitions import Args, Command, SplitArgs
from pypdfeditor.read_args import read_args


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
