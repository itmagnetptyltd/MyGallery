"""Where Photos are kept.

ADR-0004: the Photos are ordinary files in a folder the client can find and
back up; a SQLite index beside them carries the identifier, the filename the
Photo was uploaded under, its format, its size and when it arrived.

The index is opened per call from `config`, not captured at import time, so
tests can repoint the Gallery at a throwaway directory.
"""

import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from mygallery import config
from mygallery.photos import thumbnails
from mygallery.photos.identity import new_photo_id

_PAGE_SQL = (
    "SELECT id, filename, format, byte_size, uploaded_at, sequence"
    " FROM photos ORDER BY sequence DESC LIMIT ?"
)

_PAGE_AFTER_SQL = (
    "SELECT id, filename, format, byte_size, uploaded_at, sequence"
    " FROM photos WHERE sequence < ? ORDER BY sequence DESC LIMIT ?"
)

_SCHEMA = """
CREATE TABLE IF NOT EXISTS photos (
    id          TEXT PRIMARY KEY,
    filename    TEXT NOT NULL,
    format      TEXT NOT NULL,
    byte_size   INTEGER NOT NULL,
    uploaded_at TEXT NOT NULL,
    sequence    INTEGER NOT NULL
);
"""


class GalleryUnreadable(RuntimeError):
    """The Gallery exists but could not be read.

    REQ-GAL-007 distinguishes this from an empty Gallery: one shows a message
    inviting the first Upload, the other reports an error. Collapsing the two
    is how a broken application looks merely empty.
    """


@dataclass(frozen=True)
class Page:
    photos: list["Photo"]
    next_cursor: int | None


@dataclass(frozen=True)
class Photo:
    id: str
    filename: str
    format: str
    byte_size: int
    uploaded_at: str


