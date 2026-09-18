"""Belt C — REQ-GAL-005 over HTTP."""

import io

import pytest
from tests.conftest import an_image

pytestmark = pytest.mark.integration


def _upload(client, count: int) -> list[dict]:
    client.post(
        "/api/photos",
        data={
            "photos": [(io.BytesIO(an_image("JPEG")), f"p{n}.jpg") for n in range(count)]
        },
        content_type="multipart/form-data",
    )
    return client.get("/api/photos").get_json()["photos"]


# @covers REQ-GAL-005@v1
def test_deleting_a_photo_reports_success(client, gallery_dir):
    photo = _upload(client, 1)[0]

    response = client.delete(f"/api/photos/{photo['id']}")

    assert response.status_code == 204


# @covers REQ-GAL-005@v1
def test_a_deleted_photo_is_no_longer_listed(client, gallery_dir):
    photo = _upload(client, 1)[0]

    client.delete(f"/api/photos/{photo['id']}")

    assert client.get("/api/photos").get_json()["photos"] == []


# @covers REQ-GAL-005@v1
def test_deleting_a_photo_leaves_the_others_listed(client, gallery_dir):
    photos = _upload(client, 3)

    client.delete(f"/api/photos/{photos[1]['id']}")

    remaining = {p["id"] for p in client.get("/api/photos").get_json()["photos"]}
    assert remaining == {photos[0]["id"], photos[2]["id"]}


# @covers REQ-GAL-005@v1
def test_the_thumbnail_of_a_deleted_photo_is_no_longer_served(client, gallery_dir):
    photo = _upload(client, 1)[0]
    assert client.get(f"/api/photos/{photo['id']}/thumbnail").status_code == 200

    client.delete(f"/api/photos/{photo['id']}")

    assert client.get(f"/api/photos/{photo['id']}/thumbnail").status_code == 404


def test_deleting_an_unknown_photo_is_not_found(client, gallery_dir):
    response = client.delete("/api/photos/does-not-exist")

    assert response.status_code == 404
