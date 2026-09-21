"""Belt B — REQ-GAL-001 uploaded through a real browser.

The Gallery's own rendering (Thumbnails, ordering, the empty state) is
REQ-GAL-003 and REQ-GAL-007, which are slice 2b. This file covers only what
REQ-GAL-001 asserts: a Photo picked in the browser reaches the Gallery, and
reaching the Gallery needs no sign-in.
"""

import pytest
from playwright.sync_api import expect
from tests.conftest import an_image, upload_files


@pytest.fixture
def gallery_url(running_server) -> str:
    return f"http://{running_server.host}:{running_server.port}"


# @covers REQ-GAL-001@v3
def test_the_gallery_is_shown_without_a_sign_in_step(page, gallery_url):
    page.goto(gallery_url)

    expect(page.get_by_test_id("gallery")).to_be_visible()


# @covers REQ-GAL-001@v3
def test_uploading_a_photo_through_the_browser_adds_it_to_the_gallery(
    page, gallery_url, tmp_path
):
    photo = tmp_path / "holiday.jpg"
    photo.write_bytes(an_image("JPEG"))
    page.goto(gallery_url)

    upload_files(page, str(photo))

    expect(page.get_by_test_id("photo-count")).to_have_text("1")


# @covers REQ-GAL-001@v3
def test_uploading_a_batch_through_the_browser_adds_every_photo(page, gallery_url, tmp_path):
    photos = []
    for n in range(3):
        photo = tmp_path / f"p{n}.jpg"
        photo.write_bytes(an_image("JPEG"))
        photos.append(str(photo))
    page.goto(gallery_url)

    upload_files(page, photos)

    expect(page.get_by_test_id("photo-count")).to_have_text("3")
