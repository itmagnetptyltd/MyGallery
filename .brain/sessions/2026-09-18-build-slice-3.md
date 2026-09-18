# 2026-09-18 — Build slice 3, Larger view

Fourth session of the day. Slices 1 and 2 were built earlier; this one built
slice 3 and got slices 2 and 3 onto `main`.

## Worked on

`REQ-GAL-004` — activating a Thumbnail shows the Larger view over the Gallery.

- `/feature-plan REQ-GAL-004`, then `/tdd`, tests first.
- 13 tests across belts A and B. Whole suite **93 passed**, coverage **96%**,
  ruff clean.
- `/close-slice` — slice 3 **Done (1/1)**.
- Commit `4af7ec7`, merged to `main` as pull request **#6**.

Four slices of six are now closed: `REQ-GAL-001`, `002`, `003`, `004`, `007`,
`010` and `011` are `verified`. Four requirements remain `agreed` —
`REQ-GAL-005`, `006`, `008`, `009`.

## Learned

The durable item was promoted — see below. Three that were not:

**`click()` scrolls its target into view before clicking.** The scroll-position
test captured `window.scrollY` before activating a Thumbnail, then found it
had changed by the time the Larger view opened — not because the dialog moved
the page, but because Playwright scrolled the last tile into view to click it.
The test now reads the position *with the Larger view open*, which is the place
the user is actually returning to.

**A test that cannot fail will happily pass.** The first scroll test used 12
tiles in an 800×600 viewport, which does not overflow — `scrollY` was 0, and
"the position is preserved" was trivially true. A guard assertion
(`assert scrolled_to > 0, "the Gallery did not scroll, so the test proves
nothing"`) caught it. Worth writing that guard by reflex whenever a test's
premise is a state the fixture has to reach.

**Native `<dialog>` did most of the work, and that is worth knowing when
reading the coverage.** Escape-to-close, the focus trap, the backdrop and the
preserved scroll position all came from the element rather than from code here.
Criterion 3's test therefore proves Chromium's behaviour as much as ours. That
is a real pass — the client asked for Escape to work and it does — but a
reviewer counting tests should know which ones exercise our own logic.

No ADR was written. The two real choices — native `<dialog>` over a hand-built
overlay, and serving the full Photo over a mid-size rendition — are each
confined to one template, one route and one block of `app.js`. Recording them
would be manufacturing ADRs to look diligent, and the reasoning is in the plan
and the commit message. If that judgement is wrong, the one to promote is
serving the full Photo: it becomes expensive the day MyGallery is reachable
from another device, which `REQ-GAL-011` forbids.

## Left unfinished

- **Slice 2 reached `main` without its own pull request.** `feat/gal-larger-view`
  was branched from `feat/gal-upload-gallery` because slice 3 genuinely needs
  slice 2's code, and pull request **#6** merged both. No pull request ever
  merged `feat/gal-upload-gallery`, so `REQ-GAL-001`, `002`, `003`, `007` and
  `010` — five requirements, 29 acceptance criteria, storage through front-end
  JavaScript — arrived with no review of their own. The branch was pushed in
  time for that to be avoidable, and was not. **The lesson for slices 4 to 6:
  branch the next slice from `main` after the previous slice's pull request has
  merged, not from the previous slice's branch.** `main` now carries everything
  through slice 3, so slice 4 can branch cleanly and this need not recur.
- **`feat/gal-upload-gallery` is still open on the remote** and now redundant —
  its commit is on `main`. Safe to delete, along with `feat/gal-boot`.
- **`.gitignore` still has no `.coverage` entry.** Third session running; the
  artefact was removed by hand again.
- **The stale-row problem is still unhandled** — a Photo deleted in Explorer
  leaves its index row, the Gallery lists it, and its Thumbnail 404s. Recorded
  in [[ADR-0004]] and belongs to `REQ-GAL-005` in slice 4.
- **`tests/`, `tests/api/` and `tests/e2e/` still have no `__init__.py`.** The
  naming convention holds, but the permanent fix is still two minutes' work.

## Promoted to the record

- `constraints/csp-blocks-playwright-wait-for-function.md` — the application's
  own `default-src 'self'` makes `page.wait_for_function` fail as `unsafe-eval`,
  while `page.evaluate` and `expect(...)` are unaffected because they go through
  the DevTools protocol rather than in-page `eval`. Explicitly forbids
  "fixing" it by relaxing the CSP.

Nothing was added to `rejected/`. Neither the hand-built overlay nor the
mid-size rendition was ever written, so there is no evidence to record; both
are argued in the slice 3 plan and the commit message.
