import math

class TextHider:
    character_sets = ["ascii", "utf-8"]

    @classmethod
    def hide_text(cls, payload, carrier, allowed_characters, index):
        hide = cls._get_hider(allowed_characters)
        return hide(payload, carrier, index)

    """factory"""
    @classmethod
    def _get_hider(cls, allowed_characters):
        def hide(payload, carrier, index):
            radix = len(allowed_characters)
            payload_character_set = cls._detect_character_set(payload)
            if payload_character_set == "ascii":
                max_value = 256
            if payload_character_set == "utf-8":
                max_value = 1114111
            num_of_digits = math.ceil(math.log(max_value, radix))
            encoded_payload = ""
            for character in payload:
                character_code = ord(character)
                encoded_character = cls._base_n(character_code, radix, allowed_characters)
                padding_length = num_of_digits - len(encoded_character)
                encoded_character = padding_length*allowed_characters[0] + encoded_character
                encoded_payload += encoded_character
            return carrier.insert(encoded_payload, index)

        return hide

    @classmethod
    def _base_n(cls, num, radix, numerals):
        assert radix == len(numerals)
        if num == 0:
            return numerals[0]
        return cls._base_n(num // radix, radix, numerals).lstrip(numerals[0]) + numerals[num % radix]

    @classmethod
    def _detect_character_set(cls, string):
        for character_set in cls.character_sets:
            try:
                string.encode(character_set)
                return character_set
            except UnicodeEncodeError:
                pass
        raise UnicodeError(f"Can't detect character set: {string}")






