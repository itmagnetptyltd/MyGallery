"""REQ-GAL-003 — Thumbnails.

The client asked for the Gallery to stay fast with large phone photos, which
is why a Thumbnail is a separately stored smaller rendering rather than the
Photo shown small.
"""

from tests.conftest import a_coloured_image, a_noisy_image, dominant_colour


# @covers REQ-GAL-003@v4
def test_a_thumbnail_is_smaller_in_bytes_than_its_photo(store):
    content = a_noisy_image()
    saved = store.save(filename="big.png", content=content, image_format="PNG")

    assert len(store.thumbnail_bytes(saved.id)) < len(content)


# @covers REQ-GAL-003@v4
def test_a_thumbnail_renders_its_own_photo_and_not_another(store):
    red = store.save(
        filename="red.png", content=a_coloured_image((220, 20, 20)), image_format="PNG"
    )
    store.save(
        filename="blue.png", content=a_coloured_image((20, 20, 220)), image_format="PNG"
    )

    red_thumbnail = dominant_colour(store.thumbnail_bytes(red.id))

    assert red_thumbnail[0] > red_thumbnail[2]


# @covers REQ-GAL-003@v4
def test_every_photo_in_the_gallery_has_a_thumbnail(store):
    for n in range(3):
        store.save(
            filename=f"p{n}.png",
            content=a_coloured_image((10 * n, 40, 90)),
            image_format="PNG",
        )

    assert all(store.thumbnail_bytes(photo.id) for photo in store.all())
