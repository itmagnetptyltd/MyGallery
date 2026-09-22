"""Belt B — REQ-GAL-004: the Larger view over the Gallery, in a real browser."""

import pytest
from playwright.sync_api import expect
from tests.conftest import a_coloured_image, an_image, upload_files


@pytest.fixture
def gallery_url(running_server) -> str:
    return f"http://{running_server.host}:{running_server.port}"


def _upload(page, tmp_path, count: int) -> None:
    names = []
    for n in range(count):
        photo = tmp_path / f"p{n}.jpg"
        photo.write_bytes(an_image("JPEG", size=(900, 700)))
        names.append(str(photo))
    upload_files(page, names)
    expect(page.get_by_test_id("thumbnail")).to_have_count(count)


def test_the_larger_view_is_not_shown_before_a_thumbnail_is_activated(page, gallery_url, tmp_path):
    page.goto(gallery_url)
    _upload(page, tmp_path, 1)

    expect(page.get_by_test_id("larger-view")).to_be_hidden()


# @covers REQ-GAL-004@v3
def test_activating_a_thumbnail_shows_the_larger_view(page, gallery_url, tmp_path):
    page.goto(gallery_url)
    _upload(page, tmp_path, 1)

    page.get_by_test_id("thumbnail").first.click()

    expect(page.get_by_test_id("larger-view")).to_be_visible()


# @covers REQ-GAL-004@v3
def test_the_larger_view_shows_the_photo_that_was_activated(page, gallery_url, tmp_path):
    red = tmp_path / "red.png"
    red.write_bytes(a_coloured_image((220, 20, 20), size=(900, 700)))
    blue = tmp_path / "blue.png"
    blue.write_bytes(a_coloured_image((20, 20, 220), size=(900, 700)))
    page.goto(gallery_url)
    upload_files(page, [str(red), str(blue)])
    expect(page.get_by_test_id("thumbnail")).to_have_count(2)

    # Newest first, so blue.png is the first tile. Activate the second — red.
    page.get_by_test_id("thumbnail").nth(1).click()

    expect(page.get_by_test_id("larger-view-photo")).to_have_attribute(
        "data-filename", "red.png"
    )


# @covers REQ-GAL-004@v3
def test_the_photo_is_rendered_larger_than_its_thumbnail(page, gallery_url, tmp_path):
    page.goto(gallery_url)
    _upload(page, tmp_path, 1)
    thumbnail_box = page.get_by_test_id("thumbnail").first.bounding_box()

    page.get_by_test_id("thumbnail").first.click()
    expect(page.get_by_test_id("larger-view-photo")).to_be_visible()
    photo_box = page.get_by_test_id("larger-view-photo").bounding_box()

    assert photo_box["width"] > thumbnail_box["width"]


# @covers REQ-GAL-004@v3
def test_pressing_escape_closes_the_larger_view(page, gallery_url, tmp_path):
    page.goto(gallery_url)
    _upload(page, tmp_path, 1)
    page.get_by_test_id("thumbnail").first.click()
    expect(page.get_by_test_id("larger-view")).to_be_visible()

    page.keyboard.press("Escape")

    expect(page.get_by_test_id("larger-view")).to_be_hidden()


# @covers REQ-GAL-004@v3
def test_the_gallery_is_shown_again_after_escape(page, gallery_url, tmp_path):
    page.goto(gallery_url)
    _upload(page, tmp_path, 1)
    page.get_by_test_id("thumbnail").first.click()

    page.keyboard.press("Escape")

    expect(page.get_by_test_id("gallery")).to_be_visible()


# @covers REQ-GAL-004@v3
def test_activating_the_close_control_closes_the_larger_view(page, gallery_url, tmp_path):
    page.goto(gallery_url)
    _upload(page, tmp_path, 1)
    page.get_by_test_id("thumbnail").first.click()
    expect(page.get_by_test_id("larger-view")).to_be_visible()

    page.get_by_test_id("larger-view-close").click()

    expect(page.get_by_test_id("larger-view")).to_be_hidden()


# @covers REQ-GAL-004@v3
def test_the_gallery_is_shown_again_after_the_close_control(page, gallery_url, tmp_path):
    page.goto(gallery_url)
    _upload(page, tmp_path, 1)
    page.get_by_test_id("thumbnail").first.click()

    page.get_by_test_id("larger-view-close").click()

    expect(page.get_by_test_id("gallery")).to_be_visible()


# @covers REQ-GAL-004@v3
def test_the_gallery_keeps_its_scroll_position_when_the_larger_view_closes(
    page, gallery_url, tmp_path
):
    # Short viewport and enough tiles that the Gallery genuinely overflows —
    # otherwise there is nothing to scroll and the test proves nothing.
    page.set_viewport_size({"width": 700, "height": 400})
    page.goto(gallery_url)
    _upload(page, tmp_path, 24)

    # scrollTo rather than mouse.wheel + wait_for_function: the page sets
    # Content-Security-Policy: default-src 'self', and wait_for_function
    # evaluates its predicate as a string inside the page, which that policy
    # refuses as unsafe-eval. This is deterministic and needs no polling.
    page.evaluate("window.scrollTo(0, 600)")
    page.get_by_test_id("thumbnail").last.click()
    expect(page.get_by_test_id("larger-view")).to_be_visible()

    # Read the position with the Larger view open, not before activating it:
    # clicking scrolls the tile into view, so the pre-click position is not
    # the place the user is returning to. Guarded so a Gallery that never
    # scrolled cannot pass this silently.
    activated_at = page.evaluate("window.scrollY")
    assert activated_at > 0, "the Gallery did not scroll, so the test proves nothing"

    page.get_by_test_id("larger-view-close").click()
    expect(page.get_by_test_id("larger-view")).to_be_hidden()

    assert page.evaluate("window.scrollY") == activated_at
