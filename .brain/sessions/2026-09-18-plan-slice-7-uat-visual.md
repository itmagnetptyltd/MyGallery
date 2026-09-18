# Plan — slice 7, UAT visual

Covers **REQ-GAL-012@v1, REQ-GAL-013@v1, REQ-GAL-014@v1** — all `agreed`.
Branch named in the sequence: `feat/gal-uat-visual`.

These three ids are the new criteria also written onto **REQ-GAL-003@v2**,
**REQ-GAL-001@v2 / REQ-GAL-007@v2**, and **REQ-GAL-004@v2** (CHG-0001–0004
absorbed). Slice 7 exists because add-slice refuses to put 001/003/007/004
in a second slice; they stay in slices 2 and 3.

Gate: `--gate REQ-GAL-012 REQ-GAL-013 REQ-GAL-014` fails — slice 2 is
In progress (2/5) because 001/003/007 dropped to `agreed` at v2. Ran with
`--force` because this increment was ordered after that versioning.

Dependencies 003, 001, 007, 004 are `agreed` at v2, not `verified`. Their
v1 behaviour still holds in the running app. This slice adds the new
surface; it does not rebuild Upload or the Gallery store.

Belts: **A and B** on all three. No belt C — nothing new is an HTTP
contract.

## Record read before designing

- **ADR-0002** — Flask; this slice changes the template and static assets
  it already serves.
- **ADR-0004** — Photos and Thumbnails stay files named by identifier.
  Larger cards still request `/api/photos/<id>/thumbnail`, not the Photo.
- **constraints/test-basenames-must-be-unique-across-belts.md** — belt B
  file is `test_uat_visual_browser.py`.
- **constraints/csp-blocks-playwright-wait-for-function.md** — belt B uses
  `expect(...)` and `page.evaluate`, never `wait_for_function`.
- `.brain/rejected/` is empty.

---

## What must be true

**REQ-GAL-012 — Thumbnail cards (2).** Each Thumbnail is shown in a card
wider than the v1 160-pixel-minimum tile. Each Thumbnail is a card with a
visible surface around the image, not a bare `img`.

**REQ-GAL-013 — Upload popup (2).** Starting an Upload offers the file
picker from a popup. An empty Gallery still shows a control that opens
that popup.

**REQ-GAL-014 — In-panel controls (2).** When the Larger view is open, the
close control is inside the panel. The Delete control is inside the panel.

v1 criteria on 001/003/007/004 still hold: Photos still land, Thumbnails
are still smaller in bytes than the Photo, empty Gallery still says so,
Escape and close still dismiss the Larger view.

---

## Approach

No new routes. No store change. The v1 grid is `minmax(160px, 1fr)` and
each Thumbnail is a bare `img.tile`. The v1 Larger view places close at
`top: -14px` and Delete at `bottom: -52px`, both outside the dialog box.

**Cards.** Wrap each Thumbnail in a card element (`data-testid="thumbnail-card"`)
with a visible surface (background and padding or border). Raise the grid
minimum above 160px so a card is wider than the delivered v1 tile. The
`img` inside still loads the stored Thumbnail. A card that showed the
full Photo would contradict REQ-GAL-003 criterion 4.

**Upload popup.** A second native `<dialog>` (same pattern as the Larger
view), opened from a control that stays visible on an empty Gallery. The
file input lives in that dialog. The existing header control becomes the
opener; the empty-state copy can point at the same opener. `set_input_files`
in current belt-B tests targets `upload-input` — keep that test id on the
input so v1 upload tests still find it once the popup is open, or open the
popup in those tests when we re-pin them.

**Larger view.** Keep the native `<dialog>`. Move close and Delete into the
panel's box (a header and a footer inside the dialog, `overflow` no longer
`visible` for the purpose of parking controls outside). "Inside" means the
control's bounding box is within the panel's bounding box. Escape, close,
and scroll restore stay as they are.

Files:

