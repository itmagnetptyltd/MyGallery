"""Belt B — UAT visual in a real browser.

No wait_for_function: default-src 'self' forbids the in-page eval it needs.
See constraints/csp-blocks-playwright-wait-for-function.md.
"""

import re

from playwright.sync_api import expect
from tests.conftest import an_image, upload_files


def _gallery_url(running_server) -> str:
    return f"http://{running_server.host}:{running_server.port}"


def _upload_one(page, tmp_path) -> None:
    photo = tmp_path / "holiday.jpg"
    photo.write_bytes(an_image("JPEG", size=(900, 700)))
    page.get_by_test_id("upload-open").click()
    expect(page.get_by_test_id("upload-popup")).to_be_visible()
    upload_files(page, str(photo))
    expect(page.get_by_test_id("thumbnail")).to_have_count(1)


def _box_inside(inner: dict, outer: dict) -> bool:
    return (
        inner["x"] >= outer["x"]
        and inner["y"] >= outer["y"]
        and inner["x"] + inner["width"] <= outer["x"] + outer["width"]
        and inner["y"] + inner["height"] <= outer["y"] + outer["height"]
    )


def _grid_minmax_px(page) -> int:
    value = page.evaluate(
        """() => {
          for (const sheet of document.styleSheets) {
            for (const rule of sheet.cssRules) {
              if (rule.selectorText === ".gallery") {
                return rule.style.gridTemplateColumns;
              }
            }
          }
          return "";
        }"""
    )
    match = re.search(r"minmax\((\d+)px", value)
    assert match is not None, f"Gallery grid has no minmax size: {value!r}"
    return int(match.group(1))


# @covers REQ-GAL-012@v2
# @covers REQ-GAL-003@v3
def test_a_thumbnail_card_is_wider_than_160_pixels(page, running_server, tmp_path):
    page.goto(_gallery_url(running_server))
    _upload_one(page, tmp_path)

    assert _grid_minmax_px(page) > 160
    box = page.get_by_test_id("thumbnail-card").first.bounding_box()
    assert box is not None
    assert box["width"] > 160


# @covers REQ-GAL-012@v2
# @covers REQ-GAL-003@v3
def test_a_thumbnail_is_shown_as_a_card_not_a_bare_image(page, running_server, tmp_path):
    page.goto(_gallery_url(running_server))
    _upload_one(page, tmp_path)

    card = page.get_by_test_id("thumbnail-card").first
    expect(card).to_be_visible()
    expect(card.get_by_test_id("thumbnail")).to_be_visible()
    padding = card.evaluate("el => getComputedStyle(el).padding")
    assert padding != "0px"


# @covers REQ-GAL-013@v2
# @covers REQ-GAL-001@v3
def test_starting_an_upload_opens_a_popup(page, running_server):
    page.goto(_gallery_url(running_server))

    expect(page.get_by_test_id("upload-popup")).to_be_hidden()
    page.get_by_test_id("upload-open").click()

    expect(page.get_by_test_id("upload-popup")).to_be_visible()
    expect(page.get_by_test_id("upload-input")).to_be_attached()


# @covers REQ-GAL-013@v2
# @covers REQ-GAL-007@v2
def test_an_empty_gallery_shows_a_control_that_opens_the_upload_popup(
    page, running_server
):
    page.goto(_gallery_url(running_server))

    expect(page.get_by_test_id("empty-gallery")).to_be_visible()
    expect(page.get_by_test_id("upload-open")).to_be_visible()
    page.get_by_test_id("upload-open").click()

    expect(page.get_by_test_id("upload-popup")).to_be_visible()


# @covers REQ-GAL-014@v1
# @covers REQ-GAL-004@v2
def test_the_close_control_is_inside_the_larger_view_panel(page, running_server, tmp_path):
    page.goto(_gallery_url(running_server))
    _upload_one(page, tmp_path)
    page.get_by_test_id("thumbnail").first.click()
    expect(page.get_by_test_id("larger-view")).to_be_visible()

    panel = page.get_by_test_id("larger-view").bounding_box()
    close = page.get_by_test_id("larger-view-close").bounding_box()

    assert panel is not None and close is not None
    assert _box_inside(close, panel)


