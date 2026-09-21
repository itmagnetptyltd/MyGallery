"""REQ-GAL-002 — the application issues the identifier, not the caller."""

from mygallery.photos.identity import new_photo_id


# @covers REQ-GAL-002@v2
def test_the_application_issues_an_identifier():
    assert new_photo_id()


# @covers REQ-GAL-002@v2
def test_two_photos_uploaded_under_the_same_filename_get_different_identifiers():
    first = new_photo_id()
    second = new_photo_id()

    assert first != second


# @covers REQ-GAL-002@v2
def test_an_identifier_contains_no_path_separator():
    identifier = new_photo_id()

    assert "/" not in identifier and "\\" not in identifier and ".." not in identifier
