try:  # IDE workaround for imports
    from text_hider import TextHider
    from pyscript import Element, js, document
except ModuleNotFoundError:  # in pyscript
    pass

#  https://docs.pyscript.net/latest/tutorials/getting-started.html

from js import method

carrier_element = js.document.getElementById("carrier")
payload_element = js.document.getElementById("payload")

def convert():
    global method
    if method == "hide":
        carrier = carrier_element.value
        ...
        #TextHider.hide(...)
