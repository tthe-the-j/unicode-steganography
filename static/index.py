try:  # IDE workaround for imports
    from text_hider import TextHider
    from pyscript import Element, js, document
except ModuleNotFoundError:  # in pyscript
    pass

#  https://docs.pyscript.net/latest/tutorials/getting-started.html

carrier_textarea = document.getElementById("encode-carrier")
payload_textarea = document.getElementById("encode-payload")
encode_button = document.getElementById("encode-button")
encode_output = document.getElementById("encode-output")

result = None

test = None


def encode(*args, **kwargs):
    print("encode")
    global test
    test = 1
    carrier = carrier_textarea.value
    payload = payload_textarea.value
    global result
    result = TextHider.hide(payload, carrier, ["0", "1"], 1)
    encode_output.innerHTML = result


encode_button.onclick = encode
