"""Identifiers for Photos.

REQ-GAL-002: the application issues the identifier. The caller's filename is
neither unique nor trusted, so it is stored as data and never used to name a
file on disk.
"""

import uuid


def new_photo_id() -> str:
    """A fresh identifier, unique and safe to use as a filename."""
    return uuid.uuid4().hex
