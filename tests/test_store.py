"""REQ-GAL-001 and REQ-GAL-002 — what saving a Photo actually does on disk."""

from tests.conftest import an_image


# @covers REQ-GAL-001@v2
def test_saving_a_photo_puts_it_in_the_gallery(store):
    store.save(filename="one.jpg", content=an_image("JPEG"))

    assert len(store.all()) == 1


# @covers REQ-GAL-001@v2
def test_saving_a_second_photo_leaves_the_first_in_place(store):
    store.save(filename="one.jpg", content=an_image("JPEG"))
    store.save(filename="two.jpg", content=an_image("JPEG"))

    assert len(store.all()) == 2


# @covers REQ-GAL-001@v2
def test_a_saved_photo_can_be_retrieved_afterwards(store):
    saved = store.save(filename="one.jpg", content=an_image("JPEG"))

    assert store.get(saved.id) is not None


# @covers REQ-GAL-001@v2
def test_a_retrieved_photo_carries_the_bytes_that_were_saved(store):
    content = an_image("JPEG")
    saved = store.save(filename="one.jpg", content=content)

    assert store.read_bytes(saved.id) == content


# @covers REQ-GAL-002@v1
def test_two_photos_saved_under_the_same_filename_get_different_identifiers(store):
    first = store.save(filename="IMG_1234.jpg", content=an_image("JPEG"))
    second = store.save(filename="IMG_1234.jpg", content=an_image("JPEG"))

    assert first.id != second.id


# @covers REQ-GAL-002@v1
def test_a_photo_keeps_the_filename_it_was_uploaded_under(store):
    saved = store.save(filename="IMG_1234.jpg", content=an_image("JPEG"))

    assert store.get(saved.id).filename == "IMG_1234.jpg"


# @covers REQ-GAL-002@v1
def test_a_filename_containing_path_separators_stores_inside_the_photo_directory(
    store, gallery_dir
):
    saved = store.save(filename="../../evil.jpg", content=an_image("JPEG"))

    assert (gallery_dir / "photos").resolve() in store.path_for(saved.id).resolve().parents


# @covers REQ-GAL-002@v1
def test_a_filename_containing_a_drive_letter_stores_inside_the_photo_directory(
    store, gallery_dir
):
    saved = store.save(filename=r"C:\windows\system32\evil.jpg", content=an_image("JPEG"))

    assert (gallery_dir / "photos").resolve() in store.path_for(saved.id).resolve().parents
