# Plan — slice 9: REQ-GAL-015@v1, REQ-GAL-017@v1, REQ-GAL-018@v1

All three `agreed`. Gate passed: slices 1–8 are Done. Dependencies REQ-GAL-001,
002, 003, 008 and 013 are all `verified`. REQ-GAL-018 depends on REQ-GAL-017,
which is in this plan — a dependency inside the slice, not a lock, so both are
planned and 017 is built first.

## Read first

`.brain/rejected/` holds nothing but its README: no approach here has been
tried and abandoned. `.brain/decisions/` governs the runtime, the HTTP layer
and storage; this slice touches none of them — the counter is presentation
only and adds no dependency, so no ADR is forced. The glossary fixes **Photo**,
**Thumbnail**, **Gallery**, **Upload** and **Larger view**; "description" is
not a glossary term and the requirements call it a description, so the tests do
too. Two constraints apply and are honoured: test basenames must be unique
across belts, and `page.wait_for_function` is unusable under the app's CSP —
`page.evaluate` is not, and is what the existing drop test uses.

## The one thing that is genuinely not built

**The character counter. REQ-GAL-017 c4 and c5.**

`grep` over `src/` finds no counter in the markup, the stylesheet or the
script. It was written into REQ-GAL-017 during `/resolve-ambiguities` on
2026-09-21, from the client's own words — *"a count on ke prass 1/150 like this
will indicate"* — and reads against 250 because 250 is the agreed limit; their
"150" was a slip in the illustration, which REQ-GAL-017's rationale records.

Everything else in this slice already exists, built in slice 2: the previews,
the description field and its 250-character cap, the storage, the durability,
the Larger view editor, and the alt text. **One further gap is a test gap, not
a code gap:** REQ-GAL-015 c2 — that a preview shows *the file it belongs to*
and not another chosen file — is not proved by any test today.

So this slice is: one small piece of code, three new tests that can genuinely
fail, and annotations for the rest.

## What must be true

### REQ-GAL-015@v1 — the popup shows the chosen files before they become Photos

| # | Observable behaviour | State |
|---|---|---|
| c1 | A chosen file is shown as a preview image, not just a filename | built, tested |
| c2 | A preview renders its own file, not another chosen one | built, **untested** |
| c3 | Thirty chosen files show thirty previews | built, tested |

### REQ-GAL-017@v1 — a Photo may carry an optional description given at its Upload

| # | Observable behaviour | State |
|---|---|---|
| c1 | An Upload with no description still adds the Photos | built, tested |
| c2 | A description of 250 or fewer characters is carried onto the Photos | built, tested |
| c3 | Typing past 250 leaves 250 in the field and does not refuse the Upload | built, tested |
| c4 | With the field empty, typing one character shows `1/250` | **not built** |
| c5 | With forty characters in the field, typing one more shows `41/250` | **not built** |
| c6 | A description survives a restart | built, tested |
| c7 | Changing a description replaces it and leaves the Photo unchanged | built, tested |
| c8 | The change happens in the Larger view | built, tested |

### REQ-GAL-018@v1 — a Photo's description is the alt text of its Thumbnail

| # | Observable behaviour | State |
|---|---|---|
| c1 | A described Photo's Thumbnail carries the description as alt | built, tested |
| c2 | An undescribed Photo's Thumbnail carries its filename as alt | built, tested |
| c3 | After a description is changed, alt is the changed description | built, tested |

## Approach

### The counter

A `<span>` beside the description field in the Upload popup, updated on every
`input` event. Three files, all under `src/`:

- `src/mygallery/templates/gallery.html` — a `data-testid="description-count"`
  span inside the existing `.upload-description-label`, next to the label text.
- `src/mygallery/static/app.js` — one listener on the existing
  `uploadDescription` element setting `textContent` to
  `` `${value.length}/${limit}` ``.
- `src/mygallery/static/app.css` — a rule to place it at the right of the
  label. Presentation only.

**The limit is read from the field's own `maxLength`, not written again in the
script.** `maxlength="250"` is already in the markup and is what enforces c3;
having the counter read it means the two can never disagree. Hard-coding 250 in
`app.js` would create a second place to change it, and a counter that says
`/250` while the field stops at some other number is worse than no counter.

The field starts empty, so the counter renders `0/250` before anything is
typed. No criterion names that state — see *What I am unsure about*.

Nothing is added to the Larger view's description editor: no criterion asks
for a counter there, and REQ-GAL-017 c4/c5 both say "the description field in
the Upload popup".

### Everything else

**Annotate the tests that already encode these criteria**, as slice 8 did, and
as `tests/test_uat_visual.py` has done since slice 7 — one test carrying both
`@covers REQ-GAL-012@v2` and `@covers REQ-GAL-003@v3`. Duplicating bodies under
a new id gives two tests that must be kept in step by hand.

This is the convention question raised at the end of slice 8 and not yet
settled in the record. **This plan assumes sharing.** If the project would
rather every requirement own its tests outright, say so at approval — it
changes roughly fifteen annotations into fifteen new tests, and it should then
be written down, because it will recur.

## Test skeleton

