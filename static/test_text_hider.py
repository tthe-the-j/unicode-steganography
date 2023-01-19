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
        ["when the bruh hwen the the eabz", "ZXÝC&Ɲ", "0123456789ABCDEF", 1, "Z7768656E207468652062727568206877656E2074686520746865206561627AXÝC&Ɲ"],
        ["bruh the when", "AS⦮⦪", "012345", 4, "AS⦮⦪0242031003130252005203120252024500520315025202450302"],
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
        ["7768656E207468652062727568206877656E2074686520746865206561627A",None,None,None,"when the bruh hwen the the eabz"],
        ["Z7768656E207468652062727568206877656E2074686520746865206561627AXÝC&Ɲ","0123456789ABCDEF",None,None,"when the bruh hwen the the eabz"],
        ["Z7768656E207468652062727568206877656E2074686520746865206561627AXÝC&Ɲ",None,1,-6,"when the bruh hwen the the eabz"],
        ["0242031003130252005203120252024500520315025202450302",None,None,None,"bruh the when"],
        ["AS⦮⦪0242031003130252005203120252024500520315025202450302","012345",None,None,"bruh the when"],
        ["AS⦮⦪0242031003130252005203120252024500520315025202450302",None,4,None,"bruh the when"],
    ]
)
def test_show(input_string, characters, start, end, result):
    assert TextHider.show(input_string, characters, start=start, end=end, possible_encodings=[TextHider.Ascii]).text == result