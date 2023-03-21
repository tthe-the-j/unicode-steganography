import math
import itertools
from sympy import factorint

# import textwrap


class Encoding:
    min_value: int
    max_value: int
    python_string: str

    @classmethod
    def is_valid(cls, character_code):
        return cls.min_value <= character_code <= cls.max_value


def validate(f):
    def wrapper(cls, integer, *args, **kwargs):
        assert cls.is_valid(integer)
        return f(integer, *args, **kwargs)

    return wrapper


class Ascii(Encoding):
    min_value = 0
    max_value = 256
    python_string = "ascii"

    @classmethod
    @validate
    def convert(integer):
        return chr(integer)


class UTF8(Encoding):
    min_value = 0
    max_value = 65536
    python_string = "utf-8"

    @classmethod
    @validate
    def convert(integer):
        return chr(integer)


class Payload:
    def __init__(self, text, characters, encoding, factor):
        self.text = text
        self.characters = characters
        self.encoding = encoding
        self.factor = factor

        self._alphabet_count = None

    def __repr__(self):
        return f"<Payload: text={self.text}>"

    @property
    def alphabet_count(self):
        if self._alphabet_count is None:
            self._alphabet_count = len(
                list(filter(lambda c: 0x41 <= ord(c) <= 0x7A, self.text))
            )
        return self._alphabet_count


class TextHider:
    encodings = [Ascii, UTF8]
    unicode_statistics = None

    @classmethod
    def hide(cls, payload, carrier, allowed_characters, index):
        # base to be encoded in
        radix = len(allowed_characters)
        # detect character set from payload
        payload_character_set = cls._detect_character_set(payload)
        # calculate number of digits needed per bit
        num_of_digits = math.ceil(math.log(payload_character_set.max_value, radix))
        # initialise encoded payload
        encoded_payload = ""
        for character in payload:
            # get character code
            character_code = ord(character)
            # encode character
            encoded_character = cls._base_n(
                character_code, radix, allowed_characters
            )
            # calculate the length of padding needed
            padding_length = num_of_digits - len(encoded_character)
            # add padding to encoded character
            encoded_character = (
                padding_length * allowed_characters[0] + encoded_character
            )
            # add encoded character to encoded payload
            encoded_payload += encoded_character
        # insert encoded payload into carrier at index and return
        return carrier[:index] + encoded_payload + carrier[index:]

    @classmethod
    def show(
        cls,
        input_string,
        characters=None,
        start=None,
        end=None,
        possible_encodings=None,
    ):
        possible_encodings = possible_encodings or cls.encodings
        if characters is not None:
            encoded = "".join(
                (list(filter(lambda c: c in characters, list(input_string))))
            )
        else:
            encoded = input_string[start:end]
        possible_payloads = cls._get_possible_payloads(
            encoded, possible_encodings=possible_encodings
        )
        print(possible_payloads)
        return cls._most_possible_payload(possible_payloads)

    # https://stackoverflow.com/questions/2267362/how-to-convert-an-integer-to-a-string-in-any-base
    @classmethod
    def _base_n(cls, num, radix, numerals):
        # assert that the radix is the same as the number of numerals
        assert radix == len(numerals)
        # recursion tail
        if num == 0:
            return numerals[0]
        # calculate current digit and recurse to find the rest
        return (
            cls._base_n(num // radix, radix, numerals).lstrip(numerals[0])
            + numerals[num % radix]
        )

    @classmethod
    def _decode_base(cls, byte, characters):
        base = len(characters)
        value = 0
        for index, bit in enumerate(byte[::-1]):
            value += (characters.index(bit)) * base ** (index)
        return value

    @classmethod
    def _detect_character_set(cls, string):
        # for each available character set
        for character_set in cls.encodings:
            try:
                # try to encode string in character
                string.encode(character_set.python_string)
                return character_set
            except UnicodeEncodeError:
                pass
        # no available character set works
        raise UnicodeError(f"Can't detect character set: {string}")

    @classmethod
    def _get_possible_payloads(cls, package, possible_encodings=None):
        possible_encodings = possible_encodings or cls.encodings
        # assuming data is not malformed
        unique_characters = set(package)
        print(unique_characters)
        base = len(unique_characters)
        factors = list(factorint(len(package)).keys())[::-1]
        possible_factors = {}
        possible_payloads = []
        perms = itertools.permutations(unique_characters)
        for f in factors:
            possible_character_permutations = {}
            bytes = wrap(package, len(package) // f)
            for characters in perms:
                encoded_data = {encoding: "" for encoding in possible_encodings}
                possible_character_encodings = possible_encodings.copy()
                for byte in bytes:
                    character_code = cls._decode_base(byte, characters)
                    for encoding in possible_encodings:
                        if not encoding.is_valid(character_code):
                            try:
                                possible_character_encodings.remove(encoding)
                            except ValueError:
                                pass
                    if not possible_character_encodings:
                        break
                    for encoding in possible_character_encodings:
                        try:
                            encoded_data[encoding] += encoding.convert(character_code)
                        except OverflowError:
                            break
                else:
                    possible_character_permutations[characters] = encoded_data
                    for encoding, text in encoded_data.items():
                        possible_payloads.append(Payload(text, characters, encoding, f))
            possible_factors[f] = possible_character_permutations
        # return possible_factors
        return possible_payloads

    @classmethod
    def _sort_payloads(cls, possible_payloads):
        # letter_count = lambda text: len(list(filter(lambda c: 0x41 <= ord(c) <= 0x7a, text)))
        # return sorted(list(itertools.chain.from_iterable([[[(letter_count(text), text, characters, factor) for encoding, text in j.items()] for characters, j in i.items()] for factor, i in possible_payloads.items()])))[::-1]
        return sorted(possible_payloads, key=lambda p: p.alphabet_count)[::-1]

    @classmethod
    def _most_possible_payload(cls, possible_payloads):
        return cls._sort_payloads(possible_payloads)[0]


def wrap(text, n):
    return [text[i : i + n] for i in range(0, len(text), n)]


if __name__ == "__main__":
    """
    #TextHider._decode_base("01110100",("0","1"))
    possible = TextHider._get_possible_payloads("011101000110100001100101")
    print(TextHider._sort_payloads(possible))"""
