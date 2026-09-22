"""Belt B — REQ-GAL-004@v3: the Larger view's actions are Save description and Close.

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


def _upload_and_open(page, tmp_path) -> None:
    photo = tmp_path / "a.jpg"
    photo.write_bytes(an_image("JPEG", size=(900, 700)))
    upload_files(page, str(photo))
    expect(page.get_by_test_id("thumbnail")).to_have_count(1)
    page.get_by_test_id("thumbnail").first.click()
    expect(page.get_by_test_id("larger-view")).to_be_visible()


# @covers REQ-GAL-004@v3
# @covers REQ-GAL-014@v2
def test_the_larger_view_shows_save_description_and_close_side_by_side(
    page, gallery_url, tmp_path
):
    page.goto(gallery_url)
    _upload_and_open(page, tmp_path)

    save = page.get_by_test_id("description-save")
    close = page.get_by_test_id("larger-view-close-button")
    expect(save).to_be_visible()
    expect(close).to_have_text("Close")
    save_box, close_box = save.bounding_box(), close.bounding_box()
    assert save_box is not None and close_box is not None
    assert save_box["y"] == pytest.approx(close_box["y"], abs=1)
    assert save_box["x"] < close_box["x"]
    expect(page.get_by_test_id("larger-view").get_by_test_id("download-photo")).to_have_count(0)
    expect(page.get_by_test_id("larger-view").get_by_test_id("delete-photo")).to_have_count(0)


# @covers REQ-GAL-004@v3
def test_the_close_button_closes_the_larger_view(page, gallery_url, tmp_path):
    page.goto(gallery_url)
    _upload_and_open(page, tmp_path)

    page.get_by_test_id("larger-view-close-button").click()

    expect(page.get_by_test_id("larger-view")).to_be_hidden()
    expect(page.get_by_test_id("thumbnail")).to_be_visible()
