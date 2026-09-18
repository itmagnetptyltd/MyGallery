"""REQ-GAL-005 — deleting a Photo.

ADR-0004 puts a Photo in three places: the file, its Thumbnail, and a row in
the index. Criterion 6 says none of them may be retained, so all three are
checked here rather than trusting that removing the row is enough.
"""

import pytest
from tests.conftest import an_image


# @covers REQ-GAL-005@v1
def test_deleting_a_photo_removes_it_from_the_gallery(store):
    saved = store.save(filename="one.jpg", content=an_image("JPEG"))

    store.delete(saved.id)

    assert store.get(saved.id) is None


# @covers REQ-GAL-005@v1
def test_deleting_a_photo_leaves_the_other_photos(store):
    first = store.save(filename="first.jpg", content=an_image("JPEG"))
    second = store.save(filename="second.jpg", content=an_image("JPEG"))
    third = store.save(filename="third.jpg", content=an_image("JPEG"))

    store.delete(second.id)

    assert {p.id for p in store.all()} == {first.id, third.id}


# @covers REQ-GAL-005@v1
def test_deleting_a_photo_removes_its_file_from_disk(store):
    saved = store.save(filename="one.jpg", content=an_image("JPEG"))
    path = store.path_for(saved.id)

    store.delete(saved.id)

    assert not path.exists()


# @covers REQ-GAL-005@v1
def test_deleting_a_photo_removes_its_thumbnail_from_disk(store, gallery_dir):
    saved = store.save(filename="one.jpg", content=an_image("JPEG"))
    assert store.thumbnail_bytes(saved.id)

    store.delete(saved.id)

    assert list((gallery_dir / "thumbnails").glob(f"{saved.id}.*")) == []


def test_deleting_a_photo_that_is_not_there_is_refused(store):
    with pytest.raises(KeyError):
        store.delete("does-not-exist")
