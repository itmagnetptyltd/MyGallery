# 2026-09-18 — Build slice 5, Download

Sixth session of the day. Another thin checkpoint: the plan already said this
slice would not force an ADR, and the build did not discover one.

## Worked on

`REQ-GAL-006`, now `verified`. Slice 5 is **Done (1/1)**.

- `/feature-plan REQ-GAL-006`, then `/tdd`, tests first.
- 15 new tests across belts A, B and C. `/close-slice` recorded the
  annotations at v1.
- Commit `0449c94`, merged to `main` as pull request **#10**.

Ten of eleven requirements are `verified`. One remains `agreed`:
`REQ-GAL-009` (Upload failure reporting, slice 6).

## Learned

**`/close-slice` records annotations, not a green belt-B run.** The three belt
files exist and pin `REQ-GAL-006@v1`, so the script moved the id to `verified`
and marked the slice Done. That is what the command is for. It is not evidence
that the browser path works — see below.

**The stored filename reached a header for the first time, and stayed a
header.** [[ADR-0004]] already named the file on disk after the identifier.
This slice used the stored name only as `send_file(..., download_name=...)`.
Hand-assembling `Content-Disposition` was never tried; the plan ruled it out
before a line was written. That is why nothing went into `rejected/`.

## Left unfinished

- **The Larger view has no Download control.** The plan called for an anchor
  beside Delete (`data-testid="download-photo"`) pointing at
  `GET /api/photos/<id>/download`, plus the two lines in `app.js` and
  `app.css` that make it appear when the view opens. None of those files
  changed. Belt B (`tests/e2e/test_download_browser.py`) clicks that control
  and will fail until it exists. The route itself is on `main`; this is the
  missing piece of criterion 1 in the browser.

  It is still cheap to add, and it is still the same open question as the
  Delete control: the brief's ordering put both in the Larger view, and a
  control on the grid is an equally fair reading. One sentence to the client
  would settle both.

- **"Cannot be used as delivered" is still the plan's judgement, not the
  client's.** Empty, path separators, `..`, control characters — recorded in
  `2026-09-18-plan-REQ-GAL-006.md` under *What I am unsure about*. Windows
  reserved device names (`CON.jpg`, `NUL.png`) are still not handled.

- **`.gitignore` still has no `.coverage` entry**, and the test directories
  still have no `__init__.py`. Same as the last four sessions; they want a
  `chore:` commit, not another mention here.

## Promoted to the record

**Nothing.** The plan's own verdict stands: the route shape and the control's
placement are trivially reversible, and `download_name()` is one pure function
pinned by belt A. Writing an ADR for either would put noise next to the four
decisions that actually constrain what can be built.

Nothing was added to `rejected/` or `constraints/`: nothing was tried and
abandoned, and no new limit was measured.
