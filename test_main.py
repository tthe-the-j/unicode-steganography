import pytest
import main


@pytest.mark.parametrize(
    "text, character_set",
    [
        ["!0@abnj.>M<?","ascii"],
        ["×sdafd><ZXÝC&Ɲ*$£","utf-8"]
    ],
)
def test_detect_character_set(text, character_set):
    assert main.TextHider._detect_character_set(text) == character_set


@pytest.mark.parametrize(
    "num, radix, numerals, result",
    [
        [15, 2, ["0", "1"], "1111"],
        [879, 16, "0123456789ABCDEF", "36F"]
    ],
)
def test_base_n(num, radix, numerals, result):
    assert main.TextHider._base_n(num, radix, numerals) == result