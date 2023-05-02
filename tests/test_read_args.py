import pytest

from pytest import MonkeyPatch

import pypdfeditor.main as m


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
            m.main()

    def test_read_args_split_without_arguments(self, monkeypatch) -> None:
        """
        Test case: should raise exception when split command is provided without required arguments
        """
        monkeypatch.setattr(
            "sys.argv",
            ["pypdfeditor", "split"],
        )
        with pytest.raises(SystemExit):
            m.main()

    def test_read_args_split_with_arguments(self, monkeypatch) -> None:
        """
        Test case: should return Args object when split command is provided with required arguments
        """
        monkeypatch.setattr(
            "sys.argv",
            ["pypdfeditor", "split", "test.pdf", "-p", "1-3"],
        )
        args: m.Args = m.read_args()
        expected_args: m.Args = m.Args(
            command=m.Command.SPLIT,
            options=m.SplitArgs(source_file="test.pdf", pages="1-3"),
        )
        assert args == expected_args
