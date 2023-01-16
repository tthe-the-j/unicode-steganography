try:  # IDE workaround for imports
    from text_hider import TextHider
    from pyscript import Element, js, document
except ModuleNotFoundError:  # in pyscript
    pass

#  https://docs.pyscript.net/latest/tutorials/getting-started.html

carrier_element = js.document.getElementById("carrier")
payload_element = js.document.getElementById("payload")
output_element = js.document.getElementById("output")

convert_button = js.document.getElementById("convert")


def convert(*args):
    print("convert")
    from js import method
    if method == "hide":
        carrier = carrier_element.value
        payload = payload_element.value
        allowed_characters = ["0", "1"]
        index = 0
        hidden = TextHider.hide(payload, carrier, allowed_characters, index)
        print(hidden)
        output_element.innerHTML = hidden


convert_button.onclick = convert