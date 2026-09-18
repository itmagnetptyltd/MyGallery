# Plan — slice 2, Upload and Gallery

Covers **REQ-GAL-001@v1, REQ-GAL-002@v1, REQ-GAL-003@v1, REQ-GAL-007@v1,
REQ-GAL-010@v1** — all `agreed`, all `version: 1`, 29 acceptance criteria
between them. Branch `feat/gal-upload-gallery`, cut from `origin/main`.

Gate: `close-slice.js --gate` passes — slice 1 is Done. Every `depends_on` is
either inside this slice (001, 003) or already `agreed`.

Belts: **A** on all five, **B** on 001/003/007, **C** on 001/003/010. This is
the first slice with belt C.

## Record read before designing

- **ADR-0001** — Python 3.12+, Pillow named for Thumbnails, one prerequisite.
- **ADR-0002** — Flask is the HTTP layer. Governs `app.py` and `web/**`, which
  this slice extends.
- **ADR-0003** — Python is the one prerequisite; app dependencies are part of
  the app. **Adding Pillow is the first real test of this decision.**
- **constraints/g7-...** — G7 is fail-closed; `pytest -q -m integration` exits 5
  on an empty belt-C set. **This slice writes the first belt-C tests, which
  makes that command collect something and removes the exit-5 problem.**
- `.brain/rejected/` is empty.

> ⚠️ **ADR-0002 and ADR-0003 are not merged.** They are on
> `brain/checkpoint-2026-09-18-2`, pushed but unreviewed. This plan assumes
> both stand. If ADR-0002 is rejected, the HTTP layer changes and most of this
> plan changes with it. Merge that checkpoint before `/tdd`.

---

## What must be true

**REQ-GAL-001 — Upload (9 criteria).** One Photo uploads; a second adds rather
than replaces; an uploaded Photo is retrievable afterwards; JPEG, PNG, GIF and
WebP each become Photos; ≤25 MB is accepted and >25 MB is not; a batch of thirty
produces thirty Photos; a batch of thirty with three unacceptable produces
twenty-seven; the Gallery is reachable with no sign-in.

**REQ-GAL-002 — Identity (4).** The application issues the identifier; two
Photos uploaded under the same filename get different identifiers; a second
Photo never reuses the first's identifier; a filename containing separators or
`..` still stores inside the Photo directory.

**REQ-GAL-003 — The Gallery (6).** A Thumbnail per Photo; each Thumbnail renders
its own Photo; newest Upload first; a Thumbnail is smaller in bytes than its
Photo; only part of a long Gallery loads and no numbered page control appears;
scrolling loads more.

**REQ-GAL-007 — Empty Gallery (5).** No Thumbnail; no error; a
there-are-no-Photos-yet message; the Upload control visible; and if the Gallery
genuinely cannot be read, an error **instead of** that message.

**REQ-GAL-010 — Refusing non-images (5).** Not-an-image adds no Photo and does
not report success; content renamed to `.jpg` is still refused; HEIC and RAW are
refused; the reason says "not a supported image type".

## Approach

Photos become plain files under a folder the client can find; a SQLite index
alongside them carries the identifier, original filename, format, byte size and
upload time. Upload is a `POST` accepting a batch; each file is validated,
identified, written and thumbnailed **independently**, so one bad file in thirty
cannot take the other twenty-nine with it. The Gallery page fetches a page of
Photos from a JSON endpoint and appends more as the user scrolls; the empty
state is rendered from the same data, so "no Photos" and "cannot read the
Gallery" are distinguishable rather than both being an empty grid.

Validation is by **content, not extension**: Pillow opens the bytes and reports
the real format, which is the only way `REQ-GAL-010`'s renamed-file criterion
can pass. The caller's filename is never used as a path — it is stored as data
for Download (slice 5) and nothing else, which is what makes `REQ-GAL-002`'s
traversal criterion structural rather than a sanitising function someone can
forget to call.

New and changed files:

```
pyproject.toml                         + pillow
src/mygallery/config.py                + PHOTO_DIR, THUMB_DIR, MAX_PHOTO_BYTES,
                                         ACCEPTED_FORMATS, PAGE_SIZE
src/mygallery/photos/__init__.py
src/mygallery/photos/identity.py       new identifier per Photo
src/mygallery/photos/validation.py     format sniffing + size limit
src/mygallery/photos/thumbnails.py     Pillow
src/mygallery/photos/store.py          save / list page / get / index
src/mygallery/web/api.py               POST /api/photos, GET /api/photos,
                                         GET /api/photos/<id>/thumbnail
src/mygallery/app.py                   register the api blueprint, MAX_CONTENT_LENGTH
src/mygallery/templates/gallery.html   upload control, grid, empty state
src/mygallery/static/app.js            upload + infinite scroll (external: CSP)
src/mygallery/static/app.css           tiles, empty state
tests/test_identity.py                 A
tests/test_validation.py               A
tests/test_store.py                    A
tests/test_thumbnails.py               A
tests/test_gallery_page.py             A
tests/api/test_photos_http.py          C  (@pytest.mark.integration)
tests/e2e/test_upload_and_gallery.py   B
```

Belt C goes in `tests/api/` (the adapter's `apiGlobs`) **and** carries
`@pytest.mark.integration`, so the path satisfies G3's belt letter and the
marker satisfies the gate's integration command. Both are needed; they are
different mechanisms.

## Test skeleton

Annotation is `# @covers REQ-GAL-0NN@v1`. One test per criterion minimum;
29 criteria, so at least 29 tests.

**Belt A**

`tests/test_identity.py` — 002
- `the_application_issues_an_identifier_when_an_upload_completes`
- `two_photos_uploaded_under_the_same_filename_get_different_identifiers`
- `a_second_photo_does_not_reuse_the_first_photos_identifier`

`tests/test_validation.py` — 010, 001
- `a_jpeg_a_png_a_gif_and_a_webp_are_each_accepted` *(parametrised)*
- `content_that_is_not_an_image_is_refused`
- `content_renamed_to_a_jpg_extension_but_not_a_jpeg_is_refused`
- `a_heic_file_is_refused` / `a_camera_raw_file_is_refused`
- `the_refusal_reason_says_the_file_is_not_a_supported_image_type`
- `a_file_of_exactly_the_limit_is_accepted`
- `a_file_over_the_limit_is_refused`

`tests/test_store.py` — 001, 002, 003
- `saving_a_photo_puts_it_in_the_gallery`
- `saving_a_second_photo_leaves_the_first_in_place`
- `a_saved_photo_can_be_retrieved_afterwards`
- `a_filename_containing_path_separators_stores_inside_the_photo_directory`
- `a_filename_containing_dot_dot_stores_inside_the_photo_directory`
- `photos_are_listed_with_the_most_recently_uploaded_first`
- `a_page_of_the_gallery_holds_no_more_than_the_page_size`
- `the_next_page_continues_where_the_previous_one_ended`

`tests/test_thumbnails.py` — 003
- `a_thumbnail_is_smaller_in_bytes_than_its_photo`
- `a_thumbnail_renders_its_own_photo_and_not_another`

`tests/test_gallery_page.py` — 007, 001
- `an_empty_gallery_shows_no_thumbnail`
- `an_empty_gallery_reports_no_error`
- `an_empty_gallery_says_there_are_no_photos_yet`
- `an_empty_gallery_shows_the_upload_control`
- `a_gallery_that_cannot_be_read_reports_an_error`
- `a_gallery_that_cannot_be_read_does_not_show_the_no_photos_message`
- `the_gallery_is_shown_without_a_sign_in_step`

**Belt C — `tests/api/test_photos_http.py`** (001, 003, 010)
- `uploading_one_photo_returns_success_and_the_photo_is_listed`
- `uploading_thirty_photos_in_one_request_creates_thirty_photos`
- `uploading_thirty_of_which_three_are_not_images_creates_twenty_seven`
- `uploading_a_file_over_the_limit_creates_no_photo`
- `uploading_a_non_image_does_not_report_success`
- `listing_returns_photos_newest_first`
- `listing_returns_at_most_one_page_and_a_cursor`
- `requesting_a_thumbnail_returns_image_bytes`

**Belt B — `tests/e2e/test_upload_and_gallery.py`** (001, 003, 007)
- `an_empty_gallery_invites_the_first_upload`
- `uploading_photos_shows_them_as_thumbnails`
- `thumbnails_appear_newest_first`
- `no_numbered_page_control_is_shown`
- `scrolling_to_the_end_loads_more_thumbnails`

## Decisions this forces

1. **Where Photos live on disk — ADR-0004, and it must be written before
   `/tdd`.** ADR-0001 deferred it to "when slice 2 is planned"; this is that
   moment. The client asked for "a normal folder on my disk that I can find and
   back up myself" (`REQ-GAL-008`). I propose `%USERPROFILE%\Pictures\MyGallery`
   with `photos/` and `thumbnails/` beneath it, overridable by an environment
   variable for tests. **Not** `%LOCALAPPDATA%` — the client said *find and back
   up*, and AppData is where things go to be forgotten.

2. **How Photo metadata is stored — part of ADR-0004.** Upload time, original
   filename and format have to live somewhere: ordering (003), the download
   filename (006, slice 5) and per-file batch results (009, slice 6) all need
   them. I propose a **SQLite index** (`sqlite3` is stdlib, so no dependency),
   with the Photos as ordinary files beside it. Ordering, paging and atomic
   per-file commit each become one query.
   The alternative is **a JSON sidecar per Photo** — simpler, self-describing,
   and survives the client moving files by hand, at the cost of reading every
   sidecar to sort. At the client's stated scale (a few hundred, up to 2,000)
   both work. SQLite's weakness is exactly the client's stated habit: if they
   delete a file in Explorer the index keeps a row for it, so the Gallery must
   skip rows whose file is missing. **Worth ruling on explicitly.**

3. **`MAX_CONTENT_LENGTH` is not the 25 MB limit.** Flask applies it to the
   whole request; a batch of thirty 10 MB Photos is a legitimate 300 MB request.
   Setting it to 25 MB would make `REQ-GAL-001`'s batch criterion fail. It must
   be the batch ceiling (≈30 × 25 MB), with the **per-file** 25 MB limit enforced
   in `validation.py`. Getting this backwards is the most likely way this slice
   ships something that passes review and fails the requirement.

4. **The CSP from slice 1 forbids inline script.** `default-src 'self'` is
   already set, so the upload and infinite-scroll behaviour must live in
   `static/app.js`, not a `<script>` block. This is a constraint, not a
   preference — an inline handler will silently not run.

## What I am unsure about

- **This slice is large.** Five requirements, 29 criteria, three belts, and it
  introduces storage, validation, image processing, a JSON API and front-end
  JavaScript at once. That is a big pull request to review honestly. If you want
  it split, the natural seam is **001 + 002 + 010 (upload and storage, belts
  A/C)** then **003 + 007 (the Gallery, belts A/B/C)** — the second depends on
  the first and nothing else. I have planned it whole because `slices.yaml` says
  so and `/slice-add` warns against reshuffling a written sequence; say the word
  and it becomes two.
- **"Only part of the Gallery is loaded" has no number.** The client said
  hundreds to a couple of thousand and "it shouldn't get slow", which is not a
  page size. I propose 60 per page and will state it as a constant, but it is a
  judgement filling a gap the requirement left.
- **"A Gallery that cannot be read" needs a way to be made to fail in a test.**
  I intend to point the store at an unreadable directory. That is testing an
  error path through a filesystem condition, which is slightly artificial; if
  you would rather that criterion were verified by hand, say so and I will not
  fake it with a mock.
- **Thumbnail dimensions are unspecified.** I propose a 320 px longest edge,
  JPEG, which satisfies "smaller in bytes" comfortably. A Photo already smaller
  than that is an edge case the requirement does not mention — I intend to store
  a Thumbnail anyway so the code has one path, and flag it here rather than
  silently special-casing it.
- **Pillow is the first dependency added under ADR-0003.** If that reading is
  wrong, this is where it starts costing. One sentence to the client before
  `/tdd` would settle it.

---

## Waiting for approval

**No code has been written.** Nothing outside `.brain/sessions/` was touched,
and this file is deliberately left uncommitted — a plan is brain knowledge and
belongs in a `/checkpoint` pull request, not in the slice's code commit. That
distinction is what went wrong at slice 1.

Before `/tdd`: merge the pending checkpoint (ADR-0002/0003), and write **ADR-0004**
for decisions 1 and 2 above.
