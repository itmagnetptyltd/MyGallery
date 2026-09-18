"""REQ-GAL-003 ordering and paging, and REQ-GAL-007's empty Gallery."""

import pytest
from tests.conftest import an_image


def _fill(store, count: int) -> None:
    for n in range(count):
        store.save(filename=f"p{n}.jpg", content=an_image("JPEG"))


# --- REQ-GAL-003: order and paging -------------------------------------------


# @covers REQ-GAL-003@v1
def test_photos_are_listed_with_the_most_recently_uploaded_first(store):
    first = store.save(filename="first.jpg", content=an_image("JPEG"))
    second = store.save(filename="second.jpg", content=an_image("JPEG"))
    third = store.save(filename="third.jpg", content=an_image("JPEG"))

    assert [p.id for p in store.all()] == [third.id, second.id, first.id]


# @covers REQ-GAL-003@v1
def test_a_page_holds_no_more_than_the_page_size(store):
    _fill(store, 5)

    assert len(store.page(limit=2).photos) == 2


# @covers REQ-GAL-003@v1
def test_a_page_of_a_long_gallery_is_not_the_whole_gallery(store):
    from mygallery import config

    _fill(store, config.PAGE_SIZE + 3)

    assert len(store.page().photos) == config.PAGE_SIZE


# @covers REQ-GAL-003@v1
def test_the_next_page_continues_where_the_previous_one_ended(store):
    _fill(store, 5)
    first_page = store.page(limit=2)

    second_page = store.page(limit=2, after=first_page.next_cursor)

    assert [p.id for p in second_page.photos] == [p.id for p in store.all()[2:4]]


# @covers REQ-GAL-003@v1
def test_a_page_reports_no_cursor_once_the_gallery_is_exhausted(store):
    _fill(store, 2)

    assert store.page(limit=5).next_cursor is None


# --- REQ-GAL-007: the empty Gallery ------------------------------------------


# @covers REQ-GAL-007@v1
def test_an_empty_gallery_holds_no_photos(store):
    assert store.all() == []


# @covers REQ-GAL-007@v1
def test_reading_an_empty_gallery_raises_no_error(store):
    store.page()  # must not raise


# @covers REQ-GAL-007@v1
def test_a_gallery_that_cannot_be_read_reports_a_failure(gallery_dir):
    # A directory where the index file belongs. sqlite cannot open it, which is
    # what a corrupt or locked index looks like from here.
    from mygallery import config
    from mygallery.photos.store import GalleryUnreadable, PhotoStore

    config.GALLERY_DIR.mkdir(parents=True, exist_ok=True)
    config.INDEX_PATH.mkdir(parents=True, exist_ok=True)

    with pytest.raises(GalleryUnreadable):
        PhotoStore.open().page()
