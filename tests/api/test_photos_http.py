"""Belt C — REQ-GAL-001 and REQ-GAL-010 over HTTP.

Marked `integration` so the adapter's belt-C command (`pytest -q -m
integration`) collects them. The directory satisfies G3's belt letter; the
marker satisfies the gate command. Both are needed, and they are different
mechanisms.
"""

import io

import pytest
from tests.conftest import an_image

pytestmark = pytest.mark.integration


def _upload(client, files):
    return client.post(
        "/api/photos",
        data={"photos": [(io.BytesIO(content), name) for name, content in files]},
        content_type="multipart/form-data",
    )


# @covers REQ-GAL-001@v2
def test_uploading_one_photo_reports_success(client, gallery_dir):
    response = _upload(client, [("one.jpg", an_image("JPEG"))])

    assert response.status_code == 201


# @covers REQ-GAL-001@v2
def test_an_uploaded_photo_is_listed_afterwards(client, gallery_dir):
    _upload(client, [("one.jpg", an_image("JPEG"))])

    assert len(client.get("/api/photos").get_json()["photos"]) == 1


# @covers REQ-GAL-001@v2
def test_uploading_thirty_photos_in_one_request_creates_thirty_photos(client, gallery_dir):
    _upload(client, [(f"p{n}.jpg", an_image("JPEG")) for n in range(30)])

    assert len(client.get("/api/photos").get_json()["photos"]) == 30


# @covers REQ-GAL-001@v2
def test_uploading_thirty_of_which_three_are_not_images_creates_twenty_seven(
    client, gallery_dir
):
    files = [(f"p{n}.jpg", an_image("JPEG")) for n in range(27)]
    files += [(f"bad{n}.jpg", b"not an image") for n in range(3)]

    _upload(client, files)

    assert len(client.get("/api/photos").get_json()["photos"]) == 27


# @covers REQ-GAL-001@v2
def test_a_batch_with_failures_names_each_failed_file(client, gallery_dir):
    files = [("good.jpg", an_image("JPEG")), ("bad.jpg", b"not an image")]

    response = _upload(client, files)

    assert [f["filename"] for f in response.get_json()["refused"]] == ["bad.jpg"]


# @covers REQ-GAL-010@v1
def test_uploading_a_non_image_adds_no_photo(client, gallery_dir):
    _upload(client, [("notes.txt", b"not an image")])

    assert client.get("/api/photos").get_json()["photos"] == []


# @covers REQ-GAL-010@v1
def test_uploading_only_a_non_image_does_not_report_success(client, gallery_dir):
    response = _upload(client, [("notes.txt", b"not an image")])

    assert response.status_code == 422


# @covers REQ-GAL-010@v1
def test_the_refusal_says_the_file_is_not_a_supported_image_type(client, gallery_dir):
    response = _upload(client, [("notes.txt", b"not an image")])

    assert "not a supported image type" in response.get_json()["refused"][0]["reason"]
