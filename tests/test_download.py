"""REQ-GAL-006 — what a downloaded Photo is called.

Criterion 4 requires the caller's own filename back. That string is untrusted
input kept since Upload, so criterion 5's fallback is what stops an unusable
or dangerous one reaching a Content-Disposition header.

This is a pure function on purpose: every branch is reachable without an HTTP
request, and the rule can be read in one place.
"""

import pytest

from mygallery.photos.download import download_name

PHOTO_ID = "a3f2b1c4d5e6f70819a2b3c4d5e6f708"


# @covers REQ-GAL-006@v1
def test_a_usable_filename_is_delivered_unchanged():
    assert download_name("IMG_1234.jpg", "JPEG", PHOTO_ID) == "IMG_1234.jpg"


# @covers REQ-GAL-006@v1
def test_an_empty_filename_falls_back_to_the_identifier():
    assert download_name("", "JPEG", PHOTO_ID) == f"{PHOTO_ID}.jpg"


# @covers REQ-GAL-006@v1
def test_a_filename_of_only_spaces_falls_back():
    assert download_name("   ", "JPEG", PHOTO_ID) == f"{PHOTO_ID}.jpg"


# @covers REQ-GAL-006@v1
@pytest.mark.parametrize(
    "unusable",
    ["holidays/photo.jpg", r"holidays\photo.jpg", "../photo.jpg", ".."],
)
def test_a_filename_containing_a_path_is_refused(unusable):
    assert download_name(unusable, "JPEG", PHOTO_ID) == f"{PHOTO_ID}.jpg"


# @covers REQ-GAL-006@v1
@pytest.mark.parametrize(
    "injected",
    ["photo\r\nX-Evil: yes.jpg", "photo\nX-Evil: yes.jpg", "photo\x00.jpg"],
)
def test_a_filename_containing_a_control_character_is_refused(injected):
    # Header injection. Werkzeug escapes the value too, but a name that could
    # only have been sent to break a header has no business being echoed back.
    assert download_name(injected, "JPEG", PHOTO_ID) == f"{PHOTO_ID}.jpg"


# @covers REQ-GAL-006@v1
@pytest.mark.parametrize(
    ("image_format", "extension"),
    [("JPEG", ".jpg"), ("PNG", ".png"), ("GIF", ".gif"), ("WEBP", ".webp")],
)
def test_a_fallback_name_ends_in_the_extension_for_the_format(image_format, extension):
    assert download_name("", image_format, PHOTO_ID).endswith(extension)
