"""Belt B — REQ-GAL-006: downloading from a Thumbnail card, in a real browser.

Download is started from the card (REQ-GAL-003@v4); the Larger view has no
Download since REQ-GAL-004@v3.

No `wait_for_function`: the application sets `default-src 'self'`, which
refuses the in-page eval it needs. See
constraints/csp-blocks-playwright-wait-for-function.md.
"""

import pytest
from playwright.sync_api import expect
from tests.conftest import an_image, upload_files


@pytest.fixture
def gallery_url(running_server) -> str:
    return f"http://{running_server.host}:{running_server.port}"


def _upload(page, tmp_path, name: str) -> bytes:
    content = an_image("JPEG", size=(900, 700))
    photo = tmp_path / name
    photo.write_bytes(content)
    upload_files(page, str(photo))
    expect(page.get_by_test_id("thumbnail")).to_have_count(1)
    return content


# @covers REQ-GAL-006@v1
def test_downloading_from_a_card_delivers_a_file(page, gallery_url, tmp_path):
    page.goto(gallery_url)
    _upload(page, tmp_path, "IMG_1234.jpg")

    with page.expect_download() as download_info:
        page.get_by_test_id("card-download").first.click()

    assert download_info.value is not None


# @covers REQ-GAL-006@v1
def test_the_downloaded_file_is_named_as_it_was_uploaded(page, gallery_url, tmp_path):
    page.goto(gallery_url)
    _upload(page, tmp_path, "IMG_1234.jpg")

    with page.expect_download() as download_info:
        page.get_by_test_id("card-download").first.click()

    assert download_info.value.suggested_filename == "IMG_1234.jpg"


# @covers REQ-GAL-006@v1
def test_the_downloaded_file_holds_the_bytes_that_were_uploaded(
    page, gallery_url, tmp_path
):
    page.goto(gallery_url)
    uploaded = _upload(page, tmp_path, "IMG_1234.jpg")

    with page.expect_download() as download_info:
        page.get_by_test_id("card-download").first.click()

    saved = tmp_path / "downloaded.jpg"
    download_info.value.save_as(str(saved))
    assert saved.read_bytes() == uploaded
