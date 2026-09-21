"""Belt B — previews, the description field, dropping files, and alt text.

Everything REQ-GAL-001@v3 added to the Upload popup is a browser behaviour,
so this is the belt that actually exercises it. REQ-GAL-003@v3 criteria 9 and
10 are here too: alt text only exists in a rendered document.
"""

import base64

import pytest
from playwright.sync_api import expect
from tests.conftest import a_coloured_image, an_image, upload_files


@pytest.fixture
def gallery_url(running_server) -> str:
    return f"http://{running_server.host}:{running_server.port}"


def _a_photo(tmp_path, name="holiday.jpg"):
    path = tmp_path / name
    path.write_bytes(an_image("JPEG"))
    return str(path)


def _drop_onto(page, testid: str, name: str, content: bytes) -> None:
    """Drop a real File onto an element, the way a person drags from Explorer.

    Playwright has no drag-from-desktop, so the File and the DataTransfer are
    built in the page and dispatched as a genuine drop event.
    """
    page.evaluate(
        """([selector, name, b64]) => {
            const binary = atob(b64);
            const bytes = new Uint8Array(binary.length);
            for (let i = 0; i < binary.length; i += 1) {
                bytes[i] = binary.charCodeAt(i);
            }
            const file = new File([bytes], name, { type: 'image/jpeg' });
            const transfer = new DataTransfer();
            transfer.items.add(file);
            const target = document.querySelector(selector);
            target.dispatchEvent(
                new DragEvent('drop', {
                    dataTransfer: transfer,
                    bubbles: true,
                    cancelable: true,
                }),
            );
        }""",
        [f'[data-testid="{testid}"]', name, base64.b64encode(content).decode()],
    )


# @covers REQ-GAL-001@v3
# @covers REQ-GAL-015@v2
def test_choosing_a_file_shows_a_preview_image_before_the_upload_is_made(
    page, gallery_url, tmp_path
):
    page.goto(gallery_url)
    page.get_by_test_id("upload-open").click()

    page.get_by_test_id("upload-input").set_input_files(_a_photo(tmp_path))

    expect(page.get_by_test_id("upload-preview")).to_have_count(1)
    expect(page.get_by_test_id("photo-count")).to_have_text("0")


# @covers REQ-GAL-001@v3
# @covers REQ-GAL-015@v2
def test_choosing_thirty_files_shows_a_preview_for_every_one(page, gallery_url, tmp_path):
    photos = [_a_photo(tmp_path, f"p{n}.jpg") for n in range(30)]
    page.goto(gallery_url)
    page.get_by_test_id("upload-open").click()

    page.get_by_test_id("upload-input").set_input_files(photos)

    expect(page.get_by_test_id("upload-preview")).to_have_count(30)


# @covers REQ-GAL-001@v3
# @covers REQ-GAL-017@v1
def test_a_description_given_with_the_upload_reaches_the_gallery(page, gallery_url, tmp_path):
    page.goto(gallery_url)
    page.get_by_test_id("upload-open").click()
    page.get_by_test_id("upload-input").set_input_files(_a_photo(tmp_path))

    page.get_by_test_id("upload-description").fill("Beach at dawn")
    page.get_by_test_id("upload-submit").click()

    expect(page.get_by_test_id("thumbnail")).to_have_attribute("alt", "Beach at dawn")


# @covers REQ-GAL-001@v3
# @covers REQ-GAL-017@v1
def test_an_upload_with_no_description_still_adds_the_photo(page, gallery_url, tmp_path):
    page.goto(gallery_url)

    upload_files(page, _a_photo(tmp_path))

    expect(page.get_by_test_id("photo-count")).to_have_text("1")


# @covers REQ-GAL-001@v3
# @covers REQ-GAL-017@v1
def test_the_description_field_holds_250_characters_and_the_upload_is_not_refused(
    page, gallery_url, tmp_path
):
    page.goto(gallery_url)
    page.get_by_test_id("upload-open").click()
    page.get_by_test_id("upload-input").set_input_files(_a_photo(tmp_path))

    page.get_by_test_id("upload-description").type("y" * 300, delay=0)
    page.get_by_test_id("upload-submit").click()

    expect(page.get_by_test_id("photo-count")).to_have_text("1")
    expect(page.get_by_test_id("thumbnail")).to_have_attribute("alt", "y" * 250)


