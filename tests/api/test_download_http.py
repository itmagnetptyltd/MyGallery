"""Belt C — REQ-GAL-006 over HTTP."""

import io

import pytest
from tests.conftest import a_coloured_image, an_image, dominant_colour

pytestmark = pytest.mark.integration


def _upload(client, name: str, content: bytes) -> dict:
    client.post(
        "/api/photos",
        data={"photos": [(io.BytesIO(content), name)]},
        content_type="multipart/form-data",
    )
    return client.get("/api/photos").get_json()["photos"][0]


# @covers REQ-GAL-006@v1
def test_downloading_a_photo_delivers_a_file(client, gallery_dir):
    photo = _upload(client, "holiday.jpg", an_image("JPEG"))

    response = client.get(f"/api/photos/{photo['id']}/download")

    assert response.headers["Content-Disposition"].startswith("attachment")


# @covers REQ-GAL-006@v1
def test_the_delivered_file_is_the_requested_photo(client, gallery_dir):
    _upload(client, "blue.png", a_coloured_image((20, 20, 220)))
    red = _upload(client, "red.png", a_coloured_image((220, 20, 20)))

    response = client.get(f"/api/photos/{red['id']}/download")

    colour = dominant_colour(response.data)
    assert colour[0] > colour[2]


# @covers REQ-GAL-006@v1
def test_the_delivered_file_is_byte_for_byte_what_was_uploaded(client, gallery_dir):
    content = an_image("JPEG")
    photo = _upload(client, "holiday.jpg", content)

    response = client.get(f"/api/photos/{photo['id']}/download")

    assert response.data == content


# @covers REQ-GAL-006@v1
def test_the_delivered_file_carries_the_name_it_was_uploaded_under(client, gallery_dir):
    photo = _upload(client, "IMG_1234.jpg", an_image("JPEG"))

    response = client.get(f"/api/photos/{photo['id']}/download")

    assert "IMG_1234.jpg" in response.headers["Content-Disposition"]


# @covers REQ-GAL-006@v1
def test_a_photo_uploaded_under_an_unusable_name_is_delivered_with_the_right_extension(
    client, gallery_dir
):
    photo = _upload(client, "../../evil.png", a_coloured_image((10, 90, 40)))

    response = client.get(f"/api/photos/{photo['id']}/download")

    disposition = response.headers["Content-Disposition"]
    assert f"{photo['id']}.png" in disposition


# @covers REQ-GAL-006@v1
def test_downloading_an_unknown_photo_delivers_no_file(client, gallery_dir):
    response = client.get("/api/photos/does-not-exist/download")

    assert response.status_code == 404
    assert "Content-Disposition" not in response.headers
