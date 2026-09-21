"""Belt C — the description across the HTTP boundary.

REQ-GAL-001@v3 carries it in on the Upload, REQ-GAL-003@v3 carries it back out
in the Gallery listing, and REQ-GAL-002@v2 lets it be changed afterwards.
"""

from io import BytesIO

from tests.conftest import an_image


def _upload(client, name="holiday.jpg", description=None):
    data = {"photos": (BytesIO(an_image("JPEG")), name)}
    if description is not None:
        data["description"] = description
    return client.post("/api/photos", data=data, content_type="multipart/form-data")


# @covers REQ-GAL-001@v3
def test_uploading_with_a_description_carries_it_into_the_gallery(client):
    response = _upload(client, description="Beach at dawn")

    assert response.status_code == 201
    assert response.get_json()["photos"][0]["description"] == "Beach at dawn"


# @covers REQ-GAL-001@v3
def test_uploading_without_a_description_still_succeeds(client):
    response = _upload(client)

    assert response.status_code == 201
    assert response.get_json()["photos"][0]["description"] is None


# @covers REQ-GAL-001@v3
def test_an_upload_carrying_a_long_description_is_not_refused_for_length(client):
    response = _upload(client, description="x" * 400)

    assert response.status_code == 201
    # Not refused - but nothing unbounded reaches storage either.
    assert len(response.get_json()["photos"][0]["description"]) == 250


# @covers REQ-GAL-003@v3
def test_the_gallery_listing_carries_each_photos_description(client):
    _upload(client, name="described.jpg", description="Beach at dawn")
    _upload(client, name="plain.jpg")

    body = client.get("/api/photos").get_json()

    by_name = {photo["filename"]: photo["description"] for photo in body["photos"]}
    assert by_name == {"described.jpg": "Beach at dawn", "plain.jpg": None}


# @covers REQ-GAL-002@v2
def test_a_description_can_be_changed_after_the_upload(client):
    photo_id = _upload(client, description="first").get_json()["photos"][0]["id"]

    response = client.patch(f"/api/photos/{photo_id}/description", json={"description": "second"})

    assert response.status_code == 200
    assert client.get("/api/photos").get_json()["photos"][0]["description"] == "second"


# @covers REQ-GAL-002@v2
def test_a_photo_with_no_description_can_be_given_one_afterwards(client):
    photo_id = _upload(client).get_json()["photos"][0]["id"]

    client.patch(f"/api/photos/{photo_id}/description", json={"description": "given later"})

    assert client.get("/api/photos").get_json()["photos"][0]["description"] == "given later"


# @covers REQ-GAL-002@v2
def test_changing_the_description_of_a_photo_that_is_not_there_is_not_found(client):
    response = client.patch("/api/photos/not-a-photo/description", json={"description": "x"})

    assert response.status_code == 404
    # The route exists and refuses this Photo, rather than not existing at all.
    assert response.get_json() == {"error": "No such Photo."}
