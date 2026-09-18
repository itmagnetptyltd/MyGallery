"""REQ-GAL-008 — a Photo stays until it is deleted, including across restarts.

The restart criteria are tested by opening a second store against the same
folder. Nothing is cached in memory today, so that is equivalent to a restart
now — and it stops being equivalent the moment a cache appears, which is
exactly when these tests start earning their place.
"""

from tests.conftest import an_image


def _reopen():
    """A fresh store over the same folder — what a restart amounts to."""
    from mygallery.photos.store import PhotoStore

    return PhotoStore.open()


# @covers REQ-GAL-008@v1
def test_a_photo_is_still_in_the_gallery_later_in_the_same_run(store):
    saved = store.save(filename="one.jpg", content=an_image("JPEG"))

    assert store.get(saved.id) is not None


# @covers REQ-GAL-008@v1
def test_deleting_one_photo_leaves_the_other_in_the_gallery(store):
    kept = store.save(filename="kept.jpg", content=an_image("JPEG"))
    removed = store.save(filename="removed.jpg", content=an_image("JPEG"))

    store.delete(removed.id)

    assert [p.id for p in store.all()] == [kept.id]


# @covers REQ-GAL-008@v1
def test_a_photo_is_still_in_the_gallery_when_the_store_is_reopened(store):
    saved = store.save(filename="one.jpg", content=an_image("JPEG"))

    assert _reopen().get(saved.id) is not None


# @covers REQ-GAL-008@v1
def test_a_photo_is_present_in_the_storage_folder_as_a_readable_file(store, gallery_dir):
    saved = store.save(filename="one.jpg", content=an_image("JPEG"))

    stored = list((gallery_dir / "photos").glob(f"{saved.id}.*"))

    assert len(stored) == 1 and stored[0].is_file()


# @covers REQ-GAL-008@v1
def test_the_stored_file_holds_the_bytes_that_were_uploaded(store, gallery_dir):
    content = an_image("JPEG")
    saved = store.save(filename="one.jpg", content=content)

    stored = next((gallery_dir / "photos").glob(f"{saved.id}.*"))

    assert stored.read_bytes() == content


# @covers REQ-GAL-008@v1
def test_a_deleted_photo_is_still_gone_when_the_store_is_reopened(store):
    saved = store.save(filename="one.jpg", content=an_image("JPEG"))
    store.delete(saved.id)

    assert _reopen().get(saved.id) is None