class PhotoStore:
    """The Gallery, on disk."""

    def __init__(
        self,
        gallery_dir: Path,
        photo_dir: Path,
        thumbnail_dir: Path,
        index_path: Path,
    ) -> None:
        self._gallery_dir = gallery_dir
        self._photo_dir = photo_dir
        self._thumbnail_dir = thumbnail_dir
        self._index_path = index_path

    @classmethod
    def open(cls) -> "PhotoStore":
        """Open the Gallery the configuration currently points at."""
        store = cls(
            config.GALLERY_DIR,
            config.PHOTO_DIR,
            config.THUMBNAIL_DIR,
            config.INDEX_PATH,
        )
        store._prepare()
        return store

    # --- writing ------------------------------------------------------------

    def save(self, filename: str, content: bytes, image_format: str = "JPEG") -> Photo:
        """Write one Photo and record it.

        The caller's `filename` is stored as data only. The file on disk is
        named for the identifier this issues, which is what makes REQ-GAL-002's
        traversal criterion structural rather than a sanitising step someone
        can forget.
        """
        photo_id = new_photo_id()
        extension = config.EXTENSION_FOR_FORMAT.get(image_format, ".bin")
        self._photo_dir.mkdir(parents=True, exist_ok=True)
        (self._photo_dir / f"{photo_id}{extension}").write_bytes(content)

        # REQ-GAL-003: a Thumbnail is stored, not derived on each request, so
        # opening the Gallery never touches the full-size Photo.
        self._thumbnail_dir.mkdir(parents=True, exist_ok=True)
        thumbnail_path = self._thumbnail_dir / f"{photo_id}{thumbnails.THUMBNAIL_EXTENSION}"
        thumbnail_path.write_bytes(thumbnails.render(content))

        photo = Photo(
            id=photo_id,
            filename=filename,
            format=image_format,
            byte_size=len(content),
            uploaded_at=datetime.now(UTC).isoformat(),
        )
        with self._connect() as connection:
            connection.execute(
                "INSERT INTO photos (id, filename, format, byte_size, uploaded_at, sequence)"
                " VALUES (?, ?, ?, ?, ?,"
                " (SELECT COALESCE(MAX(sequence), 0) + 1 FROM photos))",
                (
                    photo.id,
                    photo.filename,
                    photo.format,
                    photo.byte_size,
                    photo.uploaded_at,
                ),
            )
        return photo

    def delete(self, photo_id: str) -> None:
        """Remove a Photo entirely.

        REQ-GAL-005 criterion 6: nothing may be retained. ADR-0004 puts a Photo
        in three places, so all three go — the file, its Thumbnail, and the
        index row. The client asked for deletion to be permanent ("once I
        delete it, it's gone"), so these are unlinks, not moves.
        """
        if self.get(photo_id) is None:
            raise KeyError(photo_id)

        # Files first, then the row: a row without files shows a broken tile,
        # whereas files without a row are invisible and harmless.
        self.path_for(photo_id).unlink(missing_ok=True)
        thumbnail = self._thumbnail_dir / f"{photo_id}{thumbnails.THUMBNAIL_EXTENSION}"
        thumbnail.unlink(missing_ok=True)

        try:
            with self._connect() as connection:
                connection.execute("DELETE FROM photos WHERE id = ?", (photo_id,))
        except sqlite3.Error as error:
            raise GalleryUnreadable(str(error)) from error

    # --- reading ------------------------------------------------------------

    def all(self) -> list[Photo]:
        """Every Photo, most recently uploaded first."""
        rows = self._query(
            "SELECT id, filename, format, byte_size, uploaded_at"
            " FROM photos ORDER BY sequence DESC"
        )
        return [Photo(*row) for row in rows]

    def get(self, photo_id: str) -> Photo | None:
        rows = self._query(
            "SELECT id, filename, format, byte_size, uploaded_at FROM photos WHERE id = ?",
            (photo_id,),
        )
        return Photo(*rows[0]) if rows else None

    def page(self, limit: int | None = None, after: int | None = None) -> Page:
        """One page of the Gallery, newest first.

        `after` is the cursor a previous page reported. REQ-GAL-003 asks for
        more Photos as the user scrolls, never a numbered page control, so the
        cursor is opaque to the caller and is simply where to resume.
        """
        size = limit or config.PAGE_SIZE

        # Two complete statements rather than one with an interpolated clause.
        # The fragment would have been a fixed literal, but "never build SQL by
        # interpolation" is a rule worth keeping structural: the next person to
        # edit this should not have to work out whether the f-string was safe.
        if after is None:
            rows = self._query(_PAGE_SQL, (size + 1,))
        else:
            rows = self._query(_PAGE_AFTER_SQL, (after, size + 1))

        has_more = len(rows) > size
        rows = rows[:size]
        next_cursor = rows[-1][5] if (has_more and rows) else None
        return Page(photos=[Photo(*row[:5]) for row in rows], next_cursor=next_cursor)

    def thumbnail_bytes(self, photo_id: str) -> bytes:
        if self.get(photo_id) is None:
            raise KeyError(photo_id)
        path = self._thumbnail_dir / f"{photo_id}{thumbnails.THUMBNAIL_EXTENSION}"
        return path.read_bytes()

    def path_for(self, photo_id: str) -> Path:
        photo = self.get(photo_id)
        if photo is None:
            raise KeyError(photo_id)
        extension = config.EXTENSION_FOR_FORMAT.get(photo.format, ".bin")
        return self._photo_dir / f"{photo_id}{extension}"

    def read_bytes(self, photo_id: str) -> bytes:
        return self.path_for(photo_id).read_bytes()

    # --- internals ----------------------------------------------------------

    def _prepare(self) -> None:
        self._gallery_dir.mkdir(parents=True, exist_ok=True)
        self._photo_dir.mkdir(parents=True, exist_ok=True)
        try:
            with self._connect() as connection:
                connection.executescript(_SCHEMA)
        except sqlite3.Error as error:
            raise GalleryUnreadable(str(error)) from error

    def _query(self, sql: str, parameters: tuple = ()) -> list[tuple]:
        try:
            with self._connect() as connection:
                return connection.execute(sql, parameters).fetchall()
        except sqlite3.Error as error:
            raise GalleryUnreadable(str(error)) from error

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._index_path)
