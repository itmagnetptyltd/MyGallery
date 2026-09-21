"""Belt A — a Photo carries an optional description.

REQ-GAL-001@v3 added a description to the Upload; REQ-GAL-002@v2 made it
something a Photo carries. The client's words were "a description of max 250
char can given (not mandatory)", so the absent case is as much the behaviour
as the present one.
"""

from tests.conftest import an_image


# @covers REQ-GAL-002@v2
def test_a_photo_uploaded_with_a_description_carries_it(store):
    photo = store.save("holiday.jpg", an_image(), "JPEG", description="Beach at dawn")

    assert store.get(photo.id).description == "Beach at dawn"


# @covers REQ-GAL-002@v2
def test_a_photo_uploaded_with_no_description_carries_none_and_is_still_a_photo(store):
    photo = store.save("holiday.jpg", an_image(), "JPEG")

    stored = store.get(photo.id)
    assert stored is not None
    assert stored.description is None


# @covers REQ-GAL-002@v2
def test_changing_a_description_replaces_it_and_leaves_the_photo_itself_unchanged(store):
    photo = store.save("holiday.jpg", an_image(), "JPEG", description="first")
    bytes_before = store.read_bytes(photo.id)

    store.set_description(photo.id, "second")

    assert store.get(photo.id).description == "second"
    assert store.read_bytes(photo.id) == bytes_before


# @covers REQ-GAL-002@v2
def test_a_photo_carrying_no_description_can_be_given_one(store):
    photo = store.save("holiday.jpg", an_image(), "JPEG")

    store.set_description(photo.id, "given later")

    assert store.get(photo.id).description == "given later"


# @covers REQ-GAL-002@v2
def test_changing_the_description_of_a_photo_that_is_not_there_is_refused(store):
    try:
        store.set_description("not-a-photo", "anything")
    except KeyError:
        return
    raise AssertionError("expected KeyError for an identifier not in the Gallery")


# @covers REQ-GAL-001@v3
def test_an_upload_with_no_description_still_becomes_a_photo(store):
    photo = store.save("holiday.jpg", an_image(), "JPEG", description=None)

    assert store.get(photo.id) is not None


# @covers REQ-GAL-001@v3
def test_a_description_of_250_characters_is_carried_whole(store):
    text = "x" * 250

    photo = store.save("holiday.jpg", an_image(), "JPEG", description=text)

    assert store.get(photo.id).description == text


# @covers REQ-GAL-001@v3
def test_a_photo_listed_in_a_page_carries_its_description(store):
    store.save("holiday.jpg", an_image(), "JPEG", description="Beach at dawn")

    page = store.page()

    assert page.photos[0].description == "Beach at dawn"


# @covers REQ-GAL-002@v2
def test_a_gallery_written_before_descriptions_existed_is_still_readable(gallery_dir):
    """The index the client already has on disk has no description column.

    ADR-0004's index is created with CREATE TABLE IF NOT EXISTS, which will
    not add a column to a table that already exists. Without a migration the
    Gallery stops being readable the moment this feature ships.
    """
    import sqlite3

    from mygallery import config
    from mygallery.photos.store import PhotoStore

    gallery_dir.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(config.INDEX_PATH) as connection:
        connection.execute(
            "CREATE TABLE photos ("
            " id TEXT PRIMARY KEY, filename TEXT NOT NULL, format TEXT NOT NULL,"
            " byte_size INTEGER NOT NULL, uploaded_at TEXT NOT NULL,"
            " sequence INTEGER NOT NULL)"
        )
        connection.execute(
            "INSERT INTO photos VALUES"
            " ('old1', 'before.jpg', 'JPEG', 10, '2026-01-01T00:00:00+00:00', 1)"
        )

    store = PhotoStore.open()

    assert store.get("old1").description is None
