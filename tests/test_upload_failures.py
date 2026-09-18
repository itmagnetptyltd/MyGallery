"""REQ-GAL-009 — an Upload that does not finish leaves nothing behind.

Criteria 1 and 2: a save that throws after the Photo bytes hit disk must
not publish a Photo and must not leave those bytes, a Thumbnail, or a
temp file. Criterion 6's wording is pinned here so the page can only
show what validation already decided.
"""

import pytest
from tests.conftest import an_image

from mygallery.photos.store import PhotoStore
from mygallery.photos.validation import RefusalReason


def _fail_during_thumbnail(monkeypatch):
    from mygallery.photos import store as store_module

    monkeypatch.setattr(
        store_module.thumbnails,
        "render",
        lambda _content: (_ for _ in ()).throw(OSError("disk full")),
    )


def _files_under(directory):
    if not directory.exists():
        return []
    return [path for path in directory.iterdir() if path.is_file()]


# @covers REQ-GAL-009@v1
def test_an_interrupted_save_adds_no_photo(store, monkeypatch):
    _fail_during_thumbnail(monkeypatch)

    with pytest.raises(OSError):
        store.save(filename="holiday.jpg", content=an_image("JPEG"))

    assert store.all() == []


# @covers REQ-GAL-009@v1
def test_an_interrupted_save_leaves_no_photo_file(store, gallery_dir, monkeypatch):
    _fail_during_thumbnail(monkeypatch)

    with pytest.raises(OSError):
        store.save(filename="holiday.jpg", content=an_image("JPEG"))

    assert _files_under(gallery_dir / "photos") == []


# @covers REQ-GAL-009@v1
def test_an_interrupted_save_leaves_no_thumbnail(store, gallery_dir, monkeypatch):
    _fail_during_thumbnail(monkeypatch)

    with pytest.raises(OSError):
        store.save(filename="holiday.jpg", content=an_image("JPEG"))

    assert _files_under(gallery_dir / "thumbnails") == []


# @covers REQ-GAL-009@v1
def test_an_interrupted_save_leaves_no_temp_file(store, gallery_dir, monkeypatch):
    _fail_during_thumbnail(monkeypatch)

    with pytest.raises(OSError):
        store.save(filename="holiday.jpg", content=an_image("JPEG"))

    leftovers = [
        path
        for directory in (gallery_dir / "photos", gallery_dir / "thumbnails")
        for path in _files_under(directory)
        if path.name.endswith(".tmp")
    ]
    assert leftovers == []


# @covers REQ-GAL-009@v1
def test_opening_the_store_removes_a_file_that_has_no_row(gallery_dir):
    photos = gallery_dir / "photos"
    photos.mkdir(parents=True)
    orphan = photos / "leftover.jpg"
    orphan.write_bytes(an_image("JPEG"))

    PhotoStore.open()

    assert not orphan.exists()


# @covers REQ-GAL-009@v1
def test_the_too_large_reason_names_the_25_mb_limit():
    assert RefusalReason.TOO_LARGE.message() == "file is too large (max 25 MB)"
