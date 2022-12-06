try:  # IDE workaround for imports
    from text_hider import TextHider
    from pyscript import Element
except ModuleNotFoundError:  # in pyscript
    pass

#  https://docs.pyscript.net/latest/tutorials/getting-started.html

carrier_textarea = Element("encode-carrier")
payload_textarea = Element("encode-payload")
encode_button = Element("encode-button")
encode_output = Element("encode-output")

result = None


def encode(*args, **kwargs):
    carrier = carrier_textarea.value
    payload = payload_textarea.value
    global result
    result = TextHider.hide(payload, carrier)
    encode_output.write(result)