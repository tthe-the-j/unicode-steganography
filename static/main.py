try:  # IDE workaround for imports
    from text_hider import TextHider
    from pyscript import Element, js, document
    import pyscript
except ModuleNotFoundError:  # executing in pyscript
    pass

text_element = js.document.getElementById("text")
carrier_element = js.document.getElementById("carrier")
payload_element = js.document.getElementById("payload")
hide_output_element = js.document.getElementById("hide-output")
show_output_element = js.document.getElementById("show-output")
hide_convert_button = js.document.getElementById("hide-convert")
show_convert_button = js.document.getElementById("show-convert")

allowed_characters = ["\u200C", "\u200D"]

def hide_convert(*args):
    text = text_element.value
    carrier = carrier_element.value
    index = 0
    output = TextHider.hide(text, carrier, allowed_characters, index)
    hide_output_element.innerText = output
    print(f"""hide_convert()
{text=}
{carrier=}
{allowed_characters=}
{index=}
{output=}""")


def show_convert(*args):
    payload = payload_element.value
    output = TextHider.show(payload, characters=allowed_characters).text
    show_output_element.innerText = output
    print(f"""show_convert()
{payload=}
{output=}""")


hide_convert_button.onclick = hide_convert
show_convert_button.onclick = show_convert