New tests. Belt A, in `tests/test_uat_visual.py`:

```python
# @covers REQ-GAL-017@v1
def test_the_upload_popup_shows_a_character_count_for_the_description(client):
    # assert: 'data-testid="description-count"' in the served page

# @covers REQ-GAL-017@v1
def test_the_character_count_reads_its_limit_from_the_field(project_root):
    # the script must not carry its own copy of 250
    # assert: "maxLength" in app.js
    # assert: "/250" not in app.js
```

Belt B, in `tests/e2e/test_description_browser.py`:

```python
# @covers REQ-GAL-017@v1
def test_typing_one_character_shows_one_of_two_hundred_and_fifty(page, gallery_url):
    # open the popup, type "x" into the description
    # assert: the count reads "1/250"

# @covers REQ-GAL-017@v1
def test_typing_a_forty_first_character_shows_forty_one_of_two_hundred_and_fifty(
    page, gallery_url
):
    # fill forty characters, then type one more
    # assert: the count reads "41/250"

# @covers REQ-GAL-015@v1
def test_each_preview_renders_its_own_file(page, gallery_url, tmp_path):
    # choose two files of known and different colours
    # assert: the two preview images have different src values,
    #         and each matches the file it was created from
```

The last one is REQ-GAL-015 c2 and is the only new test here that is not about
the counter. `conftest.a_coloured_image` and `dominant_colour` already exist
for exactly this kind of "which Photo is this really" check — slice 2 used them
to tie a Thumbnail to its Photo.

Annotations to add to existing tests, each read against the 015/017/018
criterion text before it is added:

| Criterion | Belt | Test gaining an annotation |
|---|---|---|
| 015 c1 | A | `test_the_upload_popup_shows_a_preview_of_each_chosen_file` |
| 015 c1 | B | `test_choosing_a_file_shows_a_preview_image_before_the_upload_is_made` |
| 015 c3 | B | `test_choosing_thirty_files_shows_a_preview_for_every_one` |
| 017 c1 | A | `test_an_upload_with_no_description_still_becomes_a_photo` |
| 017 c1 | C | `test_uploading_without_a_description_still_succeeds` |
| 017 c2 | A | `test_a_description_of_250_characters_is_carried_whole` |
| 017 c2 | B | `test_a_description_given_with_the_upload_reaches_the_gallery` |
| 017 c2 | C | `test_uploading_with_a_description_carries_it_into_the_gallery` |
| 017 c3 | B | `test_the_description_field_holds_250_characters_and_the_upload_is_not_refused` |
| 017 c3 | C | `test_an_upload_carrying_a_long_description_is_not_refused_for_length` |
| 017 c6 | A | `test_a_description_given_at_upload_survives_a_restart` |
| 017 c7 | A | `test_changing_a_description_replaces_it_and_leaves_the_photo_itself_unchanged` |
| 017 c7 | C | `test_a_description_can_be_changed_after_the_upload` |
| 017 c8 | B | `test_a_description_is_changed_in_the_larger_view` |
| 018 c1 | A | `test_a_thumbnails_alt_text_is_its_photos_description` |
| 018 c1 | B | `test_a_thumbnail_carries_its_photos_description_as_alt_text` |
| 018 c2 | B | `test_a_thumbnail_with_no_description_carries_its_filename_as_alt_text` |
| 018 c3 | B | `test_a_description_is_changed_in_the_larger_view` |

REQ-GAL-017 declares belt C; 015 and 018 do not, and none is written for them.
No new test file is created, so the basename constraint is not engaged.

## Decisions this forces

None that needs an ADR. No dependency, no storage change, no new HTTP surface.

The one choice worth recording if it is contested is reading the limit from
`maxLength` rather than declaring it in the script. It is a one-line decision
now and an annoying inconsistency later if the two ever disagree.

## What I am unsure about

**The counter's resting state.** No criterion says what the field shows before
anything is typed. `0/250` is the only reading that keeps c4 meaningful — a
counter that appears on first keypress would satisfy c4's letter while being
strange to use — but it is my choice, not the client's. If they want the
counter hidden until typing starts, that is a different build and I would
rather hear it now than after.

**Whether the counter belongs in the Larger view too.** REQ-GAL-017 c4 and c5
both say "the Upload popup", so this plan builds it only there. But a user who
can edit a description in the Larger view against the same 250-character limit
and see no count will reasonably call that a defect. It is out of scope as
written; if you want it, it is a change record, not something to fold in.

**The 250 in the test names and assertions.** `test_typing_one_character_shows_
one_of_two_hundred_and_fifty` hard-codes the limit in the test, which is right —
a test that computed the expected value from `maxLength` would pass even if both
were wrong.

**REQ-GAL-015 c2 is the weakest of the three new tests.** Comparing `src`
values proves two previews differ; proving each renders *its own* file means
decoding a blob URL in the page. The skeleton above compares the rendered
colours through `conftest.dominant_colour`, which is what slice 2 did for
Thumbnails, but it is more machinery than the other tests here and I would
drop it to a simpler "the two previews differ" assertion if you would rather
keep it cheap.

---

**Waiting for approval. No code and no test has been written.**
