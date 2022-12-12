import pytest
from static.text_hider import TextHider


@pytest.mark.parametrize(
    "text, character_set",
    [
        ["!0@abnj.>M<?","ascii"],
        ["×sdafd><ZXÝC&Ɲ*$£","utf-8"]
    ],
)
def test_detect_character_set(text, character_set):
    assert TextHider._detect_character_set(text) == character_set


@pytest.mark.parametrize(
    "num, radix, numerals, result",
    [
        [15, 2, ["0", "1"], "1111"],
        [879, 16, "0123456789ABCDEF", "36F"]
    ],
)
def test_base_n(num, radix, numerals, result):
    assert TextHider._base_n(num, radix, numerals) == result


@pytest.mark.parametrize(
    "payload, carrier, characters, index, result",
    [
        ["the", "abcdefg", "01", 3, "abc011101000110100001100101defg"],
        ["whƝn", "ZXÝC&Ɲ", "0123456789ABCDEF", 1, "Z00770068019D006EXÝC&Ɲ"],
        ["ä≅≇⦇", "AS⦮⦪", "012345", 4, "AS⦮⦪0001020010434101043430121115"]
    ],
)
def test_hide(payload, carrier, characters, index, result):
    assert TextHider.hide(payload, carrier, characters, index) == result