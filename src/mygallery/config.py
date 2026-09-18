"""Where the application listens, and where Photos live.

Read these through the module (`config.PHOTO_DIR`), never by importing the
name directly — tests repoint them, and a direct import captures the value at
import time.
"""

import os
from pathlib import Path

# --- where the application listens -------------------------------------------
#
# HOST is loopback deliberately: REQ-GAL-011 requires that a connection from
# another device on the network is refused, and binding to 127.0.0.1 is what
# makes that true without the client configuring a firewall. Do not change it
# to 0.0.0.0.

HOST = "127.0.0.1"
PORT = 8765

# --- where Photos live --------------------------------------------------------
#
# ADR-0004: a folder the client can find and back up themselves, not AppData.
# REQ-GAL-008 requires the Photos be present there as ordinary copyable files.

GALLERY_DIR = Path(os.environ.get("MYGALLERY_DIR", Path.home() / "Pictures" / "MyGallery"))
PHOTO_DIR = GALLERY_DIR / "photos"
THUMBNAIL_DIR = GALLERY_DIR / "thumbnails"
INDEX_PATH = GALLERY_DIR / "index.db"

# --- limits -------------------------------------------------------------------

# REQ-GAL-001: 25 MB per Photo, from the client's answer of 2026-09-18.
MAX_PHOTO_BYTES = 25 * 1024 * 1024

# REQ-GAL-001 allows a batch; MAX_CONTENT_LENGTH applies to the whole request,
# so this is the batch ceiling, NOT the per-Photo limit. Setting Flask's limit
# to MAX_PHOTO_BYTES would refuse a legitimate batch of thirty.
MAX_BATCH_PHOTOS = 30
MAX_REQUEST_BYTES = MAX_BATCH_PHOTOS * MAX_PHOTO_BYTES

# REQ-GAL-003: the Gallery loads in parts and grows as the user scrolls. The
# client asked for no numbered pages and gave no page size; this is a judgement
# recorded in the slice 2 plan, not a number they supplied.
PAGE_SIZE = 60

# REQ-GAL-010: the client named these four and asked for everything else to be
# refused rather than guessed at. These are Pillow's own format names.
ACCEPTED_FORMATS = ("JPEG", "PNG", "GIF", "WEBP")
EXTENSION_FOR_FORMAT = {
    "JPEG": ".jpg",
    "PNG": ".png",
    "GIF": ".gif",
    "WEBP": ".webp",
}