```
src/mygallery/templates/gallery.html     upload <dialog>; card markup;
                                         close/Delete inside Larger view
src/mygallery/static/app.css             larger card grid; card surface;
                                         in-panel Larger view chrome
src/mygallery/static/app.js              open/close upload popup; wrap
                                         tiles in cards
tests/test_uat_visual.py                 A
tests/e2e/test_uat_visual_browser.py     B
```

Existing `@covers REQ-GAL-001@v1` / `003@v1` / `007@v1` / `004@v1` pins
are stale the moment those versions moved. This slice re-reads them and
moves the pin to `@v2` where the v1 assertion still holds. New tests
annotate both the slice-7 id and the versioned id, e.g.
`@covers REQ-GAL-012@v1` and `@covers REQ-GAL-003@v2`.

---

## Test skeleton

Annotation is `# @covers REQ-GAL-012@v1` (and the matching versioned id).

**Belt A — `tests/test_uat_visual.py`**

Rendered from the Flask test client: parse the Gallery HTML and, where
needed, the CSS the page links.

- `gallery_css_sets_card_min_width_above_160px` — 012 criterion 1
- `gallery_html_has_a_card_surface_around_each_thumbnail` — after a
  Photo is stored, the Gallery markup wraps the Thumbnail in a card
  element, not a bare `img` as the only child of the grid. 012 criterion 2
- `gallery_html_includes_an_upload_popup` — 013 criterion 1
- `empty_gallery_html_includes_a_control_that_opens_the_upload_popup` —
  013 criterion 2
- `larger_view_markup_places_close_inside_the_panel` — 014 criterion 1
- `larger_view_markup_places_delete_inside_the_panel` — 014 criterion 2

**Belt B — `tests/e2e/test_uat_visual_browser.py`**

- `a_thumbnail_card_is_wider_than_160_pixels` — bounding box width > 160
- `a_thumbnail_is_shown_as_a_card_not_a_bare_image` — card surface
  visible around the image
- `starting_an_upload_opens_a_popup` — opener → popup visible, then the
  file input
- `an_empty_gallery_shows_a_control_that_opens_the_upload_popup`
- `the_close_control_is_inside_the_larger_view_panel` — close
  `getBoundingClientRect()` is inside the panel's
- `the_delete_control_is_inside_the_larger_view_panel` — same for Delete

| Criterion | Covered by |
|---|---|
| 012-1 card wider than 160px | A (1), B (1) |
| 012-2 card surface, not bare image | A (1), B (1) |
| 013-1 files chosen from a popup | A (1), B (1) |
| 013-2 empty Gallery opens that popup | A (1), B (1) |
| 014-1 close inside the panel | A (1), B (1) |
| 014-2 Delete inside the panel | A (1), B (1) |

---

## Decisions this forces

**None that warrant an ADR.** A second `<dialog>` for Upload, wrapping
tiles in cards, and moving two controls inside a box they already belong
to are cheap to reverse and confined to the three static files above.

---

## What I am unsure about

- **"Larger" has no target size.** The criterion is only "wider than the
  v1 160px minimum." I will pick a minimum that is clearly larger (not
  161px) and leave the exact number in CSS, not in the requirement.
- **"In a good way" has no look.** The criterion is a visible card
  surface around the image. I will not invent a design system, captions,
  hover chrome, or a new type scale unless you name them.
- **REQ-GAL-009's failure list.** CHG-0003 noted it may need a home on
  the popup. 009 is still v1 and not in this slice. I will leave the
  existing on-page list unless you say to move it.
- **Existing belt-B upload tests** click `upload-input` without opening a
  popup. Once the input lives in a closed dialog they will fail. Re-pin
  and teach those tests to open the popup first — that is in this slice,
  because otherwise G3 and the suite go red together.
- **Slices 2 and 3 stay not-Done** until 001/003/007/004 have `@covers`
  at v2. The dual annotation above is how they close without a second
  rebuild of Upload.

---

## Waiting for approval

**No code has been written.** Nothing outside `.brain/` was touched for
the implementation. Say what to change in this plan, or approve and
`/tdd`.
