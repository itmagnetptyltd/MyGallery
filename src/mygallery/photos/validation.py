"""Deciding whether uploaded content is a Photo.

REQ-GAL-010 requires this to read the **content**, never the extension: a file
renamed to `.jpg` is still refused. Pillow reports the real format, which is
the only thing consulted here.
"""

from dataclasses import dataclass
from enum import Enum
from io import BytesIO

from PIL import Image, UnidentifiedImageError

from mygallery import config


class RefusalReason(Enum):
    """Why an upload was refused, in words the user is shown."""

    UNSUPPORTED_TYPE = "not a supported image type"
    TOO_LARGE = "file is too large"

    def message(self) -> str:
        if self is RefusalReason.TOO_LARGE:
            megabytes = config.MAX_PHOTO_BYTES // (1024 * 1024)
            return f"{self.value} (max {megabytes} MB)"
        return self.value


@dataclass(frozen=True)
class ValidationResult:
    accepted: bool
    image_format: str | None = None
    reason: RefusalReason | None = None


def validate_upload(filename: str, content: bytes) -> ValidationResult:
    """Decide whether these bytes may become a Photo.

    `filename` is accepted for symmetry with the caller and is deliberately
    **not consulted**. Judging an upload by its name is the defect REQ-GAL-010
    exists to prevent.
    """
    if len(content) > config.MAX_PHOTO_BYTES:
        return ValidationResult(accepted=False, reason=RefusalReason.TOO_LARGE)

    image_format = _format_of(content)
    if image_format not in config.ACCEPTED_FORMATS:
        return ValidationResult(accepted=False, reason=RefusalReason.UNSUPPORTED_TYPE)

    return ValidationResult(accepted=True, image_format=image_format)


def _format_of(content: bytes) -> str | None:
    try:
        with Image.open(BytesIO(content)) as image:
            image.verify()
            return image.format
    except (UnidentifiedImageError, OSError, ValueError):
        return None
