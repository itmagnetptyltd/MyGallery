"""Belt B — the Upload popup's size, border and controls in a real browser.

REQ-GAL-013@v3 holds the Upload popup to the Larger view: the same close
control, the same border, and Choose files and Upload shaped like Save
description. Each comparison reads computed styles while both elements are
shown, with the pointer parked away from them so no hover style is compared.

No wait_for_function: default-src 'self' forbids the in-page eval it needs.
See constraints/csp-blocks-playwright-wait-for-function.md.
"""

import pytest
from playwright.sync_api import expect
from tests.conftest import an_image, upload_files

DELIVERED_POPUP_WIDTH = 680

CLOSE_CONTROL_LOOK = (
    "width",
    "height",
    "borderTopWidth",
    "borderTopStyle",
    "borderTopColor",
    "borderRadius",
    "backgroundColor",
    "color",
)

BORDER = tuple(
    f"border{side}{part}"
    for side in ("Top", "Right", "Bottom", "Left")
    for part in ("Width", "Style", "Color")
)

BUTTON_LOOK = (
    "borderTopWidth",
    "borderTopStyle",
    "borderTopColor",
    "borderRadius",
    "backgroundColor",
    "color",
)

_READ_STYLE = """([selector, names]) => {
  const style = getComputedStyle(document.querySelector(selector));
  return Object.fromEntries(names.map((name) => [name, style[name]]));
}"""


@pytest.fixture
def gallery_url(running_server) -> str:
    return f"http://{running_server.host}:{running_server.port}"


def _style(page, selector: str, names: tuple[str, ...]) -> dict[str, str]:
    page.mouse.move(1, 1)
    return page.evaluate(_READ_STYLE, [selector, list(names)])


def _open_larger_view(page, gallery_url, tmp_path) -> None:
    photo = tmp_path / "harbour.jpg"
    photo.write_bytes(an_image("JPEG", size=(900, 700)))
    page.set_viewport_size({"width": 1280, "height": 800})
    page.goto(gallery_url)
    upload_files(page, str(photo))
    expect(page.get_by_test_id("thumbnail")).to_have_count(1)
    page.get_by_test_id("thumbnail").first.click()
    expect(page.get_by_test_id("larger-view")).to_be_visible()


def _open_upload_popup_after_larger_view(page) -> None:
    page.keyboard.press("Escape")
    expect(page.get_by_test_id("larger-view")).to_be_hidden()
    page.get_by_test_id("upload-open").click()
    expect(page.get_by_test_id("upload-popup")).to_be_visible()


# @covers REQ-GAL-013@v3
def test_the_upload_popup_is_wider_than_680_pixels_on_a_1280_pixel_screen(page, gallery_url):
    page.set_viewport_size({"width": 1280, "height": 800})
    page.goto(gallery_url)

    page.get_by_test_id("upload-open").click()
    expect(page.get_by_test_id("upload-popup")).to_be_visible()
    popup = page.get_by_test_id("upload-popup").bounding_box()

    assert popup is not None
    assert popup["width"] > DELIVERED_POPUP_WIDTH


# @covers REQ-GAL-013@v3
# @covers REQ-GAL-019@v2
def test_the_upload_popup_close_control_looks_like_the_larger_views(page, gallery_url, tmp_path):
    _open_larger_view(page, gallery_url, tmp_path)
    larger_view_close = _style(page, '[data-testid="larger-view-close"]', CLOSE_CONTROL_LOOK)

    _open_upload_popup_after_larger_view(page)
    upload_close = _style(page, '[data-testid="upload-popup-close"]', CLOSE_CONTROL_LOOK)

    assert upload_close == larger_view_close


# @covers REQ-GAL-013@v3
def test_the_upload_popup_has_the_larger_view_panels_border(page, gallery_url, tmp_path):
    _open_larger_view(page, gallery_url, tmp_path)
    panel_border = _style(page, '[data-testid="larger-view"]', BORDER)

    _open_upload_popup_after_larger_view(page)
    popup_border = _style(page, '[data-testid="upload-popup"]', BORDER)

    assert popup_border == panel_border


# @covers REQ-GAL-013@v3
def test_choose_files_and_upload_look_like_save_description(page, gallery_url, tmp_path):
    _open_larger_view(page, gallery_url, tmp_path)
    save = _style(page, '[data-testid="description-save"]', BUTTON_LOOK)

    _open_upload_popup_after_larger_view(page)
    choose = _style(page, ".upload-pick span", BUTTON_LOOK)
    upload = _style(page, '[data-testid="upload-submit"]', BUTTON_LOOK)

    assert save["borderRadius"] != "50%"
    assert choose == save
    assert upload == save
