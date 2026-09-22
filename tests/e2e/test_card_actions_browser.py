"""Belt B — REQ-GAL-003@v4: Download and Delete on every Thumbnail card.

No `wait_for_function`: the application sets `default-src 'self'`, which
refuses the in-page eval it needs. See
constraints/csp-blocks-playwright-wait-for-function.md.
"""

import pytest
from playwright.sync_api import expect
from tests.conftest import an_image, upload_files

CONFIRMATION = "Are you sure you want to delete this photo?"


@pytest.fixture
def gallery_url(running_server) -> str:
    return f"http://{running_server.host}:{running_server.port}"


def _upload(page, tmp_path, names: list[str]) -> dict[str, bytes]:
    contents = {}
    for name in names:
        content = an_image("JPEG", size=(900, 700))
        (tmp_path / name).write_bytes(content)
        contents[name] = content
    upload_files(page, [str(tmp_path / name) for name in names])
    expect(page.get_by_test_id("thumbnail-card")).to_have_count(len(names))
    return contents


def _card(page, filename: str):
    return page.get_by_test_id("thumbnail-card").filter(
        has=page.locator(f'[data-filename="{filename}"]')
    )


# @covers REQ-GAL-003@v4
# @covers REQ-GAL-012@v3
def test_every_card_shows_download_and_delete_without_hovering(
    page, gallery_url, tmp_path
):
    page.goto(gallery_url)
    _upload(page, tmp_path, ["a.jpg", "b.jpg"])
    page.mouse.move(0, 0)

    expect(page.get_by_test_id("card-download")).to_have_count(2)
    expect(page.get_by_test_id("card-delete")).to_have_count(2)
    card = _card(page, "a.jpg")
    expect(card.get_by_test_id("card-download")).to_be_visible()
    expect(card.get_by_test_id("card-delete")).to_be_visible()
    image = card.get_by_test_id("thumbnail").bounding_box()
    download = card.get_by_test_id("card-download").bounding_box()
    assert image is not None and download is not None
    assert download["y"] >= image["y"] + image["height"]


# @covers REQ-GAL-003@v4
# @covers REQ-GAL-012@v3
def test_a_cards_download_and_delete_are_the_same_width(page, gallery_url, tmp_path):
    page.goto(gallery_url)
    _upload(page, tmp_path, ["a.jpg"])

    download = page.get_by_test_id("card-download").bounding_box()
    delete = page.get_by_test_id("card-delete").bounding_box()

    assert download is not None and delete is not None
    assert download["width"] == pytest.approx(delete["width"], abs=1)


# @covers REQ-GAL-003@v4
def test_downloading_from_a_card_delivers_that_photo_without_the_larger_view(
    page, gallery_url, tmp_path
):
    page.goto(gallery_url)
    contents = _upload(page, tmp_path, ["IMG_1234.jpg", "other.jpg"])

    with page.expect_download() as download_info:
        _card(page, "IMG_1234.jpg").get_by_test_id("card-download").click()

    download = download_info.value
    assert download.suggested_filename == "IMG_1234.jpg"
    download.save_as(tmp_path / "got.jpg")
    assert (tmp_path / "got.jpg").read_bytes() == contents["IMG_1234.jpg"]
    expect(page.get_by_test_id("larger-view")).to_be_hidden()


# @covers REQ-GAL-003@v4
def test_deleting_from_a_card_asks_first_without_the_larger_view(
    page, gallery_url, tmp_path
):
    page.goto(gallery_url)
    _upload(page, tmp_path, ["a.jpg"])

    page.get_by_test_id("card-delete").click()

    expect(page.get_by_text(CONFIRMATION)).to_be_visible()
    expect(page.get_by_test_id("larger-view")).to_be_hidden()


# @covers REQ-GAL-003@v4
def test_declining_a_delete_from_a_card_keeps_the_photo(page, gallery_url, tmp_path):
    page.goto(gallery_url)
    _upload(page, tmp_path, ["a.jpg"])
    page.get_by_test_id("card-delete").click()

    page.get_by_test_id("delete-decline").click()

    expect(page.get_by_test_id("thumbnail-card")).to_have_count(1)


# @covers REQ-GAL-003@v4
def test_confirming_a_delete_from_a_card_removes_that_card(page, gallery_url, tmp_path):
    page.goto(gallery_url)
    _upload(page, tmp_path, ["keep.jpg", "gone.jpg"])
    _card(page, "gone.jpg").get_by_test_id("card-delete").click()

    page.get_by_test_id("delete-confirm").click()

    expect(page.get_by_test_id("thumbnail-card")).to_have_count(1)
    expect(_card(page, "gone.jpg")).to_have_count(0)
    expect(_card(page, "keep.jpg")).to_have_count(1)
