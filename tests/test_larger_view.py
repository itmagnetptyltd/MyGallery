"""REQ-GAL-004 — serving the Photo the Larger view shows.

The Larger view shows the Photo itself, not an upscaled Thumbnail: upscaling
would satisfy "rendered larger" while showing the user a blurry 320px image.
"""

import io

from tests.conftest import a_noisy_image, an_image


def _upload(client, name: str, content: bytes) -> dict:
    client.post(
        "/api/photos",
        data={"photos": [(io.BytesIO(content), name)]},
        content_type="multipart/form-data",
    )
    return client.get("/api/photos").get_json()["photos"][0]


# @covers REQ-GAL-004@v1
def test_requesting_a_photo_returns_the_bytes_that_were_uploaded(client, gallery_dir):
    content = an_image("JPEG")
    photo = _upload(client, "holiday.jpg", content)

    response = client.get(f"/api/photos/{photo['id']}")

    assert response.data == content


# @covers REQ-GAL-004@v1
def test_requesting_a_photo_returns_it_as_an_image(client, gallery_dir):
    photo = _upload(client, "holiday.jpg", an_image("JPEG"))

    response = client.get(f"/api/photos/{photo['id']}")

    # Content type, not just a 200: a 404 page is also "not the Thumbnail".
    assert response.headers["Content-Type"].startswith("image/")


# @covers REQ-GAL-004@v1
def test_the_photo_served_is_larger_than_its_thumbnail(client, gallery_dir):
    photo = _upload(client, "big.png", a_noisy_image())

    full = client.get(f"/api/photos/{photo['id']}")
    thumbnail = client.get(f"/api/photos/{photo['id']}/thumbnail")

    assert len(full.data) > len(thumbnail.data)


def test_requesting_an_unknown_photo_is_not_found(client, gallery_dir):
    response = client.get("/api/photos/does-not-exist")

    assert response.status_code == 404
