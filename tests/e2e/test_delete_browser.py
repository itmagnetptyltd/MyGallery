"""Belt B — REQ-GAL-005: confirming and declining a deletion, in a browser.

No `wait_for_function` anywhere: the application sets
`Content-Security-Policy: default-src 'self'`, which refuses the in-page eval
it needs. See constraints/csp-blocks-playwright-wait-for-function.md.
"""

import pytest
from playwright.sync_api import expect
from tests.conftest import an_image, upload_files

CONFIRMATION = "Are you sure you want to delete this photo?"


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


def _open_first_photo(page) -> None:
    page.get_by_test_id("thumbnail").first.click()
    expect(page.get_by_test_id("larger-view")).to_be_visible()


# @covers REQ-GAL-005@v1
def test_asking_to_delete_a_photo_asks_for_confirmation(page, gallery_url, tmp_path):
    page.goto(gallery_url)
    _upload(page, tmp_path, 1)
    _open_first_photo(page)

    page.get_by_test_id("delete-photo").click()

    expect(page.get_by_test_id("delete-confirmation")).to_be_visible()


# @covers REQ-GAL-005@v1
def test_the_confirmation_asks_are_you_sure_you_want_to_delete_this_photo(
    page, gallery_url, tmp_path
):
    page.goto(gallery_url)
    _upload(page, tmp_path, 1)
    _open_first_photo(page)

    page.get_by_test_id("delete-photo").click()

    # The client gave this wording verbatim; it is a criterion, not a caption.
    expect(page.get_by_test_id("delete-confirmation-question")).to_have_text(CONFIRMATION)


# @covers REQ-GAL-005@v1
def test_declining_the_confirmation_leaves_the_photo_in_the_gallery(
    page, gallery_url, tmp_path
):
    page.goto(gallery_url)
    _upload(page, tmp_path, 1)
    _open_first_photo(page)
    page.get_by_test_id("delete-photo").click()

    page.get_by_test_id("delete-decline").click()

    expect(page.get_by_test_id("thumbnail")).to_have_count(1)


# @covers REQ-GAL-005@v1
def test_confirming_the_deletion_removes_the_thumbnail_from_the_gallery(
    page, gallery_url, tmp_path
):
    page.goto(gallery_url)
    _upload(page, tmp_path, 1)
    _open_first_photo(page)
    page.get_by_test_id("delete-photo").click()

    page.get_by_test_id("delete-confirm").click()

    expect(page.get_by_test_id("thumbnail")).to_have_count(0)


# @covers REQ-GAL-005@v1
def test_confirming_the_deletion_leaves_the_other_thumbnails(page, gallery_url, tmp_path):
    page.goto(gallery_url)
    _upload(page, tmp_path, 3)
    _open_first_photo(page)
    page.get_by_test_id("delete-photo").click()

    page.get_by_test_id("delete-confirm").click()

    expect(page.get_by_test_id("thumbnail")).to_have_count(2)


# @covers REQ-GAL-005@v1
def test_the_larger_view_closes_once_the_photo_is_deleted(page, gallery_url, tmp_path):
    page.goto(gallery_url)
    _upload(page, tmp_path, 2)
    _open_first_photo(page)
    page.get_by_test_id("delete-photo").click()

    page.get_by_test_id("delete-confirm").click()

    expect(page.get_by_test_id("larger-view")).to_be_hidden()
