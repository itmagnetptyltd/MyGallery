# Outline: MyGallery user manual and quick-start guide

**Date:** 2026-09-23\
**Author:** manual-analyst, Phase 2\
**Against:** `AI guides/MyGallery/Planning/documentation-plan.md`, settled at the
Phase 1 gate on 2026-09-23

Every topic below carries the requirement and the test it rests on, so Phase 3
drafts from evidence rather than from memory. A topic with no requirement names
the file its facts come from instead.

Contents:

1. [Decisions settled here](#1-decisions-settled-here)
2. [Content typing: all 33 tasks](#2-content-typing-all-33-tasks)
3. [Merge decisions](#3-merge-decisions)
4. [The manual](#4-the-manual)
5. [The quick start, and README.md](#5-the-quick-start-and-readmemd)
6. [File layout](#6-file-layout)
7. [Figures](#7-figures)
8. [What could not be placed](#8-what-could-not-be-placed)

---

## 1. Decisions settled here

| Decision | Outcome | Section |
| --- | --- | --- |
| Document set | User manual and quick-start guide, as settled at the Phase 1 gate | 4, 5 |
| File layout | One Markdown file per document, not one file per chapter | 6 |
| Chapters | Fourteen, from the `references/structure.md` skeleton, with three of its chapters dropped | 4 |
| Merges | All four candidate pairs merged | 3 |
| Topics | Twenty-nine topics carry the 33 tasks | 2, 4 |
| Authority over the start steps | `README.md`, for every fact it states | 5 |
| Figures | All eight existing captures placed. None still to capture | 7 |
| Unplaceable | None. One topic is placed but cannot be completed until Q3 answers, and one until Q10 answers | 8 |

## 2. Content typing: all 33 tasks

Typed against the Diátaxis table in `SKILL.md`. The Phase 1 column is the
proposal in section 3 of the documentation plan.

| # | Task | Phase 1 | Phase 2 | Topic that carries it |
| --- | --- | --- | --- | --- |
| 1 | Install Python before the first run | how-to | how-to | 3.2 |
| 2 | Start MyGallery | how-to | how-to | 4.1 |
| 3 | Stop MyGallery | how-to | how-to | 4.3 |
| 4 | Open the Gallery again while MyGallery is running | how-to | how-to | 4.2 |
| 5 | Add your first Photo and see it in the Gallery | tutorial | tutorial | 5.1 |
| 6 | Add Photos to your Gallery | how-to | how-to | 7.1 |
| 7 | Add a batch of Photos in one Upload | how-to | how-to | 7.1, merged |
| 8 | Choose files by dropping them on the Upload popup | how-to | how-to | 7.1, as a second procedure under its own subheading |
| 9 | Check what you chose before you upload it | how-to | how-to | 7.1, as a step and its result |
| 10 | Describe a Photo as you upload it | how-to | how-to | 9.2 |
| 11 | Close the Upload popup without adding anything | how-to | how-to | 7.2 |
| 12 | Find a Photo in the Gallery | how-to | how-to | 8.1 |
| 13 | See a Photo at a larger size | how-to | how-to | 8.2 |
| 14 | Close the Larger view and return to your place | how-to | how-to | 8.2, merged |
| 15 | Change a Photo's description | how-to | how-to | 9.3 |
| 16 | Give a description to a Photo that has none | how-to | how-to | 9.3, merged |
| 17 | Where a description is shown, and who reads it | concept | concept | 9.1 |
| 18 | Download a Photo | how-to | how-to | 10.2 |
| 19 | Back up your Gallery | how-to | how-to | 10.3 |
| 20 | Delete a Photo | how-to | how-to | 11.1 |
| 21 | Keep a Photo after starting to delete it | how-to | how-to | 11.1, merged |
| 22 | Which files become a Photo | reference | reference | 12.1 |
| 23 | Limits | reference | reference | 12.2 |
| 24 | Where your Photos are kept, and who can reach them | concept | concept | 10.1 |
| 25 | What happens when part of an Upload fails | concept | concept | 13.1 |
| 26 | A file was refused as not a supported image type | how-to | how-to | 13.3 |
| 27 | A file was refused as too large | how-to | how-to | 13.4 |
| 28 | Some files in a batch did not go in | how-to | how-to | 13.2 |
| 29 | MyGallery will not start: "Python was not found" | how-to | how-to | 13.5 |
| 30 | MyGallery will not start: "Address already in use" | how-to | how-to | 13.6 |
| 31 | The browser did not open | how-to | how-to | 13.7 |
| 32 | The Gallery says it could not be read | how-to | how-to | 13.9 |
| 33 | Windows blocked MyGallery from creating its Gallery folder | new at the gate | how-to | 13.8 |

No type changed. Three placements differ from a one-task-one-topic reading, and
each is argued here:

- **Task 8 is a second procedure inside topic 7.1**, under its own subheading,
  because `REQ-GAL-016` makes dropping an alternative to the picker rather than
  a different goal. `references/structure.md` handles a meaningfully different
  path inside the topic, and its subheading keeps the phrase findable.
- **Task 9 is a step and its result inside topic 7.1.** The reader performs no
  separate procedure: the previews appear when files are chosen, and checking
  them is the verification step before the committing action. A topic of its
  own would have no `Before you begin` that 7.1 does not already carry.
- **Task 10 is topic 9.2 rather than a step in 7.1**, because a description is
  the client's own ask under `REQ-GAL-017` and a reader searches for it by name.
  Its procedure starts from an open Upload popup with files chosen, links 7.1 as
  its prerequisite, and repeats none of 7.1's steps. Topic 7.1 carries one
  optional step naming the `Description (optional)` field and linking to 9.2.

Three chapters the skeleton offers are dropped, and the reasons stand from the
Phase 1 plan: **Advanced tasks** (no requirement describes automation, bulk
operations or an integration), **Administration** (`04-permissions.md` found no
role, and `.brain/glossary.md` records no second user), and **Support and
feedback** (no support channel, hours or defect channel is recorded anywhere in
`.brain/`, and naming one would be invention).

The **FAQ** half of chapter 13 is also dropped. `references/structure.md`
forbids inventing FAQ entries, and no support ticket record exists for this
product.

## 3. Merge decisions

All four candidate pairs merge.

| Pair | Decision | Reason |
| --- | --- | --- |
| 6 and 7 | **Merged**, as topic 7.1 | One Upload carries one file or thirty, and the popup, the controls and the steps are identical. The only difference is how many files the reader selects, which is a sentence and a limit, not a topic. Two near-duplicate procedures drift apart |
| 13 and 14 | **Merged**, as topic 8.2 | Opening the Larger view and leaving it is one visit. The close is the procedure's last step, and the Gallery returning to the position it was scrolled to is the topic's result. A separate closing topic would end where the first began and would carry no prerequisite of its own |
| 15 and 16 | **Merged**, as topic 9.3 | `REQ-GAL-002` c7 and c8 differ only in whether the field starts empty. The steps, the control and the result are the same, so the difference is one sentence inside the topic |
| 20 and 21 | **Merged**, as topic 11.1 | The confirmation is one decision with two outcomes, and the reader who wants to stop is already inside the delete procedure. Putting the escape route in a second topic hides it from the only reader who needs it. The topic carries both outcomes: `Delete` confirms, `Keep it` declines |

Task 5 stays separate from 2, 6 and 12, as the Phase 1 plan reads it: it is the
tutorial kind, a single managed path to first success, and it branches nowhere.

## 4. The manual

Fourteen chapters, in reading order. Chapters 1 to 6 follow dependency, 7 to 11
follow the order the reader meets them, and 12 to 14 are lookup material.

Each topic title below is the heading Phase 3 writes. Titles are verb-first and
outcome-shaped for tasks, and noun phrases for concept and reference topics.

### 1. About this manual

Front matter, and one of the two places `references/style.md` permits a scope
statement. Not a task.

Holds: the product version (0.1.0, from `pyproject.toml` at commit `a00d0a4`),
the document version, the date, the audience, and the conventions.

The conventions section records three things:

- **Bold** names a control, and `code font` names a file, a folder or an
  address.
- The five callout types in use.
- **A quoted label keeps its own wording.** The empty-Gallery message reads
  `No photos yet. Click Upload photos to add your first photos.`, so a verbatim
  quotation carries `Click` into a manual whose own prose says `select`. The
  label is quoted exactly and never corrected. Source: `02-labels.md`,
  `src/mygallery/templates/gallery.html:24`.
- Photo, Gallery, Thumbnail, Upload, Download and Delete carry a capital as the
  defined terms of this product, and `Larger view` carries a capital `L` alone.
  Source: `AI guides/MyGallery/Planning/terminology.md`.

### 2. What MyGallery is

Introduction. Not a task. Two short paragraphs and a capability map linking to
each chapter. States that MyGallery runs on the reader's own PC and links to
topic 10.1 rather than restating it.

Evidence: `.brain/requirements/BRIEF.md`; `.brain/glossary.md`, "The user";
`REQ-GAL-011`.

### 3. Before you start

| # | Topic | Type | Rests on | Test | Figure |
| --- | --- | --- | --- | --- | --- |
| 3.1 | What you need | reference | `REQ-GAL-011` c1, c3; `ADR-0003`; open question Q8 | `tests/test_start_instructions.py:9,14` | none |
| 3.2 | Install Python | how-to | `REQ-GAL-011` c3; `README.md` "Before you start" | `tests/test_start_instructions.py:9,14` | none |

Topic 3.1 is a table of three rows: Windows 11, Python 3.12 or later, and Chrome
or Edge. It names no Windows build, because Q2 is unanswered and the record
supports "Windows 11" alone. It is silent on other browsers rather than claiming
them, which is Q8's answer.

Topic 3.2 carries the one prerequisite verbatim from `README.md`, including
`"Add python.exe to PATH"`. See section 5 for why that copy is the only one in
the set.

### 4. Starting and stopping MyGallery

| # | Topic | Type | Rests on | Test | Figure |
| --- | --- | --- | --- | --- | --- |
| 4.1 | Start MyGallery | how-to | `REQ-GAL-011` c1, c4; `README.md` "Run MyGallery" | `tests/e2e/test_boot.py:21`; `tests/test_launcher.py:20,47` | none |
| 4.2 | Open the Gallery again while MyGallery is running | how-to | `REQ-GAL-011` c1 | `tests/test_config.py:12`; `tests/test_launcher.py:37` | none |
| 4.3 | Stop MyGallery | how-to | `README.md` "Run MyGallery". No acceptance criterion covers stopping. Assumption A6, open question Q9 | none | none |

Topic 4.1 names `scripts/start.cmd` and `http://127.0.0.1:8765`, both copied
from `README.md`. Its `See also` links topic 13.8, so the Controlled Folder
Access entry is reachable from the starting chapter.

Topic 4.3 documents both ways `README.md` states, which is assumption A6. A
correction to Q9 changes this topic alone.

### 5. Getting started: your first Photo

| # | Topic | Type | Rests on | Test | Figure |
| --- | --- | --- | --- | --- | --- |
| 5.1 | Add your first Photo | tutorial | `REQ-GAL-001`, `REQ-GAL-003`, `REQ-GAL-007`, `REQ-GAL-011` | `tests/e2e/test_upload.py:27`; `tests/e2e/test_gallery_browser.py:69` | `Images/01-empty-gallery.png` |

A single managed path with no options and no branching: start MyGallery, see the
empty Gallery and its message, open the Upload popup, choose one photo, upload
it, and see its Thumbnail. It closes with next steps into chapters 7 to 11.

Its `See also` links topic 13.8, which is the second route into the Controlled
Folder Access entry from the starting chapters. That failure strikes at the
first Upload, which is this topic's third step.

### 6. The Gallery screen

The interface tour, kept against the odds because every later instruction naming
the header, a Thumbnail card, the Upload popup or the Larger view depends on
this chapter naming them first.

| # | Topic | Type | Rests on | Test | Figure |
| --- | --- | --- | --- | --- | --- |
| 6.1 | The Gallery screen | reference | `REQ-GAL-003` c7, c8; `REQ-GAL-007` c4, c6; `REQ-GAL-012`; `01-routes.md` | `tests/e2e/test_uat_visual_browser.py:55,67,92` | `Images/04-gallery-with-photos.png` |
| 6.2 | What a Thumbnail card shows | reference | `REQ-GAL-003` c11, c12; `REQ-GAL-018` c1, c2 | `tests/e2e/test_card_actions_browser.py:39,59`; `tests/e2e/test_uat_visual_browser.py:187` | `Images/05-thumbnail-card.png` |

Topic 6.1 departs from the tour pattern in `references/structure.md` on one
point: it carries a `Region | What it is for` table with **no numbered
callouts**, because each region is identified by its own visible label. The
accessibility rule forbids identifying an element by its position, the labels
are already verbatim in `02-labels.md`, and no annotated recapture is then
needed.

The regions named are the `MyGallery` heading, the `Upload photos` button, the
count of Photos, and the Gallery of Thumbnail cards. Source: `02-labels.md`,
Header and Gallery.

### 7. Adding Photos

| # | Topic | Type | Rests on | Test | Figure |
| --- | --- | --- | --- | --- | --- |
| 7.1 | Add Photos to your Gallery | how-to | `REQ-GAL-001` c7, c8, c10, c11; `REQ-GAL-013` c1, c5, c6; `REQ-GAL-015` | `tests/e2e/test_upload.py:27,40`; `tests/e2e/test_uat_visual_browser.py:80,170`; `tests/e2e/test_description_browser.py:57,71,195` | `Images/02-upload-popup-empty.png`, `Images/03-upload-popup-chosen.png` |
| 7.1a | Choose files by dropping them on the popup | how-to | `REQ-GAL-016` | `tests/e2e/test_description_browser.py:122`; `tests/e2e/test_uat_visual_browser.py:201` | none |
| 7.2 | Close the Upload popup without adding anything | how-to | `REQ-GAL-019` | `tests/e2e/test_uat_visual_browser.py:127,146,158` | none |

Topic 7.1 is the manual's central procedure and carries both popup figures,
which are the two states of one screen. Its steps are: open the popup with
`Upload photos`, choose files with `Choose files`, check the previews,
optionally enter a description, then `Upload`. Its result names the new
Thumbnails appearing newest first.

The topic states the batch limit of 30 and links topic 12.2 for the rest.
`09-reconciliation.md` records that a batch of chosen files makes a tall popup
the reader scrolls, which is the agreed criterion of `REQ-GAL-015@v2` and is
described as what the reader sees rather than as a fault.

Topic 7.2 is a single-step procedure and takes a bullet. It exists as a topic
because `REQ-GAL-019` was written after the client could not find the way out of
the popup.

### 8. Looking at Photos

| # | Topic | Type | Rests on | Test | Figure |
| --- | --- | --- | --- | --- | --- |
| 8.1 | Find a Photo in the Gallery | how-to | `REQ-GAL-003` c3, c5, c6 | `tests/e2e/test_gallery_browser.py:78,89,98` | none |
| 8.2 | See a Photo at a larger size | how-to | `REQ-GAL-004` c1 to c5, c8; `REQ-GAL-014` c2 | `tests/e2e/test_larger_view_browser.py:31,41,59,72,84,95,118`; `tests/e2e/test_larger_view_actions_browser.py:48` | `Images/06-larger-view.png` |

Topic 8.1 states the ordering (most recently uploaded first) and the load-more
behaviour (scrolling to the end loads further Thumbnails, with no numbered page
control) inside the topic. A separate concept topic for two sentences earns
nothing.

Topic 8.2 names all three ways out, which `REQ-GAL-004` c3, c4 and c8 each
require: **Escape**, the cross, and the `Close` button beside `Save
description`. Its result is the Gallery at the position it was scrolled to.

### 9. Describing Photos

| # | Topic | Type | Rests on | Test | Figure |
| --- | --- | --- | --- | --- | --- |
| 9.1 | Where a description is shown | concept | `REQ-GAL-018` | `tests/e2e/test_description_browser.py:135,147`; `tests/e2e/test_uat_visual_browser.py:187` | none |
| 9.2 | Describe a Photo as you upload it | how-to | `REQ-GAL-017` c1 to c5 | `tests/e2e/test_description_browser.py:83,96,106,172,182` | none |
| 9.3 | Change a Photo's description | how-to | `REQ-GAL-017` c7, c8; `REQ-GAL-002` c8, c9 | `tests/e2e/test_description_browser.py:160`; `tests/test_description.py:30,41` | none |

Topic 9.1 is the chapter's concept, at its head as `references/structure.md`
requires, and it states that a description becomes the Thumbnail's alt text and
that a Photo with none carries its filename instead. It carries no instructions.

Topic 9.2 has a `Before you begin` linking topic 7.1 and starts from an open
popup with files chosen. It states the 250-character limit, the `<typed>/250`
counter, and that an Upload with no description still succeeds.

Topic 9.3 carries both starting states in one sentence: the `Description` field
in the Larger view holds the Photo's description, or is empty where it has none.
The committing action is `Save description`.

### 10. Getting your Photos back out

| # | Topic | Type | Rests on | Test | Figure |
| --- | --- | --- | --- | --- | --- |
| 10.1 | Where your Photos are kept, and who can reach them | concept | `REQ-GAL-008` c4; `REQ-GAL-011` c5; `ADR-0004`; `README.md` "Your photos are yours" | `tests/test_binding.py:23`; `tests/test_durability.py:44`; `tests/e2e/test_upload.py:20` | none |
| 10.2 | Download a Photo | how-to | `REQ-GAL-006`; `REQ-GAL-003` c13 | `tests/e2e/test_download_browser.py:31,42,53`; `tests/e2e/test_card_actions_browser.py:71` | none |
| 10.3 | Back up your Gallery | how-to | `REQ-GAL-008` c4 | `tests/test_durability.py:44,53` | none |

Topic 10.1 is the chapter's concept and names `Pictures\MyGallery`, which Q4
settled at the gate. It states that a Photo is there as an ordinary file the
reader can copy, and that a connection from another device is refused. It does
not mention `MYGALLERY_DIR`, which Q5 settled as undocumented and unsupported.

Topic 10.3 therefore describes **copying** the Photos out of `Pictures\MyGallery`
and never moving the folder. Its `Before you begin` links topic 10.1 rather than
repeating the location.

Topic 10.2 states that the downloaded file is byte-for-byte the file that was
uploaded and keeps its uploaded filename, and that Download is on the Thumbnail
card rather than in the Larger view.

### 11. Removing Photos

| # | Topic | Type | Rests on | Test | Figure |
| --- | --- | --- | --- | --- | --- |
| 11.1 | Delete a Photo | how-to | `REQ-GAL-005`; `REQ-GAL-003` c14, c15 | `tests/e2e/test_delete_browser.py:34,44,57,70,83`; `tests/e2e/test_card_actions_browser.py:88,101,112` | `Images/07-delete-confirmation.png` |

The confirmation question is quoted exactly as
`Are you sure you want to delete this photo?`, which
`src/mygallery/templates/gallery.html:138` records as the client's own wording
and a criterion of `REQ-GAL-005`, never a caption.

The topic carries a **Warning** callout inside the step it governs, because
deletion is permanent and `.brain/` records no route to recover a deleted Photo.
Both outcomes are stated: `Delete` confirms, and `Keep it` leaves the Photo in
the Gallery.

### 12. Reference

| # | Topic | Type | Rests on | Test | Figure |
| --- | --- | --- | --- | --- | --- |
| 12.1 | Which files become a Photo | reference | `REQ-GAL-010`; `.brain/glossary.md`, "Accepted image format" | `tests/test_validation.py` | none |
| 12.2 | Limits | reference | `REQ-GAL-001` c5 to c7; `REQ-GAL-017` c3; `REQ-GAL-003` c5; `09-reconciliation.md` limits table | `tests/test_upload_failures.py:91`; `tests/e2e/test_description_browser.py:106`; `tests/test_gallery.py:25` | none |

Topic 12.1 states the four accepted formats, that the format is judged by the
file's content rather than its extension, and that HEIC and camera RAW are
refused.

Topic 12.2 is one table of five rows: 25 MB per Photo, 30 files per Upload, 250
characters per description, 60 Thumbnails loaded at a time, and the four
accepted formats. Source: `09-reconciliation.md`.

**No keyboard shortcuts table.** The record holds two key actions, **Escape** in
the Larger view and `Ctrl+C` in the console window, and each is stated in the
topic it belongs to. A table of two entries restates them for no gain.

**Error messages live in chapter 13**, not here, which is the choice
`references/structure.md` asks for. The literal text goes where the reader in
trouble searches.

### 13. When something does not work

Organised by symptom, because a symptom is all the reader has. It opens with a
symptom index: one table linking each entry, with the literal message where
there is one.

| # | Topic | Type | Rests on | Test | Figure |
| --- | --- | --- | --- | --- | --- |
| 13.1 | What happens when part of an Upload fails | concept | `REQ-GAL-009` c1 to c5 | `tests/test_upload_failures.py:33,43,53,63`; `tests/e2e/test_upload_failures_browser.py:36,47,60` | none |
| 13.2 | Some of the files you chose are not in the Gallery | how-to | `REQ-GAL-009` c3, c4, c5 | `tests/e2e/test_upload_failures_browser.py:36,47,60` | none |
| 13.3 | A file was refused as not a supported image type | how-to | `REQ-GAL-010` c5 | `tests/test_validation.py`; `tests/api/test_photos_http.py` | `Images/08-upload-refused.png` |
| 13.4 | A file was refused as too large | how-to | `REQ-GAL-009` c6 | `tests/e2e/test_upload_failures_browser.py:71`; `tests/test_upload_failures.py:91` | none |
| 13.5 | MyGallery will not start: "Python was not found" | how-to | `README.md` "If something goes wrong" | none | none |
| 13.6 | MyGallery will not start: "Address already in use" | how-to | `README.md` "If something goes wrong" | none | none |
| 13.7 | The browser did not open | how-to | `README.md` "If something goes wrong" | `tests/test_config.py:12` | none |
| 13.8 | Windows blocked MyGallery from creating its Gallery folder | how-to | `AI guides/MyGallery/Planning/open-questions.md`, Q1. **Blocked on Q10** | none | none |
| 13.9 | The Gallery says it could not be read | how-to | `REQ-GAL-007` c5; `src/mygallery/templates/gallery.html:28`; `src/mygallery/web/api.py:79`. **Blocked on Q3 for its general case** | `tests/e2e/test_gallery_browser.py:48`; `tests/test_gallery.py:71` | none |

Topic 13.1 sits at the head of the chapter rather than at the head of chapter 7,
because it explains the mechanism behind 13.2, 13.3 and 13.4 and the reader
meets it while already in trouble. It states that the files that worked stay in
the Gallery and that each failure is named on the page with its reason.

Topics 13.3 and 13.4 quote the refusal text exactly, as
`<filename>: not a supported image type` and
`<filename>: file is too large (max 25 MB)`, so a search finds them.

Topic 13.8 is reachable from topic 4.1 and topic 5.1, as the Phase 1 gate
required, and it also sits first in the symptom index because it strikes on
first use.

Topic 13.9 quotes `The Gallery could not be read.` and points at 13.8 as the one
known cause. What the reader does when the cause is something else is Q3.

### 14. Glossary

Type: reference. Not a task.

Nine entries: the eight terms fixed in
`AI guides/MyGallery/Planning/terminology.md`, plus a row explaining that a
label is quoted as the application spells it. Each definition leads with the
definition and never restates the term.

The five interface labels that the glossary does not define are listed as
controls rather than as terms: `Upload photos`, `Choose files`,
`Description (optional)`, `Save description` and `Keep it`.

### Navigation

The manual opens with a hierarchical contents list. It carries **no separate
task index**, which is a departure from `references/structure.md`. In a single
file, every topic title is already a verb-first goal in the contents list, and
the reader's text search is the second way in, so a task index would be a second
copy of the contents list in a different order.

## 5. The quick start, and README.md

`README.md` is authoritative for every fact it states, because
`tests/test_start_instructions.py` and `tests/test_config.py:12` assert it and
nothing asserts a copy of it. `tests/conftest.py:59,70,82` parses three things
from it: the bullets under `## Before you start`, the bullets under
`## Run MyGallery`, and every `127.0.0.1:<port>` in the file. The tests then
require exactly one prerequisite naming Python, exactly one run step naming a
file that exists, and exactly one port.

### Who holds which fact

| Fact | Authoritative | In the quick start | In the manual |
| --- | --- | --- | --- |
| The one prerequisite, and `"Add python.exe to PATH"` | `README.md` "Before you start" | No. It names the README section | Yes, topics 3.1 and 3.2, copied verbatim |
| The start step and the file it names | `README.md` "Run MyGallery" | No. It names the README section | Yes, topic 4.1, copied verbatim |
| The address | `README.md` | No | Yes, topics 4.1 and 4.2, copied verbatim |
| How to stop MyGallery | `README.md` "Run MyGallery" | No | Yes, topic 4.3 |
| "Python was not found", "Address already in use", the browser not opening | `README.md` "If something goes wrong" | No. Its next-steps table links the README section | Yes, topics 13.5 to 13.7, copied verbatim |
| Photos stay on this machine | `README.md` "Your photos are yours", `REQ-GAL-011` c5 | No | Yes, topic 10.1 |
| The first Upload, from an open Gallery to a Thumbnail | **The quick start** | Yes, and this is its whole content | Yes, topics 5.1 and 7.1 |
| Every other fact about using MyGallery | The manual | No | Yes |

### What each document holds that the other does not

- **The quick start holds what `README.md` has none of:** the path from a
  displayed Gallery to the reader's first Thumbnail. `README.md` stops at the
  Gallery appearing and never mentions the Upload popup, `Choose files`,
  `Upload`, a description, Download or Delete.
- **`README.md` holds what the quick start deliberately omits:** the
  prerequisite, the start step, the address, how to stop, the three start-time
  failures, and the privacy statement.

### How the two are kept from contradicting each other

The rule is that **the quick start states no fact that `README.md` states**, and
names the README section instead. A document holding no start fact cannot
contradict a tested file, which removes the drift risk the client accepted at
the gate rather than managing it.

Two supporting rules:

1. **The manual is the set's only restatement of a README fact.** Topics 3.1,
   3.2, 4.1, 4.2, 4.3 and 13.5 to 13.7 copy their values from `README.md` rather
   than authoring them. The drift surface is one document, not two.
2. **The release check is named in the maintainer's note.** Read `README.md`
   under "Before you start", "Run MyGallery" and "If something goes wrong", and
   confirm those six topics still match. The comparison is recorded in
   `MyGallery User Manual - changelog.md`. Nothing tests the manual, so the
   check is a person's, and an automated guard asserting the manual's start
   topic against the README's bullets is a development option rather than a
   documentation decision.

This is the honest answer the Phase 2 brief invited: **the quick start is thin
on the start steps and points at `README.md` for them.** It is not thin overall,
because the first Upload is content no other short document holds.

### The quick start's sections

From `assets/quickstart-template.md`. Under roughly 900 words, and it carries no
figure: each of the eight captures is already placed in the manual, and a second
copy is a second thing to recapture at every release.

| Section | Holds | Rests on | Test |
| --- | --- | --- | --- |
| Title block | For: the user. Applies to: MyGallery 0.1.0 | `pyproject.toml` at `a00d0a4` | none |
| Opening line | The outcome, stated about the product: a photo on the reader's PC becomes a Photo they can see, describe, download and delete | `REQ-GAL-001`, `REQ-GAL-003` | none |
| Before you begin | MyGallery is installed and running. Names `README.md` "Before you start" and "Run MyGallery" and states no value from either | `README.md`; `tests/test_start_instructions.py` | `tests/e2e/test_boot.py:21` |
| 1. Open the Upload popup | `Upload photos` in the header, or the same control on an empty Gallery | `REQ-GAL-013` c1, c2 | `tests/e2e/test_uat_visual_browser.py:80,92` |
| 2. Choose your photos | `Choose files`, and the previews that confirm the choice | `REQ-GAL-013` c5; `REQ-GAL-015` c1 | `tests/e2e/test_description_browser.py:57` |
| 3. Upload them | Optionally `Description (optional)`, then `Upload`. Result: a Thumbnail card, newest first | `REQ-GAL-001` c10, c11; `REQ-GAL-003` c3 | `tests/e2e/test_upload.py:27`; `tests/e2e/test_gallery_browser.py:69,78` |
| What you just did | Names Photo, Gallery, Thumbnail and Upload, so the manual's words are already met | `AI guides/MyGallery/Planning/terminology.md` | none |
| Next steps | A table linking manual topics 8.2, 9.2, 10.2, 11.1 and chapter 13, and `README.md` "If something goes wrong" | the manual | none |

The quick start and the manual's topic 5.1 cover the same ground at different
lengths, which `references/structure.md` builds into the quick start's
definition. Both are drafted in the same pass, from one source pack and one
terminology list, so the terms and the labels cannot diverge.

## 6. File layout

**One Markdown file per document.** The Phase 1 estimate of 4,500 to 6,000 words
straddles the threshold in `references/structure.md`, and three things settle it
for one file:

- The deliverable is Markdown alone, since Phase 6 does not run, so the split's
  usual payoff of per-chapter build files does not arise.
- The outline links prerequisites rather than repeating them, so the manual
  carries many cross-references. In-file anchors survive a rename and a move;
  relative links across fourteen files do not.
- One reader reads it on screen beside the application. Fourteen files cost that
  reader a file hop on every cross-reference, in exchange for nothing.

| File | Holds |
| --- | --- |
| `AI guides/MyGallery/Documents/User Manual/MyGallery User Manual v1.0 draft 01.md` | The manual, chapters 1 to 14 |
| `AI guides/MyGallery/Documents/User Manual/MyGallery User Manual - changelog.md` | One row per change, from `assets/changelog-template.md` |
| `AI guides/MyGallery/Documents/User Manual/Images/` | The eight figures, already captured |
| `AI guides/MyGallery/Documents/User Manual/Logs/` | The lint report and the QA report for each draft |
| `AI guides/MyGallery/Documents/Quick Start/MyGallery Quick Start v1.0 draft 01.md` | The quick start |
| `AI guides/MyGallery/Documents/Quick Start/MyGallery Quick Start - changelog.md` | One row per change |
| `AI guides/MyGallery/Documents/Quick Start/Logs/` | Its lint and QA reports |

`AI guides/MyGallery/Documents/Quick Start/Images/` and both `Diagrams/` folders
stay empty: the quick start carries no figure, and no process in this product
branches or passes between owners, so no chart earns its place.

Drafts build to each document's `Drafts/`, and a confirmed release goes to
`AI guides/MyGallery/Deliverables/`.

## 7. Figures

All eight existing captures are placed, and no figure is planned that does not
exist. Each was taken in Chromium at 1280 by 860 in the light presentation,
which is assumption Q7.

| File | Topic | What it confirms |
| --- | --- | --- |
| `01-empty-gallery.png` | 5.1 | The first screen, its message and the `Upload photos` button |
| `02-upload-popup-empty.png` | 7.1 | The popup before files are chosen, with `Choose files` |
| `03-upload-popup-chosen.png` | 7.1 | The popup after files are chosen, with a preview, the description field and the counter |
| `04-gallery-with-photos.png` | 6.1 | The whole screen, for the region table |
| `05-thumbnail-card.png` | 6.2 | One card, with its `Download` and `Delete` controls |
| `06-larger-view.png` | 8.2 | The Larger view, with `Save description` and `Close` |
| `07-delete-confirmation.png` | 11.1 | The confirmation, with `Keep it` and `Delete` |
| `08-upload-refused.png` | 13.3 | A refusal, reading `notes.txt: not a supported image type` |

**No topic waits on a capture.** Production steps P1 and P2 in
`open-questions.md` are the two messages never reproduced, and neither topic
needs a figure: an error message is text, and
`references/style.md` excludes a screenshot for text the manual can quote. Topic
13.9 quotes `The Gallery could not be read.` and topic 13.4 quotes
`<filename>: file is too large (max 25 MB)`. P1 and P2 therefore block nothing
in this outline, and whether to capture them anyway is the writer's call at a
later pass.

Entries for the eight placed figures go in `Source pack/10-capture-list.json`,
whose `captures` array is empty and whose defaults of 1440 by 900 do not match
the captures taken. Correcting the defaults to 1280 by 860 is a Phase 3 step for
`manual-mechanic`.

## 8. What could not be placed

Every one of the 33 tasks has a topic. Two topics cannot be **completed** on
today's record, and both are recorded rather than written around.

| Topic | What is missing | Question | Owner |
| --- | --- | --- | --- |
| 13.8, Windows blocked MyGallery from creating its Gallery folder | What the reader does about it. The remedy is a path through Windows Security, which is in no repository and in no part of the source pack. Naming it would be inventing a menu path in another product | **Q10, new at Phase 2** | Client, with the development team |
| 13.9, The Gallery says it could not be read | What the reader does when the cause is not Controlled Folder Access. The message names no action | Q3, open since Phase 0 | Development team |

Both topics are drafted in Phase 3 with the facts the record holds: the symptom,
the literal message, and for 13.8 the cause and its evidence. The sentence
naming the remedy is left out of the draft until its question answers, and the
draft carries no marker of the gap.

Four assumptions still carry topics: A2 sets the register throughout, A3 keeps
the manual on screen rather than printed, A6 and Q9 carry topic 4.3, and Q7
carries every figure. A correction to any of them changes the named topic and
nothing else.
