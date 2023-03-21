import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(scope="function", autouse=True)
def go_to_website(page: Page):
    # Go to the starting url before each test
    page.goto("http://127.0.0.1:5000/")


def test_title(page):
    expect(page).to_have_title("Unicode Steganography")


def test_form_visibility(page):
    hide_form = page.locator("#hide")
    show_form = page.locator("#show")
    hide_swap_button = hide_form.get_by_role("button", name="Swap")
    show_swap_button = show_form.get_by_role("button", name="Swap")

    # test initial visibility
    expect(hide_form).to_have_css("display", "block")
    expect(show_form).to_have_css("display", "none")

    # swap forms
    hide_swap_button.click()

    # check swapped visibility
    expect(hide_form).to_have_css("display", "none")
    expect(show_form).to_have_css("display", "block")

    # swap back
    show_swap_button.click()

    # test original visibility
    expect(hide_form).to_have_css("display", "block")
    expect(show_form).to_have_css("display", "none")


def test_hide_form(page):
    hide_form = page.locator("#hide")
    text_input = page.locator("#text")
    carrier_input = page.locator("#carrier")
    hide_output = page.locator("#hide-output")
    hide_convert_button = hide_form.get_by_role("button", name="Convert")

    parameters = [
        ["the", "abcdefg", "‌‍‍‍‌‍‌‌‌‍‍‌‍‌‌‌‌‍‍‌‌‍‌‍abcdefg"],
        ["when the bruh hwen the the eabz", "ZXÝC&Ɲ", "‌‍‍‍‌‍‍‍‌‍‍‌‍‌‌‌‌‍‍‌‌‍‌‍‌‍‍‌‍‍‍‌‌‌‍‌‌‌‌‌‌‍‍‍‌‍‌‌‌‍‍‌‍‌‌‌‌‍‍‌‌‍‌‍‌‌‍‌‌‌‌‌‌‍‍‌‌‌‍‌‌‍‍‍‌‌‍‌‌‍‍‍‌‍‌‍‌‍‍‌‍‌‌‌‌‌‍‌‌‌‌‌‌‍‍‌‍‌‌‌‌‍‍‍‌‍‍‍‌‍‍‌‌‍‌‍‌‍‍‌‍‍‍‌‌‌‍‌‌‌‌‌‌‍‍‍‌‍‌‌‌‍‍‌‍‌‌‌‌‍‍‌‌‍‌‍‌‌‍‌‌‌‌‌‌‍‍‍‌‍‌‌‌‍‍‌‍‌‌‌‌‍‍‌‌‍‌‍‌‌‍‌‌‌‌‌‌‍‍‌‌‍‌‍‌‍‍‌‌‌‌‍‌‍‍‌‌‌‍‌‌‍‍‍‍‌‍‌ZXÝC&Ɲ"],
        ["bruh the when", "AS⦮⦪", "‌‍‍‌‌‌‍‌‌‍‍‍‌‌‍‌‌‍‍‍‌‍‌‍‌‍‍‌‍‌‌‌‌‌‍‌‌‌‌‌‌‍‍‍‌‍‌‌‌‍‍‌‍‌‌‌‌‍‍‌‌‍‌‍‌‌‍‌‌‌‌‌‌‍‍‍‌‍‍‍‌‍‍‌‍‌‌‌‌‍‍‌‌‍‌‍‌‍‍‌‍‍‍‌AS⦮⦪"],
    ]

    for t in parameters:
        text_input.fill(t[0])
        carrier_input.fill(t[1])
        hide_convert_button.click()
        expect(hide_output).to_have_value(t[2])


def test_show_form(page):
    hide_form = page.locator("#hide")
    show_form = page.locator("#show")
    payload_input = page.locator("#payload")
    show_output = page.locator("#show-output")
    show_convert_button = show_form.get_by_role("button", name="Convert")
    hide_swap_button = hide_form.get_by_role("button", name="Swap")

    parameters = [
        ["‌‍‍‍‌‍‌‌‌‍‍‌‍‌‌‌‌‍‍‌‌‍‌‍abcdefg", "the"],
        ["‌‍‍‍‌‍‍‍‌‍‍‌‍‌‌‌‌‍‍‌‌‍‌‍‌‍‍‌‍‍‍‌‌‌‍‌‌‌‌‌‌‍‍‍‌‍‌‌‌‍‍‌‍‌‌‌‌‍‍‌‌‍‌‍‌‌‍‌‌‌‌‌‌‍‍‌‌‌‍‌‌‍‍‍‌‌‍‌‌‍‍‍‌‍‌‍‌‍‍‌‍‌‌‌‌‌‍‌‌‌‌‌‌‍‍‌‍‌‌‌‌‍‍‍‌‍‍‍‌‍‍‌‌‍‌‍‌‍‍‌‍‍‍‌‌‌‍‌‌‌‌‌‌‍‍‍‌‍‌‌‌‍‍‌‍‌‌‌‌‍‍‌‌‍‌‍‌‌‍‌‌‌‌‌‌‍‍‍‌‍‌‌‌‍‍‌‍‌‌‌‌‍‍‌‌‍‌‍‌‌‍‌‌‌‌‌‌‍‍‌‌‍‌‍‌‍‍‌‌‌‌‍‌‍‍‌‌‌‍‌‌‍‍‍‍‌‍‌ZXÝC&Ɲ","when the bruh hwen the the eabz"],
        ["‌‍‍‌‌‌‍‌‌‍‍‍‌‌‍‌‌‍‍‍‌‍‌‍‌‍‍‌‍‌‌‌‌‌‍‌‌‌‌‌‌‍‍‍‌‍‌‌‌‍‍‌‍‌‌‌‌‍‍‌‌‍‌‍‌‌‍‌‌‌‌‌‌‍‍‍‌‍‍‍‌‍‍‌‍‌‌‌‌‍‍‌‌‍‌‍‌‍‍‌‍‍‍‌AS⦮⦪", "bruh the when"]
    ]

    hide_swap_button.click()

    for t in parameters:
        payload_input.fill(t[0])
        show_convert_button.click()
        expect(show_output).to_have_value(t[1])
