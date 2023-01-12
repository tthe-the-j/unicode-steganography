try:  # IDE workaround for imports
    from text_hider import TextHider
    from pyscript import Element, js, document
except ModuleNotFoundError:  # in pyscript
    pass

#  https://docs.pyscript.net/latest/tutorials/getting-started.html

carrier_textarea = document.getElementById("work-carrier")
payload_textarea = document.getElementById("work-payload")
button = document.getElementById("work-button")
output = document.getElementById("work-output")

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
    output.innerHTML = result

def decode(*args, **kwargs):
    ...

def show_possible_decodings(*args, **kwargs):
    ...



from js import method # encode or decode

if method == "encode":
    button.
    button.onclick = encode
elif method == "decode":
    button.onclick = decode
