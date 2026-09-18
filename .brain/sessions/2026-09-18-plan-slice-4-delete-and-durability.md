# Plan — slice 4, Delete and durability

Covers **REQ-GAL-005@v1** (6 criteria, belts A/B/C) and **REQ-GAL-008@v1**
(5 criteria, belt A). Branch `feat/gal-delete`, cut from `origin/main`.

Gate: `close-slice.js --gate` passes — slices 1–3 are Done. `REQ-GAL-005`
depends on `001` and `003`, both `verified`; `REQ-GAL-008` depends on `001`
(verified) and `005` (this slice).

**Branched from `main`, not from a previous slice's branch.** Last session
slice 2 reached `main` inside slice 3's pull request because slice 3 was
stacked on it, and five requirements went unreviewed. `main` now carries
everything through slice 3, so this branch needs nothing else.

## Record read before designing

- **ADR-0004** — Photos are files named by identifier, Thumbnails beside them,
  a SQLite index. Deleting therefore touches three things, and all three must go.
- **ADR-0002** — Flask; this adds one route.
- **constraints/csp-blocks-playwright-wait-for-function.md** — belt B uses
  `page.evaluate` and `expect(...)`, never `wait_for_function`.
- **constraints/test-basenames-must-be-unique-across-belts.md** — hence
  `test_delete.py` (A), `test_delete_http.py` (C), `test_delete_browser.py` (B).
- `.brain/rejected/` is empty.

---

## What must be true

**REQ-GAL-005 — Delete.** A confirmed deletion removes that Photo and leaves
the others; no Thumbnail for it is shown afterwards; asking to delete produces
the question **"Are you sure you want to delete this photo?"** verbatim;
declining leaves the Photo; and neither the Photo nor its Thumbnail is retained
anywhere afterwards.

**REQ-GAL-008 — Durability.** An undeleted Photo is still there later in the
same run, and **after the application is stopped and started again**; deleting
one leaves the others; the Photo is present in the storage folder as an
ordinary copyable file; and a deleted Photo is still gone after a restart.

## Approach

`PhotoStore.delete()` removes the index row, the Photo file and the Thumbnail
file — all three, because ADR-0004 put the bytes in two places and the facts in
a third, and criterion 6 says nothing may be retained. `DELETE /api/photos/<id>`
exposes it.

The delete control lives **in the Larger view**, not on the tile. The brief
reads "click one to see it larger, and be able to delete and download a photo",
which puts deleting after opening; it also keeps the Gallery grid free of
controls that would compete with the Thumbnails. Confirmation is a second
`<dialog>` carrying the required sentence as its text, consistent with slice 3
and assertable word-for-word. On confirm the Photo goes, both dialogs close and
the Gallery reloads; on decline the confirmation closes and nothing else
changes.

Durability needs almost no code — ADR-0004 already put every fact on disk. What
it needs is **tests that would fail if that stopped being true**: a second
`PhotoStore` opened against the same folder, standing in for a restart. That is
an honest analogue rather than a real process restart, because nothing is
cached in memory today; it is worth writing precisely so that the day someone
adds a cache, this fails.

Files:

```
src/mygallery/photos/store.py           + delete()
src/mygallery/web/api.py                + DELETE /api/photos/<id>
src/mygallery/templates/gallery.html    + delete control, confirmation dialog
src/mygallery/static/app.js             + the delete flow
src/mygallery/static/app.css            + confirmation dialog styling
tests/test_delete.py                    A  (005)
tests/test_durability.py                A  (008)
tests/api/test_delete_http.py           C  (005)
tests/e2e/test_delete_browser.py        B  (005)
```

## Test skeleton

Annotation `# @covers REQ-GAL-005@v1` / `# @covers REQ-GAL-008@v1`.

**Belt A — `tests/test_delete.py`** (005)
- `deleting_a_photo_removes_it_from_the_gallery` *(1)*
- `deleting_a_photo_leaves_the_other_photos` *(2)*
- `deleting_a_photo_removes_its_file_from_disk` *(6)*
- `deleting_a_photo_removes_its_thumbnail_from_disk` *(6)*
- `deleting_a_photo_that_is_not_there_is_refused` *(hardening)*

