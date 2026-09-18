"""The JSON endpoints the Gallery page talks to."""

import io
import sqlite3

from flask import Blueprint, Response, jsonify, request, send_file

from mygallery import config
from mygallery.photos import thumbnails
from mygallery.photos.download import download_name
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
        try:
            photo = store.save(
                filename=upload.filename or "",
                content=content,
                image_format=result.image_format or "JPEG",
            )
        except (OSError, sqlite3.Error):
            # REQ-GAL-009: this file failed; the rest of the batch still runs.
            # The client's wording for a failure that is not a type or a size.
            refused.append(
                {
                    "filename": upload.filename,
                    "reason": "upload failed, please try again",
                }
            )
            continue
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
    record, content = _photo_and_bytes(photo_id)
    if record is None:
        return jsonify({"error": "No such Photo."}), 404
    return Response(content, mimetype=_media_type(record))


@api.get("/photos/<photo_id>/download")
def download_photo(photo_id: str):
    """The Photo as a file to save. REQ-GAL-006.

    The same bytes as the route above — the difference is Content-Disposition
    and the name. send_file builds that header: it applies RFC 5987 encoding
    and escaping, which is what stops a filename from breaking or injecting a
    header. Do not assemble it by hand.
    """
    record, content = _photo_and_bytes(photo_id)
    if record is None:
        return jsonify({"error": "No such Photo."}), 404

    return send_file(
        io.BytesIO(content),
        mimetype=_media_type(record),
        as_attachment=True,
        download_name=download_name(record.filename, record.format, record.id),
    )


def _photo_and_bytes(photo_id: str):
    """One read shared by every route that serves a Photo, so they cannot
    drift apart on what "the Photo" means."""
    store = PhotoStore.open()
    record = store.get(photo_id)
    if record is None:
        return None, None
    try:
        return record, store.read_bytes(photo_id)
    except (KeyError, FileNotFoundError):
        return None, None


def _media_type(record) -> str:
    return config.MEDIA_TYPE_FOR_FORMAT.get(record.format, "application/octet-stream")


@api.delete("/photos/<photo_id>")
def delete_photo(photo_id: str):
    """Delete a Photo. REQ-GAL-005."""
    store = PhotoStore.open()
    try:
        store.delete(photo_id)
    except KeyError:
        return jsonify({"error": "No such Photo."}), 404
    return "", 204


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
