"""REQ-GAL-010 and the format/size criteria of REQ-GAL-001.

Validation reads the bytes, never the filename. That is what makes the
renamed-file criterion pass, and it is why every fixture here is a real
encoded image rather than a placeholder.
"""

import pytest
from tests.conftest import an_image

from mygallery.photos.validation import RefusalReason, validate_upload


# @covers REQ-GAL-001@v3
@pytest.mark.parametrize("fmt", ["JPEG", "PNG", "GIF", "WEBP"])
def test_each_accepted_image_format_is_accepted(fmt):
    result = validate_upload(filename=f"holiday.{fmt.lower()}", content=an_image(fmt))

    assert result.accepted


# @covers REQ-GAL-010@v1
def test_content_that_is_not_an_image_is_refused():
    result = validate_upload(filename="notes.txt", content=b"this is not an image")

    assert not result.accepted


# @covers REQ-GAL-010@v1
def test_content_renamed_to_an_accepted_extension_is_still_refused():
    result = validate_upload(filename="sneaky.jpg", content=b"this is not an image")

    assert not result.accepted


# @covers REQ-GAL-010@v1
def test_a_file_in_an_unaccepted_image_format_is_refused():
    # BMP is a real image Pillow can read, and is not on the accepted list —
    # so this fails only because of the allow-list, not because decoding failed.
    result = validate_upload(filename="scan.bmp", content=an_image("BMP"))

    assert not result.accepted


# @covers REQ-GAL-010@v1
def test_the_reason_for_an_unsupported_type_says_so():
    result = validate_upload(filename="notes.txt", content=b"this is not an image")

    assert result.reason is RefusalReason.UNSUPPORTED_TYPE


# @covers REQ-GAL-001@v3
def test_a_file_at_the_size_limit_is_accepted():
    from mygallery import config

    content = an_image("PNG")
    padded = content + b"\0" * (config.MAX_PHOTO_BYTES - len(content))

    result = validate_upload(filename="big.png", content=padded)

    assert result.accepted


# @covers REQ-GAL-001@v3
def test_a_file_over_the_size_limit_is_refused():
    from mygallery import config

    content = an_image("PNG")
    oversized = content + b"\0" * (config.MAX_PHOTO_BYTES + 1 - len(content))

    result = validate_upload(filename="huge.png", content=oversized)

    assert not result.accepted


# @covers REQ-GAL-001@v3
def test_the_reason_for_an_oversized_file_names_the_size():
    from mygallery import config

    oversized = an_image("PNG") + b"\0" * config.MAX_PHOTO_BYTES

    result = validate_upload(filename="huge.png", content=oversized)

    assert result.reason is RefusalReason.TOO_LARGE