# @covers REQ-GAL-014@v1
# @covers REQ-GAL-004@v2
def test_the_delete_control_is_inside_the_larger_view_panel(page, running_server, tmp_path):
    page.goto(_gallery_url(running_server))
    _upload_one(page, tmp_path)
    page.get_by_test_id("thumbnail").first.click()
    expect(page.get_by_test_id("larger-view")).to_be_visible()

    panel = page.get_by_test_id("larger-view").bounding_box()
    delete = page.get_by_test_id("delete-photo").bounding_box()

    assert panel is not None and delete is not None
    assert _box_inside(delete, panel)


# --- REQ-GAL-012@v2 / REQ-GAL-013@v2 ----------------------------------------


# @covers REQ-GAL-013@v2
# @covers REQ-GAL-019@v1
def test_the_upload_popup_close_control_is_inside_the_popup_at_its_top_right(
    page, running_server
):
    page.goto(_gallery_url(running_server))
    page.get_by_test_id("upload-open").click()
    expect(page.get_by_test_id("upload-popup")).to_be_visible()

    popup = page.get_by_test_id("upload-popup").bounding_box()
    close = page.get_by_test_id("upload-popup-close").bounding_box()

    assert popup is not None and close is not None
    assert _box_inside(close, popup)
    # Top right: in the upper and the right-hand quarter of the panel.
    assert close["y"] < popup["y"] + popup["height"] / 4
    assert close["x"] > popup["x"] + popup["width"] * 3 / 4


# @covers REQ-GAL-013@v2
# @covers REQ-GAL-019@v1
def test_closing_the_upload_popup_adds_no_photo(page, running_server):
    page.goto(_gallery_url(running_server))
    page.get_by_test_id("upload-open").click()

    page.get_by_test_id("upload-popup-close").click()

    expect(page.get_by_test_id("upload-popup")).to_be_hidden()
    expect(page.get_by_test_id("photo-count")).to_have_text("0")


# @covers REQ-GAL-013@v2
# @covers REQ-GAL-019@v1
def test_the_upload_popup_can_be_reopened_after_it_was_closed(page, running_server):
    page.goto(_gallery_url(running_server))
    page.get_by_test_id("upload-open").click()
    page.get_by_test_id("upload-popup-close").click()

    page.get_by_test_id("upload-open").click()

    expect(page.get_by_test_id("upload-popup")).to_be_visible()


# @covers REQ-GAL-013@v2
def test_the_upload_popup_previews_every_chosen_file(page, running_server, tmp_path):
    photos = []
    for n in range(3):
        photo = tmp_path / f"p{n}.jpg"
        photo.write_bytes(an_image("JPEG"))
        photos.append(str(photo))
    page.goto(_gallery_url(running_server))
    page.get_by_test_id("upload-open").click()

    page.get_by_test_id("upload-input").set_input_files(photos)

    expect(page.get_by_test_id("upload-preview")).to_have_count(3)
    expect(page.get_by_test_id("photo-count")).to_have_text("0")


# @covers REQ-GAL-012@v2
def test_a_thumbnail_shows_its_photos_description_as_alt_text(page, running_server, tmp_path):
    photo = tmp_path / "holiday.jpg"
    photo.write_bytes(an_image("JPEG"))
    page.goto(_gallery_url(running_server))
    page.get_by_test_id("upload-open").click()
    page.get_by_test_id("upload-input").set_input_files(str(photo))
    page.get_by_test_id("upload-description").fill("Beach at dawn")

    page.get_by_test_id("upload-submit").click()

    expect(page.get_by_test_id("thumbnail")).to_have_attribute("alt", "Beach at dawn")


# @covers REQ-GAL-016@v1
def test_the_picker_still_chooses_files_when_dropping_is_available(
    page, running_server, tmp_path
):
    """REQ-GAL-016 c3. Dropping was added alongside the picker, not over it."""
    photo = tmp_path / "picked.jpg"
    photo.write_bytes(an_image("JPEG"))
    page.goto(_gallery_url(running_server))
    page.get_by_test_id("upload-open").click()

    page.get_by_test_id("upload-input").set_input_files(str(photo))
    page.get_by_test_id("upload-submit").click()

    expect(page.get_by_test_id("photo-count")).to_have_text("1")
