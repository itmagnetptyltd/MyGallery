"""The JSON endpoints the Gallery page talks to."""

from flask import Blueprint, Response, jsonify, request

from mygallery import config
from mygallery.photos import thumbnails
from mygallery.photos.store import GalleryUnreadable, PhotoStore
from mygallery.photos.validation import validate_upload

api = Blueprint("api", __name__, url_prefix="/api")


@api.post("/photos")
def upload_photos():
    """Accept a batch of Photos.

    REQ-GAL-001: each file succeeds or fails on its own, so three bad files in
    thirty leave twenty-seven Photos in the Gallery rather than none.
    """
    store = PhotoStore.open()
    stored, refused = [], []

    for upload in request.files.getlist("photos"):
        content = upload.read()
        result = validate_upload(filename=upload.filename or "", content=content)
        if not result.accepted:
            refused.append(
                {
                    "filename": upload.filename,
                    "reason": result.reason.message() if result.reason else "refused",
                }
            )
            continue
        photo = store.save(
            filename=upload.filename or "",
            content=content,
            image_format=result.image_format or "JPEG",
        )
        stored.append(_as_json(photo))

    # Nothing got in: the Upload did not succeed. Some got in: it did, and the
    # caller is told which did not.
    status = 201 if stored else 422
    return jsonify({"photos": stored, "refused": refused}), status


@api.get("/photos")
def list_photos():
    """One page of the Gallery, newest first.

    REQ-GAL-003: a long Gallery is not delivered whole, and the cursor is how
    the page asks for more as the user scrolls.
    """
    limit = request.args.get("limit", type=int)
    after = request.args.get("after", type=int)
    try:
        page = PhotoStore.open().page(limit=limit, after=after)
    except GalleryUnreadable:
        # REQ-GAL-007: an unreadable Gallery is an error, not an empty one.
        return jsonify({"error": "The Gallery could not be read."}), 500
    return jsonify(
        {
            "photos": [_as_json(photo) for photo in page.photos],
            "nextCursor": page.next_cursor,
        }
    )


@api.get("/photos/<photo_id>")
def photo(photo_id: str):
    """The Photo itself, as stored.

    REQ-GAL-004: the Larger view shows the Photo, not an upscaled Thumbnail.
    REQ-GAL-006 (Download) serves these same bytes and differs only by
    Content-Disposition and the filename — extend this rather than duplicating
    the read.
    """
    store = PhotoStore.open()
    record = store.get(photo_id)
    if record is None:
        return jsonify({"error": "No such Photo."}), 404
    try:
        content = store.read_bytes(photo_id)
    except (KeyError, FileNotFoundError):
        return jsonify({"error": "No such Photo."}), 404

    media_type = config.MEDIA_TYPE_FOR_FORMAT.get(record.format, "application/octet-stream")
    return Response(content, mimetype=media_type)


@api.get("/photos/<photo_id>/thumbnail")
def photo_thumbnail(photo_id: str):
    store = PhotoStore.open()
    try:
        content = store.thumbnail_bytes(photo_id)
    except (KeyError, FileNotFoundError):
        return jsonify({"error": "No such Photo."}), 404
    return Response(content, mimetype=thumbnails.THUMBNAIL_MEDIA_TYPE)


def _as_json(photo) -> dict:
    return {
        "id": photo.id,
        "filename": photo.filename,
        "format": photo.format,
        "byteSize": photo.byte_size,
        "uploadedAt": photo.uploaded_at,
    }
