import pytest

from pypdfeditor.parser import parse_page_range, parse_page_ranges


class TestParsePageRange:
    @pytest.mark.parametrize(
        "page_range, expected_page_range",
        [
            ("1-10,11", {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}),
            ("1-3,5,7", {1, 2, 3, 5, 7}),
            ("2-6,9-10", {2, 3, 4, 5, 6, 9, 10}),
            ("1", {1}),
            ("1-10,11,15,100", {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 15, 100}),
            ("1,10-15", {1, 10, 11, 12, 13, 14, 15}),
            ("1,3-5", {1, 3, 4, 5}),
            ("1-3,5,8-9", {1, 2, 3, 5, 8, 9}),
        ],
    )
    def test_parse_valid_ranges_returning_set(
        self, page_range: str, expected_page_range: set[int]
    ) -> None:
        """
        Test case: should return a set of int if page_range input is valid
        """
        pages: set[int] = parse_page_range(pages=page_range)
        assert pages == expected_page_range

    @pytest.mark.parametrize(
        "page_range, expected_page_range",
        [
            ("1-10,11", [{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}, {11}]),
            ("1-3,5,7", [{1, 2, 3}, {5}, {7}]),
            ("2-6,9-10", [{2, 3, 4, 5, 6}, {9, 10}]),
            ("1", [{1}]),
            ("1-10,11,15,100", [{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}, {11}, {15}, {100}]),
            ("1,10-15", [{1}, {10, 11, 12, 13, 14, 15}]),
            ("1,3-5", [{1}, {3, 4, 5}]),
            ("1-3,5,8-9", [{1, 2, 3}, {5}, {8, 9}]),
        ],
    )
    def test_parse_valid_ranges_returning_list_of_sets(
        self, page_range: str, expected_page_range: list[set[int]]
    ) -> None:
        """
        Test case: should return a set of int if page_range input is valid
        """
        pages: list[set[int]] = parse_page_ranges(pages=page_range)
        assert pages == expected_page_range
