import pytest
from static.text_hider import TextHider, Ascii, UTF8


@pytest.mark.parametrize(
    "text, character_set",
    [
        ["!0@abnj.>M<?",Ascii],
        ["×sdafd><ZXÝC&Ɲ*$£",UTF8],
    ],
)
def test_detect_character_set(text, character_set):
    assert TextHider._detect_character_set(text) == character_set


@pytest.mark.parametrize(
    "num, radix, numerals, result",
    [
        [15, 2, ["0", "1"], "1111"],
        [879, 16, "0123456789ABCDEF", "36F"],
    ],
)
def test_base_n(num, radix, numerals, result):
    assert TextHider._base_n(num, radix, numerals) == result


@pytest.mark.parametrize(
    "payload, carrier, characters, index, result",
    [
        ["the", "abcdefg", "01", 3, "abc011101000110100001100101defg"],
        ["whƝn", "ZXÝC&Ɲ", "0123456789ABCDEF", 1, "Z00770068019D006EXÝC&Ɲ"],
        ["ä≅≇⦇", "AS⦮⦪", "012345", 4, "AS⦮⦪0001020010434101043430121115"],
    ],
)
def test_hide(payload, carrier, characters, index, result):
    assert TextHider.hide(payload, carrier, characters, index) == result

@pytest.mark.parametrize(
    "input_string, characters, start, end, result",
    [
        ["011101000110100001100101",None,None,None,"the"],
        ["abc011101000110100001100101defg",("0","1"),None,None,"the"],
        ["abc011101000110100001100101defg",None,3,27,"the"],
        ["00770068019D006E",None,None,None,"whƝn"],
        ["Z00770068019D006EXÝC&Ɲ","0123456789ABCDEF",None,None,"whƝn"],
        ["Z00770068019D006EXÝC&Ɲ",1,17,None,"whƝn"],
    ]
)
def test_show(input_string, characters, start, end, result):
    assert TextHider.show(input_string, characters, start=start, end=end).text == result