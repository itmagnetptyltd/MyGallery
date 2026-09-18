# ADR-0004 — Photos are files in a folder the client can back up, indexed in SQLite

- **Status:** accepted
- **Date:** 2026-09-18
- **Governs:** src/mygallery/config.py (`GALLERY_DIR`, `PHOTO_DIR`, `THUMBNAIL_DIR`, `INDEX_PATH`), src/mygallery/photos/store.py, src/mygallery/photos/thumbnails.py

## Context

[[ADR-0001]] deferred this explicitly — "where Photos are stored on disk is also
still open and belongs in its own ADR when slice 2 is planned". Slice 2 cannot
store a Photo without it, so this is that decision.

Two requirements constrain it. `REQ-GAL-008` carries the client's own words:

> "Please keep them in a normal folder on my disk that I can find and back up
> myself." — `.brain/requirements/ANSWERS.md`, 2026-09-18

And `REQ-GAL-003` needs three things from whatever holds the metadata: Photos
ordered by Upload time newest first, a Gallery that loads in parts as the user
scrolls, and a Thumbnail that is smaller than its Photo. Later slices need
more — the original filename for Download (`REQ-GAL-006`) and per-file results
for a partly failed batch (`REQ-GAL-009`).

So the Photo bytes and the facts *about* each Photo are two separate questions,
and this ADR answers both.

## Decision

**Location.** `%USERPROFILE%\Pictures\MyGallery`, overridable by the
`MYGALLERY_DIR` environment variable, holding:

```
Pictures/MyGallery/
  index.db
  photos/      <identifier>.jpg
  thumbnails/  <identifier>.jpg
```

A Photo's file is named for the identifier the application issued, never for
the name it was uploaded under. That is what makes `REQ-GAL-002`'s traversal
criterion structural rather than a sanitising step someone can forget to call.

**Metadata.** A **SQLite index** (`index.db`) carrying the identifier, the
filename the Photo was uploaded under, its format, its byte size, its upload
time and a monotonic sequence number. `sqlite3` is in the standard library, so
this adds no dependency.

**Thumbnails** are rendered once at Upload with Pillow and stored beside the
Photos, not derived per request — the client asked for the Gallery to stay fast
with large phone photos, and re-rendering on every view would defeat that.

The developer was shown both metadata options with their trade-offs and chose
this one.

## Alternatives considered

**`%LOCALAPPDATA%\MyGallery`.** The conventional Windows location for
application data, and rejected on the client's own words. They said *find and
back up*; AppData is hidden from a default Explorer view and is where things go
to be forgotten. Convention lost to a stated requirement.

**A JSON sidecar per Photo** (`<identifier>.json` beside each file). Genuinely
attractive: everything is readable in Notepad, copying the folder is a complete
and self-describing backup, there is no single file that can corrupt, and a
Photo the client moves by hand takes its metadata with it. It lost on what
`REQ-GAL-003` needs — ordering and paging become "read every sidecar, sort in
memory", and per-file atomicity on a partly failed batch needs care that a
single `INSERT` gets for free. At the client's stated scale (a few hundred, up
to 2,000) both would work; this was a judgement about which code stays honest
as the Gallery grows, not a measurement.

**A full database server.** Never seriously on the table. It would breach
`REQ-GAL-011`'s one-prerequisite criterion outright.

## Consequences

**Makes easy.** Newest-first ordering is `ORDER BY sequence DESC`. Paging is
`LIMIT` plus a cursor, which is what `REQ-GAL-003`'s scroll-to-load-more asks
for and what stops a two-thousand-Photo Gallery being delivered whole. Saving
one Photo is one `INSERT`, so a batch where three of thirty fail leaves exactly
twenty-seven. Backup stays "copy the folder" — `index.db` sits inside it.

**Makes hard.**

- **A Photo deleted in Explorer leaves a row behind.** This is the weakness the
  sidecar option did not have, and the client is exactly the sort of user who
  browses that folder — they asked for it to be findable. Today the Gallery
  would list a Photo whose file is gone and whose Thumbnail request 404s.
  **Nothing in slice 2's criteria names this, so nothing handles it yet.** It
  should be dealt with when `REQ-GAL-005` (delete) is built in slice 4.
- `index.db` is a single point of corruption. `GalleryUnreadable` exists so
  that case is reported as an error rather than shown as an empty Gallery
  (`REQ-GAL-007`), but there is no repair path and none is required yet.
- The folder is full of files named `a3f2b1c4….jpg`. The client can back it up,
  but they cannot browse it by photo name. That is the direct cost of
  `REQ-GAL-002` and is worth saying out loud, because "a normal folder I can
  find" may have implied more than it delivers.

**Rules out.** Naming stored files after the caller's filename, now or later —
that would reopen the traversal question and make two Photos with the same name
collide.

**Not settled here.** What the Gallery should do about an index row whose file
has vanished. Deliberately left to slice 4, where deletion is the subject.
