"""Thumbnails.

REQ-GAL-003: the client uploads large phone photos and asked the Gallery to
stay fast, so a Thumbnail is a separately stored smaller rendering rather than
the Photo displayed small.
"""

from io import BytesIO

from PIL import Image

# Longest edge, in pixels. Big enough to look right on a high-density screen,
# small enough that a Gallery of them loads quickly.
THUMBNAIL_EDGE = 320
THUMBNAIL_FORMAT = "JPEG"
THUMBNAIL_EXTENSION = ".jpg"
THUMBNAIL_MEDIA_TYPE = "image/jpeg"


def render(content: bytes) -> bytes:
    """A Thumbnail of these Photo bytes."""
    with Image.open(BytesIO(content)) as image:
        thumbnail = image.convert("RGB")
        thumbnail.thumbnail((THUMBNAIL_EDGE, THUMBNAIL_EDGE))
        buffer = BytesIO()
        thumbnail.save(buffer, format=THUMBNAIL_FORMAT, quality=80)
        return buffer.getvalue()
