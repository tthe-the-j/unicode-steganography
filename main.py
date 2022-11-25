import math
import itertools
from sympy import factorint
import textwrap

class Encoding:
    min_value : int
    max_value : int
    python_string : str

    @classmethod
    def is_valid(cls, character_code):
        return cls.min_value <= character_code <= cls.max_value

class Ascii(Encoding):
    min_value = 0
    max_value = 256
    python_string = "ascii"

    @classmethod
    def convert(cls, integer):
        return chr(integer)

class UTF8(Encoding):
    min_value = 0
    max_value = 65536
    python_string = "utf-8"

    @classmethod
    def convert(cls, integer):
        return chr(integer)

class TextHider:
    encodings = [Ascii, UTF8]

    @classmethod
    def hide(cls, payload, carrier, allowed_characters, index):
        _hide = cls._get_hider(allowed_characters)
        return _hide(payload, carrier, index)

    @classmethod
    def show(cls, input_string, indexes=None):
        if indexes is not None:
            encoded = input_string[slice(*indexes)]
        else:
            encoded = input_string
        base = cls._detect_base(encoded)


    """factory"""
    @classmethod
    def _get_hider(cls, allowed_characters):
        def hide(payload, carrier, index):
            radix = len(allowed_characters)
            payload_character_set = cls._detect_character_set(payload)
            num_of_digits = math.ceil(math.log(payload_character_set.max_value, radix))
            encoded_payload = ""
            for character in payload:
                character_code = ord(character)
                encoded_character = cls._base_n(character_code, radix, allowed_characters)
                padding_length = num_of_digits - len(encoded_character)
                encoded_character = padding_length*allowed_characters[0] + encoded_character
                encoded_payload += encoded_character
            return carrier[:index] + encoded_payload + carrier[index:]
        return hide

    @classmethod
    def _base_n(cls, num, radix, numerals):
        assert radix == len(numerals)
        if num == 0:
            return numerals[0]
        return cls._base_n(num // radix, radix, numerals).lstrip(numerals[0]) + numerals[num % radix]

    @classmethod
    def _decode_base(cls, byte, characters):
        base = len(characters)
        value = 0
        for index, bit in enumerate(byte[::-1]):
            value += (characters.index(bit)) * base ** (index)
        return value

    @classmethod
    def _detect_character_set(cls, string):
        for character_set in cls.encodings:
            try:
                string.encode(character_set.python_string)
                return character_set
            except UnicodeEncodeError:
                pass
        raise UnicodeError(f"Can't detect character set: {string}")

    @classmethod
    def _detect_payload(cls, package, possible_encodings=None):
        possible_encodings = possible_encodings or cls.encodings
        # assuming data is not malformed
        unique_characters = set(package)
        base = len(unique_characters)
        factors = list(factorint(len(package)).keys())[::-1]
        possible_factors = {}
        for f in factors:
            possible_character_permutations = {}
            print("factor:" + str(f))
            bytes = textwrap.wrap(package, len(package)//f)
            print(bytes)
            for characters in itertools.permutations(unique_characters):
                print(characters)
                encoded_data = {encoding: "" for encoding in possible_encodings}
                possible_character_encodings = possible_encodings.copy()
                for byte in bytes:
                    print(byte)
                    character_code = cls._decode_base(byte, characters)
                    print(character_code)
                    for encoding in possible_encodings:
                        if not encoding.is_valid(character_code):
                            try:
                                possible_character_encodings.remove(encoding)
                            except ValueError:
                                pass
                    print(possible_character_encodings)
                    if not possible_character_encodings:
                        break
                    for encoding in possible_encodings:
                        try:
                            encoded_data[encoding] += encoding.convert(character_code)
                        except OverflowError:
                            break
                else:
                    possible_character_permutations[characters] = encoded_data
            possible_factors[f] = possible_character_permutations


        return possible_factors







if __name__ == "__main__":
    #print(TextHider._decode_base("01110100",("0","1")))
    print(TextHider._detect_base("011101000110100001100101"))