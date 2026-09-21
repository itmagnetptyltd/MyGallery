"""Belt B — the Larger view of a photo smaller than its Thumbnail, and centring.

test_larger_view_browser.py checks REQ-GAL-004 c2 with a 900x700 photo only,
so a small photo shown at its own size - smaller than its Thumbnail - got
through. These measure after decode() so the size is the rendered one.

No wait_for_function: default-src 'self' forbids the in-page eval it needs.
See constraints/csp-blocks-playwright-wait-for-function.md.
"""

import pytest
from playwright.sync_api import expect
from tests.conftest import an_image, upload_files

SMALL_PHOTO = (120, 90)
NARROW_PHOTO = (298, 358)

_MEASURE = """async () => {
  const photo = document.querySelector('[data-testid="larger-view-photo"]');
  await photo.decode();
  const box = photo.getBoundingClientRect();
  const panel = document
    .querySelector('[data-testid="larger-view"]')
    .getBoundingClientRect();
  return {
    width: box.width,
    height: box.height,
    centre: box.left + box.width / 2,
    panelCentre: panel.left + panel.width / 2,
  };
}"""


@pytest.fixture
def gallery_url(running_server) -> str:
    return f"http://{running_server.host}:{running_server.port}"


def _open_one(page, gallery_url, tmp_path, size: tuple[int, int]) -> dict[str, float]:
    photo = tmp_path / "small.jpg"
    photo.write_bytes(an_image("JPEG", size=size))
    page.set_viewport_size({"width": 1280, "height": 800})
    page.goto(gallery_url)
    upload_files(page, str(photo))
    expect(page.get_by_test_id("thumbnail")).to_have_count(1)
    page.get_by_test_id("thumbnail").first.click()
    expect(page.get_by_test_id("larger-view")).to_be_visible()
    return page.evaluate(_MEASURE)


# @covers REQ-GAL-004@v2
def test_a_photo_smaller_than_its_thumbnail_is_still_rendered_larger(page, gallery_url, tmp_path):
    photo = tmp_path / "small.jpg"
    photo.write_bytes(an_image("JPEG", size=SMALL_PHOTO))
    page.set_viewport_size({"width": 1280, "height": 800})
    page.goto(gallery_url)
    upload_files(page, str(photo))
    thumbnail = page.get_by_test_id("thumbnail").first
    expect(thumbnail).to_be_visible()
    thumbnail_box = thumbnail.bounding_box()

    thumbnail.click()
    expect(page.get_by_test_id("larger-view")).to_be_visible()
    measured = page.evaluate(_MEASURE)

    assert thumbnail_box is not None
    assert measured["width"] > thumbnail_box["width"]
    assert measured["height"] > thumbnail_box["height"]


# No criterion covers centring: it was asked for in the developer session of
# 2026-09-21 ("Image in preview not looking good") and built by /fix on the
# developer's instruction. Record it before relying on it.
def test_a_photo_narrower_than_the_panel_is_centred_in_it(page, gallery_url, tmp_path):
    measured = _open_one(page, gallery_url, tmp_path, NARROW_PHOTO)

    assert measured["centre"] == pytest.approx(measured["panelCentre"], abs=1)
