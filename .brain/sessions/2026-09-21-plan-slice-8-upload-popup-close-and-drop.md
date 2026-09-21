# Plan — slice 8: REQ-GAL-016@v1, REQ-GAL-019@v1

Both `agreed`. Gate passed: slices 1–7 are Done. Dependencies REQ-GAL-001,
REQ-GAL-013 are `verified`.

## Read first, and what it changed

`.brain/rejected/` holds nothing but its README, so no approach here has been
tried and abandoned before. `.brain/decisions/` governs the runtime, the HTTP
layer and storage — none of which this slice touches. Two constraints do apply
and are honoured below. The glossary fixes **Upload**, **Photo** and
**Gallery**; the popup itself is not a glossary term, so the tests say "the
Upload popup" as the requirements do.

## The finding that shapes this plan

**Neither requirement needs production code. Both behaviours already exist.**

- REQ-GAL-016 (dropping files) was built in slice 2 — the `dragover`/`drop`
  handlers on the popup in `src/mygallery/static/app.js`.
- REQ-GAL-019 (the close control) was built in slice 7 — the cross in
  `src/mygallery/templates/gallery.html`, its rule in `app.css`, its handler in
  `app.js`.

That is not an accident. REQ-GAL-019's `source` says its criteria are the same
ones carried on REQ-GAL-013@v2, and REQ-GAL-016's says the same of
REQ-GAL-001@v3. Slices 2 and 7 built those mirrors, so this slice arrives with
the work done and only the traceability missing.

**This is therefore a test-only slice.** Approving this plan approves writing
no production code. If something is expected to be built here, the plan is
wrong and should be corrected before `/tdd`.

## What must be true

### REQ-GAL-016@v1 — files can be chosen by dropping them on the Upload popup

| # | Observable behaviour |
|---|---|
| c1 | With the popup open, dropping files on it chooses them, exactly as the picker does |
| c2 | Files dropped and then uploaded are in the Gallery as Photos |
| c3 | The picker still chooses files — dropping is an addition, not a replacement |

c3 is the one worth care. The client said "in upload **or** drag-drop", and
REQ-GAL-001@v3 c10 still requires files to be chosen from a popup. A change
that made dropping the only route would break an agreed criterion.

### REQ-GAL-019@v1 — the Upload popup can be closed without uploading anything

| # | Observable behaviour |
|---|---|
| c1 | The close control is inside the popup, at its top right |
| c2 | Activating it hides the popup and adds no Photo |
| c3 | After closing, starting an Upload shows the popup again |

## Approach

**Annotate the tests that already encode these criteria, rather than writing
near-duplicates pinned to a different id.** The project already does this: in
`tests/test_uat_visual.py`, `test_gallery_css_sets_card_min_width_above_160px`
carries both `@covers REQ-GAL-012@v2` and `@covers REQ-GAL-003@v3`, because one
test genuinely proves a criterion that two requirements share. The same is true
here, and duplicating the bodies would mean two tests that must be kept in step
by hand forever.

No file is created for the annotations; they go on existing tests.

### Mapping — what each criterion gets

| Criterion | Belt | Test, and what happens to it |
|---|---|---|
| 016 c1 | B | `test_dropping_files_on_the_popup_chooses_them_for_the_upload` — add `@covers REQ-GAL-016@v1` |
| 016 c2 | B | same test (it uploads and asserts the count) — covered by the same annotation |
| 016 c3 | B | **new**: `test_the_picker_still_chooses_files_when_dropping_is_available` |
| 016 c1–c3 | A | **new**: `test_the_upload_popup_accepts_dropped_files`, `test_dropping_on_the_upload_popup_is_not_the_only_way_to_choose` |
| 019 c1 | A | `test_the_upload_popup_has_a_close_control`, `..._is_inside_the_popup`, `..._is_placed_at_the_top_right` — add `@covers REQ-GAL-019@v1` |
| 019 c1 | B | `test_the_upload_popup_close_control_is_inside_the_popup_at_its_top_right` — add annotation |
| 019 c2 | A | `test_the_upload_popup_close_control_closes_the_popup` — add annotation |
| 019 c2 | B | `test_closing_the_upload_popup_adds_no_photo` — add annotation |
| 019 c3 | B | `test_the_upload_popup_can_be_reopened_after_it_was_closed` — add annotation |
| 019 c3 | A | **new**: `test_closing_the_upload_popup_leaves_it_reusable` |