# @covers REQ-GAL-001@v3
# @covers REQ-GAL-016@v1
def test_dropping_files_on_the_popup_chooses_them_for_the_upload(page, gallery_url):
    page.goto(gallery_url)
    page.get_by_test_id("upload-open").click()

    _drop_onto(page, "upload-popup", "dropped.jpg", an_image("JPEG"))

    expect(page.get_by_test_id("upload-preview")).to_have_count(1)
    page.get_by_test_id("upload-submit").click()
    expect(page.get_by_test_id("photo-count")).to_have_text("1")


# @covers REQ-GAL-003@v3
# @covers REQ-GAL-018@v1
def test_a_thumbnail_carries_its_photos_description_as_alt_text(page, gallery_url, tmp_path):
    page.goto(gallery_url)
    page.get_by_test_id("upload-open").click()
    page.get_by_test_id("upload-input").set_input_files(_a_photo(tmp_path))
    page.get_by_test_id("upload-description").fill("Beach at dawn")
    page.get_by_test_id("upload-submit").click()

    expect(page.get_by_test_id("thumbnail")).to_have_attribute("alt", "Beach at dawn")


# @covers REQ-GAL-003@v3
# @covers REQ-GAL-018@v1
def test_a_thumbnail_with_no_description_carries_its_filename_as_alt_text(
    page, gallery_url, tmp_path
):
    page.goto(gallery_url)

    upload_files(page, _a_photo(tmp_path, "seaside.jpg"))

    expect(page.get_by_test_id("thumbnail")).to_have_attribute("alt", "seaside.jpg")


# @covers REQ-GAL-002@v2
# @covers REQ-GAL-017@v1
# @covers REQ-GAL-018@v1
def test_a_description_is_changed_in_the_larger_view(page, gallery_url, tmp_path):
    page.goto(gallery_url)
    upload_files(page, _a_photo(tmp_path))
    page.get_by_test_id("thumbnail").first.click()

    page.get_by_test_id("larger-view-description").fill("Changed here")
    page.get_by_test_id("description-save").click()

    expect(page.get_by_test_id("thumbnail")).to_have_attribute("alt", "Changed here")


# @covers REQ-GAL-017@v1
def test_typing_one_character_shows_one_of_two_hundred_and_fifty(page, gallery_url):
    page.goto(gallery_url)
    page.get_by_test_id("upload-open").click()

    page.get_by_test_id("upload-description").type("x", delay=0)

    expect(page.get_by_test_id("description-count")).to_have_text("1/250")


# @covers REQ-GAL-017@v1
def test_typing_a_forty_first_character_shows_forty_one_of_two_hundred_and_fifty(
    page, gallery_url
):
    page.goto(gallery_url)
    page.get_by_test_id("upload-open").click()
    page.get_by_test_id("upload-description").fill("z" * 40)

    page.get_by_test_id("upload-description").type("z", delay=0)

    expect(page.get_by_test_id("description-count")).to_have_text("41/250")


# @covers REQ-GAL-015@v2
def test_each_preview_renders_its_own_file(page, gallery_url, tmp_path):
    """REQ-GAL-015 c2.

    Two previews having different sources proves only that they differ. The
    criterion is that each renders *its own* file, so each preview is drawn to
    a canvas and its colour read back and matched to the file it came from.
    """
    red = tmp_path / "red.png"
    red.write_bytes(a_coloured_image((220, 20, 20)))
    blue = tmp_path / "blue.png"
    blue.write_bytes(a_coloured_image((20, 20, 220)))
    page.goto(gallery_url)
    page.get_by_test_id("upload-open").click()

    page.get_by_test_id("upload-input").set_input_files([str(red), str(blue)])

    expect(page.get_by_test_id("upload-preview")).to_have_count(2)
    colours = page.get_by_test_id("upload-preview").locator("img").evaluate_all(
        """async images => Promise.all(images.map(async (image) => {
            // The preview is a blob: URL and may not have decoded yet.
            // Waiting on decode() beats a sleep, which is how a suite
            // becomes slow and flaky at the same time.
            await image.decode();
            const canvas = document.createElement('canvas');
            canvas.width = 1;
            canvas.height = 1;
            const context = canvas.getContext('2d');
            context.drawImage(image, 0, 0, 1, 1);
            const [r, g, b] = context.getImageData(0, 0, 1, 1).data;
            return r > b ? 'red' : 'blue';
        }))"""
    )

    assert colours == ["red", "blue"]
