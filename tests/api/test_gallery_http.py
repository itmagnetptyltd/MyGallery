"""Belt C — REQ-GAL-003 over HTTP: ordering, paging and Thumbnail delivery."""

import io

import pytest
from tests.conftest import a_noisy_image, an_image, dominant_colour

pytestmark = pytest.mark.integration


def _upload(client, count: int) -> None:
    client.post(
        "/api/photos",
        data={
            "photos": [(io.BytesIO(an_image("JPEG")), f"p{n}.jpg") for n in range(count)]
        },
        content_type="multipart/form-data",
    )


# @covers REQ-GAL-003@v1
def test_listing_returns_photos_newest_first(client, gallery_dir):
    _upload(client, 3)

    listed = client.get("/api/photos").get_json()["photos"]

    assert [p["filename"] for p in listed] == ["p2.jpg", "p1.jpg", "p0.jpg"]


# @covers REQ-GAL-003@v1
def test_listing_returns_at_most_one_page(client, gallery_dir):
    from mygallery import config

    _upload(client, config.PAGE_SIZE + 2)

    assert len(client.get("/api/photos").get_json()["photos"]) == config.PAGE_SIZE


# @covers REQ-GAL-003@v1
def test_a_long_gallery_reports_a_cursor_for_the_next_page(client, gallery_dir):
    from mygallery import config

    _upload(client, config.PAGE_SIZE + 2)

    assert client.get("/api/photos").get_json()["nextCursor"] is not None


# @covers REQ-GAL-003@v1
def test_following_the_cursor_returns_the_photos_the_first_page_omitted(client, gallery_dir):
    _upload(client, 4)
    first = client.get("/api/photos?limit=2").get_json()

    second = client.get(f"/api/photos?limit=2&after={first['nextCursor']}").get_json()

    assert [p["filename"] for p in second["photos"]] == ["p1.jpg", "p0.jpg"]


# @covers REQ-GAL-003@v1
def test_requesting_a_thumbnail_returns_an_image(client, gallery_dir):
    _upload(client, 1)
    photo = client.get("/api/photos").get_json()["photos"][0]

    response = client.get(f"/api/photos/{photo['id']}/thumbnail")

    # Asserting the content type, not just a 200: a 404 error page is also
    # "smaller than the Photo", and would pass a naive size check.
    assert response.headers["Content-Type"].startswith("image/")


# @covers REQ-GAL-003@v1
def test_a_delivered_thumbnail_decodes_as_an_image(client, gallery_dir):
    _upload(client, 1)
    photo = client.get("/api/photos").get_json()["photos"][0]

    thumbnail = client.get(f"/api/photos/{photo['id']}/thumbnail")

    assert dominant_colour(thumbnail.data)


# @covers REQ-GAL-003@v1
def test_a_thumbnail_is_delivered_smaller_than_its_photo(client, gallery_dir):
    # The criterion says "a Photo whose stored file is several megabytes". A
    # tiny Photo is outside that precondition: its Thumbnail re-encodes at the
    # same dimensions and can come out the same size or larger. Using a small
    # image here would be asserting something the requirement does not promise.
    client.post(
        "/api/photos",
        data={"photos": [(io.BytesIO(a_noisy_image()), "big.png")]},
        content_type="multipart/form-data",
    )
    photo = client.get("/api/photos").get_json()["photos"][0]

    thumbnail = client.get(f"/api/photos/{photo['id']}/thumbnail")

    assert thumbnail.headers["Content-Type"].startswith("image/")
    assert len(thumbnail.data) < photo["byteSize"]


# @covers REQ-GAL-003@v1
def test_requesting_a_thumbnail_for_an_unknown_photo_is_not_found(client, gallery_dir):
    response = client.get("/api/photos/does-not-exist/thumbnail")

    assert response.status_code == 404
