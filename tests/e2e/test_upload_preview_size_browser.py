"""Belt B — the size of a chosen file's preview, measured in a real browser.

REQ-GAL-015@v2: a preview is as wide as the description field, keeps its
image's proportions, and is centred when the image is narrower than the field.
Each test waits on the preview's decode() so its size is the rendered one.

No wait_for_function: default-src 'self' forbids the in-page eval it needs.
See constraints/csp-blocks-playwright-wait-for-function.md.
"""

import pytest
from playwright.sync_api import expect
from tests.conftest import an_image

WIDE_IMAGE = (2000, 1200)
NARROW_IMAGE = (200, 150)

_MEASURE = """async () => {
  const image = document.querySelector('[data-testid="upload-preview"] img');
  await image.decode();
  const preview = image.getBoundingClientRect();
  const field = document
    .querySelector('[data-testid="upload-description"]')
    .getBoundingClientRect();
  return {
    previewWidth: preview.width,
    previewHeight: preview.height,
    previewCentre: preview.left + preview.width / 2,
    naturalWidth: image.naturalWidth,
    naturalHeight: image.naturalHeight,
    fieldWidth: field.width,
    fieldCentre: field.left + field.width / 2,
  };
}"""


@pytest.fixture
def gallery_url(running_server) -> str:
    return f"http://{running_server.host}:{running_server.port}"


def _choose_one(page, gallery_url, tmp_path, size: tuple[int, int]) -> dict[str, float]:
    photo = tmp_path / "chosen.jpg"
    photo.write_bytes(an_image("JPEG", size=size))
    page.set_viewport_size({"width": 1280, "height": 800})
    page.goto(gallery_url)
    page.get_by_test_id("upload-open").click()
    page.get_by_test_id("upload-input").set_input_files(str(photo))
    expect(page.get_by_test_id("upload-preview")).to_have_count(1)
    return page.evaluate(_MEASURE)


# @covers REQ-GAL-015@v2
def test_a_wide_preview_is_as_wide_as_the_description_field(page, gallery_url, tmp_path):
    measured = _choose_one(page, gallery_url, tmp_path, WIDE_IMAGE)

    assert measured["previewWidth"] == pytest.approx(measured["fieldWidth"], abs=1)


# @covers REQ-GAL-015@v2
def test_a_preview_keeps_its_images_proportions(page, gallery_url, tmp_path):
    measured = _choose_one(page, gallery_url, tmp_path, WIDE_IMAGE)

    rendered = measured["previewWidth"] / measured["previewHeight"]
    natural = measured["naturalWidth"] / measured["naturalHeight"]
    assert rendered == pytest.approx(natural, rel=0.01)


# @covers REQ-GAL-015@v2
def test_a_narrow_preview_is_centred_in_the_popup(page, gallery_url, tmp_path):
    measured = _choose_one(page, gallery_url, tmp_path, NARROW_IMAGE)

    assert measured["previewWidth"] < measured["fieldWidth"]
    assert measured["previewCentre"] == pytest.approx(measured["fieldCentre"], abs=1)
