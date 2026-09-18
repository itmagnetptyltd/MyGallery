"""Belt C — REQ-GAL-009 over HTTP."""

import io

import pytest
from tests.conftest import an_image

from mygallery import config

pytestmark = pytest.mark.integration


def _upload(client, files):
    return client.post(
        "/api/photos",
        data={"photos": [(io.BytesIO(content), name) for name, content in files]},
        content_type="multipart/form-data",
    )


def _mixed_thirty():
    files = [(f"p{n}.jpg", an_image("JPEG")) for n in range(27)]
    files += [(f"bad{n}.txt", b"not an image") for n in range(3)]
    return files


def _fail_during_thumbnail(monkeypatch):
    from mygallery.photos import store as store_module

    monkeypatch.setattr(
        store_module.thumbnails,
        "render",
        lambda _content: (_ for _ in ()).throw(OSError("disk full")),
    )


# @covers REQ-GAL-009@v1
def test_uploading_thirty_of_which_three_fail_keeps_twenty_seven(client, gallery_dir):
    _upload(client, _mixed_thirty())

    assert len(client.get("/api/photos").get_json()["photos"]) == 27


# @covers REQ-GAL-009@v1
def test_each_failed_file_is_named_in_the_response(client, gallery_dir):
    response = _upload(client, _mixed_thirty())

    assert [item["filename"] for item in response.get_json()["refused"]] == [
        "bad0.txt",
        "bad1.txt",
        "bad2.txt",
    ]


# @covers REQ-GAL-009@v1
def test_each_failed_file_carries_its_reason(client, gallery_dir):
    response = _upload(client, _mixed_thirty())

    for item in response.get_json()["refused"]:
        assert item["filename"]
        assert item["reason"]


# @covers REQ-GAL-009@v1
def test_an_oversized_file_is_reported_as_too_large_with_the_limit(client, gallery_dir):
    jpeg = an_image("JPEG")
    oversized = jpeg + b"\0" * (config.MAX_PHOTO_BYTES + 1 - len(jpeg))

    response = _upload(client, [("huge.jpg", oversized)])

    reason = response.get_json()["refused"][0]["reason"]
    assert "too large" in reason
    assert "25 MB" in reason


# @covers REQ-GAL-009@v1
def test_a_save_that_throws_is_reported_and_leaves_no_photo(client, gallery_dir, monkeypatch):
    _fail_during_thumbnail(monkeypatch)

    response = _upload(client, [("holiday.jpg", an_image("JPEG"))])

    body = response.get_json()
    assert response.status_code == 422
    assert body["refused"][0]["filename"] == "holiday.jpg"
    assert "try again" in body["refused"][0]["reason"]
    assert client.get("/api/photos").get_json()["photos"] == []
    photos = gallery_dir / "photos"
    leftovers = list(photos.iterdir()) if photos.exists() else []
    assert leftovers == []


# @covers REQ-GAL-009@v1
def test_a_save_that_throws_in_a_batch_does_not_stop_the_others(
    client, gallery_dir, monkeypatch
):
    from mygallery.photos import store as store_module
    from mygallery.photos import thumbnails

    original = thumbnails.render
    calls = {"n": 0}

    def flaky(content):
        calls["n"] += 1
        if calls["n"] == 1:
            raise OSError("disk full")
        return original(content)

    monkeypatch.setattr(store_module.thumbnails, "render", flaky)

    response = _upload(
        client,
        [
            ("first.jpg", an_image("JPEG")),
            ("second.jpg", an_image("JPEG")),
        ],
    )

    names = {photo["filename"] for photo in client.get("/api/photos").get_json()["photos"]}
    assert names == {"second.jpg"}
    assert [item["filename"] for item in response.get_json()["refused"]] == ["first.jpg"]
