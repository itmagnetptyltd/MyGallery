"""Belt B — REQ-GAL-003 and REQ-GAL-007 in a real browser."""

import pytest
from playwright.sync_api import expect
from tests.conftest import an_image, upload_files


@pytest.fixture
def gallery_url(running_server) -> str:
    return f"http://{running_server.host}:{running_server.port}"


def _upload(page, tmp_path, count: int) -> list[str]:
    names = []
    for n in range(count):
        photo = tmp_path / f"p{n}.jpg"
        photo.write_bytes(an_image("JPEG"))
        names.append(str(photo))
    upload_files(page, names)
    return names


# --- REQ-GAL-007: the empty Gallery ------------------------------------------


# @covers REQ-GAL-007@v2
def test_an_empty_gallery_shows_no_thumbnail(page, gallery_url):
    page.goto(gallery_url)

    expect(page.get_by_test_id("thumbnail")).to_have_count(0)


# @covers REQ-GAL-007@v2
def test_an_empty_gallery_says_there_are_no_photos_yet(page, gallery_url):
    page.goto(gallery_url)

    expect(page.get_by_test_id("empty-gallery")).to_be_visible()


# @covers REQ-GAL-007@v2
def test_an_empty_gallery_shows_the_upload_control(page, gallery_url):
    page.goto(gallery_url)

    expect(page.get_by_test_id("upload-control")).to_be_visible()


# @covers REQ-GAL-007@v2
def test_an_empty_gallery_reports_no_error(page, gallery_url):
    page.goto(gallery_url)

    # The criterion is that no error is *reported*, not that no error element
    # exists in the document — the message is present but hidden.
    expect(page.get_by_test_id("gallery-error")).to_be_hidden()


# --- REQ-GAL-003: what the Gallery shows -------------------------------------


# @covers REQ-GAL-003@v4
def test_uploaded_photos_appear_as_thumbnails(page, gallery_url, tmp_path):
    page.goto(gallery_url)

    _upload(page, tmp_path, 3)

    expect(page.get_by_test_id("thumbnail")).to_have_count(3)


# @covers REQ-GAL-003@v4
def test_the_no_photos_message_goes_once_a_photo_is_uploaded(page, gallery_url, tmp_path):
    page.goto(gallery_url)

    _upload(page, tmp_path, 1)

    expect(page.get_by_test_id("empty-gallery")).to_be_hidden()


# @covers REQ-GAL-003@v4
def test_thumbnails_appear_newest_first(page, gallery_url, tmp_path):
    page.goto(gallery_url)
    _upload(page, tmp_path, 3)
    expect(page.get_by_test_id("thumbnail")).to_have_count(3)

    first_tile = page.get_by_test_id("thumbnail").first

    expect(first_tile).to_have_attribute("data-filename", "p2.jpg")


# @covers REQ-GAL-003@v4
def test_no_numbered_page_control_is_shown(page, gallery_url, tmp_path):
    page.goto(gallery_url)
    _upload(page, tmp_path, 3)
    expect(page.get_by_test_id("thumbnail")).to_have_count(3)

    expect(page.get_by_test_id("page-control")).to_have_count(0)


# @covers REQ-GAL-003@v4
def test_scrolling_to_the_end_loads_more_thumbnails(page, gallery_url, tmp_path):
    from mygallery import config

    page.goto(gallery_url)
    _upload(page, tmp_path, config.PAGE_SIZE + 3)
    expect(page.get_by_test_id("thumbnail")).to_have_count(config.PAGE_SIZE)

    page.mouse.wheel(0, 100_000)

    expect(page.get_by_test_id("thumbnail")).to_have_count(config.PAGE_SIZE + 3)
