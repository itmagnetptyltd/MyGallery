"""Belt B — REQ-GAL-009: failed files named on the page, with a reason.

No `wait_for_function`: the application sets `default-src 'self'`, which
refuses the in-page eval it needs. See
constraints/csp-blocks-playwright-wait-for-function.md.
"""

from playwright.sync_api import expect
from tests.conftest import an_image

from mygallery import config


def _gallery_url(running_server) -> str:
    return f"http://{running_server.host}:{running_server.port}"


def _write_jpeg(path) -> None:
    path.write_bytes(an_image("JPEG"))


def _mixed_thirty(tmp_path) -> list[str]:
    names = []
    for n in range(27):
        photo = tmp_path / f"p{n}.jpg"
        _write_jpeg(photo)
        names.append(str(photo))
    for n in range(3):
        bad = tmp_path / f"bad{n}.txt"
        bad.write_text("not an image", encoding="utf-8")
        names.append(str(bad))
    return names


# @covers REQ-GAL-009@v1
def test_a_batch_with_three_failures_keeps_the_photos_that_worked(
    page, running_server, tmp_path
):
    page.goto(_gallery_url(running_server))

    page.get_by_test_id("upload-input").set_input_files(_mixed_thirty(tmp_path))

    expect(page.get_by_test_id("photo-count")).to_have_text("27")


# @covers REQ-GAL-009@v1
def test_each_failed_file_is_named_on_the_page(page, running_server, tmp_path):
    page.goto(_gallery_url(running_server))

    page.get_by_test_id("upload-input").set_input_files(_mixed_thirty(tmp_path))

    failures = page.get_by_test_id("upload-failure")
    expect(failures).to_have_count(3)
    expect(failures.filter(has_text="bad0.txt")).to_have_count(1)
    expect(failures.filter(has_text="bad1.txt")).to_have_count(1)
    expect(failures.filter(has_text="bad2.txt")).to_have_count(1)


# @covers REQ-GAL-009@v1
def test_each_failure_shows_its_reason_beside_its_name(page, running_server, tmp_path):
    page.goto(_gallery_url(running_server))

    page.get_by_test_id("upload-input").set_input_files(_mixed_thirty(tmp_path))

    for name in ("bad0.txt", "bad1.txt", "bad2.txt"):
        row = page.get_by_test_id("upload-failure").filter(has_text=name)
        expect(row).to_contain_text("not a supported image type")


# @covers REQ-GAL-009@v1
def test_an_oversized_file_names_the_25_mb_limit_on_the_page(
    page, running_server, tmp_path
):
    jpeg = an_image("JPEG")
    huge = tmp_path / "huge.jpg"
    huge.write_bytes(jpeg + b"\0" * (config.MAX_PHOTO_BYTES + 1 - len(jpeg)))
    page.goto(_gallery_url(running_server))

    page.get_by_test_id("upload-input").set_input_files(str(huge))

    expect(page.get_by_test_id("upload-failure")).to_contain_text("25 MB")
    expect(page.get_by_test_id("upload-failure")).to_contain_text("too large")
