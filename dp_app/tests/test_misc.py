import pytest
from dp_app.utils import misc as ufm

test_data1 = [
    (
        ["fox", "jump"],
        "The quick brown fox jumps over the lazy dog.",
        True,
    ),
    (
        ["cat", "jump"],
        "The quick brown fox jumps over the lazy dog.",
        True,
    ),
    (
        ["cat", "cuddle"],
        "The quick brown fox jumps over the lazy dog.",
        False,
    ),
]


@pytest.mark.parametrize("items, text, expected_output", test_data1)
def test_check_if_any_list_item_in_str(items: list, text: str, expected_output: bool):
    assert ufm.check_if_any_list_item_in_str(items, text) == expected_output


test_data2 = [
    (
        [
            {"animal": "fox", "color": "brown"},
            {"animal": "fox", "color": "brown"},
        ],
        [
            {"animal": "fox", "color": "brown"},
        ],
    ),
    (
        [
            {"animal": "cat", "color": "brown"},
            {"animal": "fox", "color": "brown"},
        ],
        [
            {"animal": "cat", "color": "brown"},
            {"animal": "fox", "color": "brown"},
        ],
    ),
]


@pytest.mark.parametrize("records, expected_output", test_data2)
def test_dedupe_list_of_dict(records: list[dict], expected_output: list[dict]):
    assert ufm.dedupe_list_of_dict(records) == expected_output
