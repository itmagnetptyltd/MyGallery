# 2026-09-18 — Build slice 2, Upload and Gallery

Third session of the day. The first decomposed the brief, the second built
slice 1; this one built slice 2 in two passes.

## Worked on

`REQ-GAL-001`, `REQ-GAL-002`, `REQ-GAL-003`, `REQ-GAL-007`, `REQ-GAL-010` —
all five now `verified`. Slice 2 is **Done (5/5)**; slices 1 and 2 are both
closed, four remain.

- `/feature-plan` for the whole slice, against Python and Flask.
- Split into two passes on the developer's call — **2a** `001 + 002 + 010`
  (upload, identity, format refusal), then **2b** `003 + 007` (the Gallery and
  its empty state). `slices.yaml` was left alone: `add-slice.js` only appends,
  and `/slice-add` forbids hand-editing the sequence, so the slice simply read
  *In progress (3/5)* between the two passes. That was accurate, and no tooling
  had to be worked around.
- `/tdd` twice, tests first both times. 80 tests, coverage 96%, ruff clean.
- Commit `e1f5006` on `feat/gal-upload-gallery`, not yet pushed.

## Learned

Durable items were promoted — see below. Four things that are not:

**A test passed before the code it tested existed.** The belt-C assertion
"a Thumbnail is smaller than its Photo" was green while the thumbnail route was
still missing, because Flask's 404 page is smaller than a JPEG. Size
comparisons make weak assertions: anything that fails produces *something*, and
something is usually small. It was strengthened to assert `Content-Type:
image/*` and that the bytes decode.

**Then the same test failed `677 < 677`, and the test was wrong, not the code.**
`REQ-GAL-003`'s criterion says "a Photo whose stored file is several
megabytes"; the test used a 64×48 image whose Thumbnail re-encodes to exactly
the same size. **A Photo already smaller than the 320px Thumbnail edge is not
guaranteed a smaller Thumbnail** — the requirement does not promise it, so
nothing was built to force it. If the client ever notices, that is a change
record, not a defect.

**Two e2e assertions were checking DOM presence when the criteria are about
what is shown.** `to_have_count(0)` fails against an element that exists but is
hidden. `REQ-GAL-007` says the application *reports* no error, not that no error
element exists — `to_be_hidden()` is the assertion that matches the words.

**`# noqa` was the wrong first instinct.** Ruff's `S608` flagged an f-string in
the paging SQL. The interpolated fragment was a fixed literal and safe, and the
first fix added two suppressions. Writing the two queries out literally removed
the finding instead of silencing it, and reads better besides.

## Left unfinished

- **Slice 2 is committed but not pushed**, and no pull request is open.
  `feat/gal-upload-gallery` sits at `e1f5006`, one commit ahead of `main`.
- **The stale-row problem is real and unhandled.** A Photo deleted in Explorer
  leaves its index row; the Gallery lists it and its Thumbnail 404s. This is the
  weakness accepted when SQLite was chosen over sidecars, it is written into
  [[ADR-0004]], and it belongs to `REQ-GAL-005` in slice 4.
- **`tests/`, `tests/api/` and `tests/e2e/` have no `__init__.py`.** The naming
  convention in the new constraint works, but the two-minute permanent fix was
  out of slice scope.
- **`.gitignore` still has no `.coverage` entry.** Second session running. The
  artefact was removed by hand again.
- **`REQ-GAL-009` will need the refusal reasons that already exist.** Slice 2's
  upload endpoint already returns `refused: [{filename, reason}]` because
  `REQ-GAL-001`'s batch criteria needed it; slice 6 is about *showing* that,
  and should reuse rather than rebuild.

## Promoted to the record

- `decisions/ADR-0004-photo-storage.md` — `%USERPROFILE%\Pictures\MyGallery`
  with a SQLite index; JSON sidecars considered and rejected, with the
  stale-row cost stated plainly. This closes the gap ADR-0001 opened and
  slice 2 had been implementing without a record.
- `constraints/test-basenames-must-be-unique-across-belts.md` — pytest cannot
  collect two same-named test files across the belt directories, and each one
  passes alone, so only the full suite catches it.
- `constraints/g7-blocks-once-a-belt-c-requirement-is-agreed.md` — **updated.**
  The exit-5 hazard recorded last session is **resolved**: belt C now has 16
  tests, so `pytest -q -m integration` exits 0. The rest of the constraint
  still stands — a collecting command does not make G7 resolve a reviewer.

Nothing was added to `rejected/`. JSON sidecars were argued against and never
written, so there is no evidence to record; they are in ADR-0004's
*Alternatives considered*, which is where an option rejected without being
tried belongs.