Belt C is not declared on either requirement and none is written. Dropping and
closing are browser behaviours with no HTTP surface of their own.

### Files

- `tests/test_uat_visual.py` — annotations, plus the three new belt A tests.
- `tests/e2e/test_uat_visual_browser.py` — annotations, plus the new belt B test.
- `tests/e2e/test_description_browser.py` — one annotation on the drop test.

No new test file is needed, which also sidesteps
`constraints/test-basenames-must-be-unique-across-belts.md`. If the developer
prefers these tests in files of their own, the basenames must differ across
belts — `test_upload_popup_controls.py` and
`test_upload_popup_controls_browser.py`, not the same name twice.

**No file under `src/` is created or changed by this slice.**

## Test skeleton

Belt A, in `tests/test_uat_visual.py`:

```python
# @covers REQ-GAL-016@v1
def test_the_upload_popup_accepts_dropped_files(project_root):
    # app.js listens for drop on the popup and reads dataTransfer.files
    # assert: 'uploadPopup.addEventListener("drop"' in the script
    # assert: "dataTransfer" in the script

# @covers REQ-GAL-016@v1
def test_dropping_on_the_upload_popup_is_not_the_only_way_to_choose(client):
    # the file input is still in the served popup
    # assert: 'data-testid="upload-input"' in the page

# @covers REQ-GAL-019@v1
def test_closing_the_upload_popup_leaves_it_reusable(project_root):
    # the handler closes the dialog rather than removing or hiding it,
    # which is what allows showModal() to open it again
    # assert: "uploadPopup.close()" in the script
    # assert: "uploadPopup.remove()" not in the script
```

Belt B, in `tests/e2e/test_uat_visual_browser.py`:

```python
# @covers REQ-GAL-016@v1
def test_the_picker_still_chooses_files_when_dropping_is_available(
    page, running_server, tmp_path
):
    # open the popup, choose a file with the picker, upload
    # assert: the photo count reads "1"
```

Annotations added to the eight existing tests named in the mapping above. Each
was read against the REQ-GAL-016/019 criterion text before its annotation was
added, not matched on the name.

## Decisions this forces

None that needs an ADR. Nothing about the runtime, the HTTP layer or storage
changes, and no dependency is added.

One question is worth settling in review rather than in code: **whether a
mirrored requirement should carry its own tests or share the original's.** This
plan shares, following the 012/003 precedent already in the tree. If the project
would rather every requirement own its tests outright, that is a convention
worth writing down once — it will recur, because REQ-GAL-015, 017 and 018 in
slice 9 mirror REQ-GAL-001, 002, 003 and 008 the same way.

## What I am unsure about

**That a test-only slice is what you want.** Every criterion here is already
satisfied, so `/tdd` will produce green tests on the first run and no code. I
will prove each new test can fail by deliberately breaking `app.js` and
confirming it goes red, as in slices 4 and 7 — but that is verification after
the fact, not red-green, and I would rather say so now than present it as TDD
later.

**Belt A's reach.** Belt A here asserts on the served HTML and on the text of
`app.js`, which is the pattern `tests/test_uat_visual.py` already established.
It is a weak belt for behaviour: `test_closing_the_upload_popup_leaves_it_reusable`
checks that the source calls `close()`, which is evidence about the code rather
than about what a user experiences. The real proof of 019 c3 is the belt B test.
If belt A on these requirements is not earning its place, the honest fix is to
change `belts:` on the requirement — a change record, not something to decide
here.

**REQ-GAL-016 c1's "as if picked from the popup".** The existing belt B test
drops one file and asserts one preview appears, then uploads. It does not prove
a dropped batch behaves identically to a picked batch in every respect. If you
want that equivalence tested directly, say so and I will add a test that drops
three and picks three and compares the outcome.

---

**Waiting for approval. No code and no test has been written.**