**Belt A — `tests/test_durability.py`** (008)
- `a_photo_is_still_in_the_gallery_later_in_the_same_run` *(1)*
- `deleting_one_photo_leaves_the_other_in_the_gallery` *(2)*
- `a_photo_is_still_in_the_gallery_when_the_store_is_reopened` *(3)*
- `a_photo_is_present_in_the_storage_folder_as_a_readable_file` *(4)*
- `the_stored_file_holds_the_bytes_that_were_uploaded` *(4)*
- `a_deleted_photo_is_still_gone_when_the_store_is_reopened` *(5)*

**Belt C — `tests/api/test_delete_http.py`** (005)
- `deleting_a_photo_reports_success` *(1)*
- `a_deleted_photo_is_no_longer_listed` *(1)*
- `deleting_a_photo_leaves_the_others_listed` *(2)*
- `the_thumbnail_of_a_deleted_photo_is_no_longer_served` *(3)*
- `deleting_an_unknown_photo_is_not_found` *(hardening)*

**Belt B — `tests/e2e/test_delete_browser.py`** (005)
- `asking_to_delete_a_photo_asks_for_confirmation` *(4)*
- `the_confirmation_asks_are_you_sure_you_want_to_delete_this_photo` — exact
  text *(4)*
- `declining_the_confirmation_leaves_the_photo_in_the_gallery` *(5)*
- `confirming_the_deletion_removes_the_thumbnail_from_the_gallery` *(1, 3)*
- `confirming_the_deletion_leaves_the_other_thumbnails` *(2)*

| Criterion | Covered by |
|---|---|
| 005.1 removed | A, C (2), B |
| 005.2 others remain | A, C, B |
| 005.3 no Thumbnail shown | C, B |
| 005.4 the exact question | B (2) |
| 005.5 declining keeps it | B |
| 005.6 nothing retained | A (2) |
| 008.1–008.5 | `tests/test_durability.py`, one test each (two for 4) |

## Decisions this forces

**None that warrant an ADR.** Both open choices — the delete control in the
Larger view rather than on the tile, and a `<dialog>` rather than the browser's
`confirm()` — are confined to one template and one block of `app.js`, and are
cheap to reverse. They are written into the Approach instead.

## What I am unsure about

- **Where the delete control belongs is a judgement, not a requirement.** No
  criterion says. I have read the brief's ordering as putting it in the Larger
  view, but "delete this one" from the grid is an equally fair reading and is
  less tedious for tidying up several Photos. **Worth one sentence to the
  client**, and cheap to move if they say the grid.
- **The restart criterion is tested by reopening the store, not by restarting a
  process.** Nothing is cached in memory today, so the two are equivalent now —
  but they would stop being equivalent the moment a cache appeared, which is
  exactly when the test would start earning its place. I would not claim
  criterion 3 is proven against a real restart; a manual stop-and-start on the
  client's PC is the honest confirmation.
- **The stale-row problem is still not covered by any criterion, and this is the
  slice ADR-0004 expected to deal with it.** A Photo the client deletes in
  Explorer leaves its index row: the Gallery lists it and its Thumbnail 404s, so
  they see a broken tile. Nothing in `REQ-GAL-005` or `REQ-GAL-008` describes
  that case, so **I do not intend to build it** — that would be scope no
  requirement asked for. It is either a new requirement or something the client
  accepts, and it is your call which. Flagging it here rather than quietly
  fixing it or quietly dropping it.
- **Criterion 6 says "not retained anywhere".** I read that as the Photo file,
  the Thumbnail file and the index row — everything ADR-0004 creates. It does
  not extend to the operating system's recycle bin, which the client explicitly
  said they do not want ("once I delete it, it's gone. I don't need a recycle
  bin"), so deletion is a real unlink, not a move.

---

## Waiting for approval

**No code has been written.** Nothing outside `.brain/sessions/` was touched,
and this file is left uncommitted — a plan is brain knowledge and belongs in a
`/checkpoint` pull request, not the slice's code commit.
