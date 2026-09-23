# Documentation plan: MyGallery

**Date:** 2026-09-23\
**Author:** manual-analyst, Phase 1\
**Product version:** 0.1.0, from `pyproject.toml` at commit `a00d0a4`

Every fact below carries a reference to the source pack, `.brain/`, or `README.md`.
A statement with no reference is an assumption, and section 6 names its owner.

## 1. Source material

| Source | Available? | Notes |
| --- | --- | --- |
| Running software | Yes | Walked at commit `a00d0a4` on a throwaway Gallery folder, Playwright Chromium at 1280 by 860. `AI guides/MyGallery/Source pack/09-reconciliation.md` |
| Screenshots / recordings | Yes | Eight captures in `AI guides/MyGallery/Documents/User Manual/Images/`, covering the empty Gallery, both popup states, a populated Gallery, a Thumbnail card, the Larger view, the delete confirmation and a refused Upload |
| Spec, PRD, or ticket history | Yes | 19 requirements in `.brain/requirements/gal.yaml`, every one `verified` or `signed_off`, with acceptance criteria. 16 change records in `.brain/changes/`, six feedback records in `.brain/feedback/`, four ADRs in `.brain/decisions/` |
| Existing manual or help centre | Partly | `README.md` holds the start steps, three troubleshooting entries and a privacy statement. It is the closest thing to a user document and its "Before you start" section is load-bearing: `tests/test_start_instructions.py` asserts it names exactly one prerequisite |
| SME available for questions | Yes | The client is also the developer, recorded as KCB / DEV throughout `.brain/feedback/` |

The client's own words are in `.brain/requirements/ANSWERS.md`, which answers
17 decomposition questions plus four later rounds. Questions 1, 3, 4 and 6 of
this plan quote it rather than assuming.

**Gaps:** five questions stand open in `AI guides/MyGallery/Planning/open-questions.md`,
and this plan adds four more. Three of them block a topic outright: the Gallery
folder's location (Q4), what the reader does when the Gallery cannot be read
(Q3), and the Controlled Folder Access failure on first run (Q1). Two labels in
`02-labels.md` were evidenced from code and not reproduced in the running
application, and both stay in the capture list as P1 and P2.

## 2. Readers

| Reader group | What they do with the product | Existing knowledge | Frequency of use | Their document |
| --- | --- | --- | --- | --- |
| The user | Uploads, views, describes, downloads and deletes their own Photos on their own Windows 11 PC | Uses a phone camera and a web browser. Willing to install one thing once, given simple steps. No command line assumed | Daily to weekly, in short sessions beside the application | User manual |
| The maintainer | Develops and releases MyGallery | Python, pytest, Playwright, the `.brain/` record | Not a reader of this set | Out of scope. See section 7 |

**Primary reader:** the user. There is one reader group, and the record is
explicit about it rather than silent.

`.brain/glossary.md` fixes it as a definition:

> **The user**: the one person who uses MyGallery, on their own Windows 11 PC.
> There is no sign-in, no account, and no second user.

The client confirmed it in their own words (`.brain/requirements/ANSWERS.md`,
2026-09-18):

> Yes, it's just me, on my own PC. Nobody else uses it and I don't want to sign
> in. It only needs to work on this computer, not from other devices or over the
> internet.

`04-permissions.md` found no role, and `REQ-GAL-011` criterion 5 requires a
connection from another device to be refused. No second group reaches a screen
this group does not, so the set stays at one document.

### What they already know

The client named their platform and their tolerance for setup
(`.brain/requirements/ANSWERS.md`, 2026-09-18):

> I'm on Windows 11. I'm happy to install one thing once if you give me simple
> steps, like Python or Node.js. After that I want to start MyGallery by
> double-clicking a file or running one command, with nothing else to set up.

And how they expect to reach it:

> I'd like to open it in my web browser. I'm happy to start it on my PC and then
> go to an address like http://localhost in Chrome or Edge. I don't need a
> separate program window.

Three consequences for the vocabulary:

- The manual explains Python only as far as installing it, since `ADR-0003` makes
  it the single prerequisite and the application installs its own dependencies.
- The manual assumes no command line. `REQ-GAL-011` criterion 4 requires a single
  command or a single file to open, and `README.md` gives the file.
- Photography vocabulary needs no explanation. The client speaks of phone photos,
  JPG, folders and backups without prompting.

## 3. Task inventory

Thirty-two goals, built from the 19 requirements and the 75 end-to-end test
titles in `07-tasks.md` read together. Grouping into chapters is Phase 2 work,
and the goal area column is a proposal rather than an outline.

| # | Task | Reader group | Frequency | Content type | Goal area | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Install Python before the first run | The user | Once | how-to | Starting MyGallery | must |
| 2 | Start MyGallery | The user | Every session | how-to | Starting MyGallery | must |
| 3 | Stop MyGallery | The user | Every session | how-to | Starting MyGallery | must |
| 4 | Open the Gallery again while MyGallery is running | The user | Occasional | how-to | Starting MyGallery | should |
| 5 | Add your first Photo and see it in the Gallery | The user | Once | tutorial | Getting started | must |
| 6 | Add Photos to your Gallery | The user | Daily | how-to | Adding Photos | must |
| 7 | Add a batch of Photos in one Upload | The user | Weekly | how-to | Adding Photos | must |
| 8 | Choose files by dropping them on the Upload popup | The user | Occasional | how-to | Adding Photos | should |
| 9 | Check what you chose before you upload it | The user | Every Upload | how-to | Adding Photos | should |
| 10 | Describe a Photo as you upload it | The user | Every Upload | how-to | Adding Photos | should |
| 11 | Close the Upload popup without adding anything | The user | Occasional | how-to | Adding Photos | should |
| 12 | Find a Photo in the Gallery | The user | Daily | how-to | Looking at Photos | must |
| 13 | See a Photo at a larger size | The user | Daily | how-to | Looking at Photos | must |
| 14 | Close the Larger view and return to your place | The user | Daily | how-to | Looking at Photos | must |
| 15 | Change a Photo's description | The user | Occasional | how-to | Descriptions | must |
| 16 | Give a description to a Photo that has none | The user | Occasional | how-to | Descriptions | should |
| 17 | Where a description is shown, and who reads it | The user | Read once | concept | Descriptions | should |
| 18 | Download a Photo | The user | Weekly | how-to | Getting Photos back out | must |
| 19 | Back up your Gallery | The user | Monthly | how-to | Getting Photos back out | should |
| 20 | Delete a Photo | The user | Occasional | how-to | Removing Photos | must |
| 21 | Keep a Photo after starting to delete it | The user | Occasional | how-to | Removing Photos | must |
| 22 | Which files become a Photo | The user | Lookup | reference | What MyGallery accepts | must |
| 23 | Limits | The user | Lookup | reference | What MyGallery accepts | must |
| 24 | Where your Photos are kept, and who can reach them | The user | Read once | concept | What MyGallery accepts | should |
| 25 | What happens when part of an Upload fails | The user | Read once | concept | What MyGallery accepts | should |
| 26 | A file was refused as not a supported image type | The user | Occasional | how-to | When something does not work | must |
| 27 | A file was refused as too large | The user | Occasional | how-to | When something does not work | must |
| 28 | Some files in a batch did not go in | The user | Occasional | how-to | When something does not work | must |
| 29 | MyGallery will not start: "Python was not found" | The user | Rare | how-to | When something does not work | must |
| 30 | MyGallery will not start: "Address already in use" | The user | Rare | how-to | When something does not work | must |
| 31 | The browser did not open | The user | Rare | how-to | When something does not work | must |
| 32 | The Gallery says it could not be read | The user | Rare | how-to | When something does not work | could |

### Evidence for each task

| # | Requirements | Tests and labels |
| --- | --- | --- |
| 1 | REQ-GAL-011 c3 | `README.md` "Before you start"; `ADR-0003`; `tests/test_start_instructions.py:9,14` |
| 2 | REQ-GAL-011 c1, c4 | `tests/e2e/test_boot.py:21`; `tests/test_launcher.py:20,47`; `README.md` "Run MyGallery" |
| 3 | None | `README.md`: close the console window, or `Ctrl+C` in it. See new question Q9 |
| 4 | REQ-GAL-011 c1 | `tests/test_config.py:12`; `README.md` "The browser did not open" |
| 5 | REQ-GAL-001, REQ-GAL-003, REQ-GAL-007, REQ-GAL-011 | `tests/e2e/test_upload.py:27`; `tests/e2e/test_gallery_browser.py:69` |
| 6 | REQ-GAL-001 c10, REQ-GAL-013 c1 | `tests/e2e/test_upload.py:27`; `tests/e2e/test_uat_visual_browser.py:80` |
| 7 | REQ-GAL-001 c7, c8 | `tests/e2e/test_upload.py:40`; `tests/e2e/test_upload_failures_browser.py:36` |
| 8 | REQ-GAL-016 | `tests/e2e/test_description_browser.py:122`; `tests/e2e/test_uat_visual_browser.py:201` |
| 9 | REQ-GAL-015 | `tests/e2e/test_description_browser.py:57,71,195`; `tests/e2e/test_upload_preview_size_browser.py:54,61,70` |
| 10 | REQ-GAL-017 c1 to c5 | `tests/e2e/test_description_browser.py:83,96,106,172,182` |
| 11 | REQ-GAL-019 | `tests/e2e/test_uat_visual_browser.py:127,146,158` |
| 12 | REQ-GAL-003 c3, c5, c6 | `tests/e2e/test_gallery_browser.py:78,89,98` |
| 13 | REQ-GAL-004 c1, c2 | `tests/e2e/test_larger_view_browser.py:31,41,59`; `tests/e2e/test_larger_view_small_photo_browser.py:52,74` |
| 14 | REQ-GAL-004 c3, c4, c5, c8; REQ-GAL-014 c2 | `tests/e2e/test_larger_view_browser.py:72,84,95,118`; `tests/e2e/test_larger_view_actions_browser.py:48` |
| 15 | REQ-GAL-017 c7, c8; REQ-GAL-002 c9 | `tests/e2e/test_description_browser.py:160`; `tests/test_description.py:30` |
| 16 | REQ-GAL-002 c8 | `tests/test_description.py:41` |
| 17 | REQ-GAL-018 | `tests/e2e/test_description_browser.py:135,147`; `tests/e2e/test_uat_visual_browser.py:187` |
| 18 | REQ-GAL-006; REQ-GAL-003 c13 | `tests/e2e/test_download_browser.py:31,42,53`; `tests/e2e/test_card_actions_browser.py:71` |
| 19 | REQ-GAL-008 c4 | `tests/test_durability.py:44,53`; `ADR-0004`. Blocked by Q4 and Q5 |
| 20 | REQ-GAL-005; REQ-GAL-003 c14, c15 | `tests/e2e/test_delete_browser.py:34,44,70,83`; `tests/e2e/test_card_actions_browser.py:88,112` |
| 21 | REQ-GAL-005 c5 | `tests/e2e/test_delete_browser.py:57`; `tests/e2e/test_card_actions_browser.py:101` |
| 22 | REQ-GAL-010 | `.brain/glossary.md`, "Accepted image format"; `tests/test_validation.py` |
| 23 | REQ-GAL-001 c5 to c7; REQ-GAL-017 c3; REQ-GAL-003 c5 | `09-reconciliation.md` limits table |
| 24 | REQ-GAL-008; REQ-GAL-011 c5 | `ADR-0004`; `tests/test_binding.py:23`; `tests/e2e/test_upload.py:20`; `README.md` "Your photos are yours" |
| 25 | REQ-GAL-009 c1 to c4 | `tests/test_upload_failures.py:33,43,53,63` |
| 26 | REQ-GAL-010 c5 | `08-upload-refused.png`, reading `notes.txt: not a supported image type` |
| 27 | REQ-GAL-009 c6 | `tests/e2e/test_upload_failures_browser.py:71`; `tests/test_upload_failures.py:91`. Capture outstanding as P2 |
| 28 | REQ-GAL-009 c3, c4, c5 | `tests/e2e/test_upload_failures_browser.py:36,47,60` |
| 29 | None | `README.md` "If something goes wrong" |
| 30 | None | `README.md` "If something goes wrong" |
| 31 | None | `README.md` "If something goes wrong" |
| 32 | REQ-GAL-007 c5 | `templates/gallery.html:28`; `src/mygallery/web/api.py:79`. Blocked by Q3 |

### Tasks that Phase 2 may merge

Four pairs split a single reader goal, and the outline decides whether each pair
is one topic with a branching step or two:

| Pair | The case for merging |
| --- | --- |
| 6 and 7 | One Upload adds one file or thirty. The popup and the steps are the same |
| 13 and 14 | Opening the Larger view and leaving it is one visit |
| 15 and 16 | The steps are identical whether or not a description is already there |
| 20 and 21 | The confirmation is one decision with two outcomes |

Task 5 is not a duplicate of 2, 6 and 12. It is the tutorial content kind, a
single managed path to first success, and it branches nowhere.

**First-use blockers:** tasks 1, 2 and 4. `REQ-GAL-011` is the only requirement
at `signed_off` and the only one that fails silently in the reader's hands:
nothing else in the manual is reachable until the Gallery is on screen. Task 5
follows them and produces the first Photo.

Open question Q1 belongs in this group and is not yet a task. Windows Defender
Controlled Folder Access blocks the application from creating `Pictures\MyGallery`
on a default Windows 11 configuration, and the reader is given `WinError 2`
rather than a refusal. It strikes on first run, before the reader has done
anything. Whether the manual documents it or the application is changed is a
decision for the client with the development team.

**Known failure modes:** eight, in three families.

| Family | What the reader sees | Evidence |
| --- | --- | --- |
| A file is refused | `<filename>: not a supported image type` | `08-upload-refused.png` |
| A file is refused | `<filename>: file is too large (max 25 MB)` | `validation.py:20-26`. Not reproduced; P2 |
| A file is refused | HEIC and camera RAW are refused, which the client asked for | `.brain/glossary.md`; REQ-GAL-010 c4 |
| Part of a batch fails | The files that worked stay, and each failure is named with its reason | REQ-GAL-009 c3 to c5 |
| MyGallery will not start | "Python was not found" | `README.md` |
| MyGallery will not start | "Address already in use" | `README.md` |
| MyGallery started, nothing opened | The browser did not open | `README.md` |
| The Gallery will not load | `The Gallery could not be read.` | `templates/gallery.html:28`. The message names no action; Q3 |

## 4. Deliverable set

Proposed here in Phase 1, and settled at the Phase 1 gate on 2026-09-23. The
table below is the Phase 1 recommendation, and the gate decisions that follow it
override two of its rows.

### Settled at the Phase 1 gate, 2026-09-23

| Decision | Outcome |
| --- | --- |
| Document set | **User manual and quick-start guide.** The client chose the quick start against the recommendation below |
| Delivery | **Markdown only.** Phase 6 does not run for v1.0, which closes P3 |
| Blocked topics | Answered rather than deferred. Q1, Q4, Q5, Q6 and Q8 are settled in `AI guides/MyGallery/Planning/open-questions.md` |

**The quick start is produced, and the drift risk is accepted.** The
recommendation below was against it, because `README.md` already holds the start
steps and `tests/test_start_instructions.py` asserts them. That risk does not go
away by being accepted, so the quick start is written **from** `README.md`
rather than beside it, and Phase 2 records which file is authoritative where the
two describe the same step. A quick start that contradicts a tested README is
the specific failure to design against.

Two tasks changed at the gate:

- **Back up your Gallery** is unblocked. The manual names `Pictures\MyGallery`
  and says its Photos can be copied. `MYGALLERY_DIR` stays out, so the topic
  describes copying the folder and not moving it.
- **The Controlled Folder Access failure** becomes a troubleshooting task, and
  the task inventory grows from 32 to 33. It is a first-use blocker, so its
  entry is findable from the starting chapter and not only from troubleshooting.

Q7 and Q9 were not put to the client and carry the writer's assumption: figures
are light at 1280 by 860, and both documented ways of stopping MyGallery are
supported.

### The Phase 1 recommendation

MyGallery is one screen used by one person with no sign-in, so the restraint is
the point: five of the seven candidate documents earn no place, and two of those
five become chapters instead.

| Document | Producing? | Why / why not |
| --- | --- | --- |
| User manual | Yes | It is the only document the reader group needs, and it carries all 32 tasks. Skeleton from `references/structure.md`, adapted for an application with no install beyond Python and no roles |
| Quick-start guide | Recommended against. **Overridden at the gate: it is produced** | `README.md` already holds the start steps, and `tests/test_start_instructions.py` tests it. A second first-success document would drift from a tested file, and the reader who will not open the manual already has the README |
| Troubleshooting & FAQ | As a chapter | Eight failure modes exist, which is enough content and not enough to split. One reader searching two files for eight entries is worse served than one reader searching one |
| Administrator guide | No | There is no administrator. `04-permissions.md` found no role, `.brain/glossary.md` records no sign-in and no second user, and `REQ-GAL-011` c5 refuses other devices |
| Release notes | No | The reader installs once and is not given a release cadence. Nothing in `.brain/` documents an upgrade path. Revisit when a second version reaches them |
| Glossary | As a chapter | `.brain/glossary.md` fixes nine terms, which passes the standalone threshold of eight. The manual is small enough that a separate file costs the reader a hop for no gain |
| File reference | No | The maintainer is not a reader of this set, and `.brain/` already serves them |

Two chapters the skeleton offers are dropped, and one is kept against the odds:

- **Advanced tasks** is dropped. No requirement describes automation, bulk
  operations, scripting or an integration, and `01-routes.md` puts the
  application programming interface out of scope.
- **Administration** is dropped, for the reason in the table.
- **The interface tour** is kept. One screen makes it cheap, and every later
  instruction that names the header, a Thumbnail card, the Upload popup or the
  Larger view depends on the tour having named them first.

**Format and delivery:** Markdown, in
`AI guides/MyGallery/Documents/User Manual/`. The inventory estimates 4,500 to
6,000 words, which straddles the threshold at which `references/structure.md`
splits a manual into one file per chapter, so Phase 2 settles the file layout
against the approved outline rather than now. Drafts build to that document's
`Drafts/`, and the release to `AI guides/MyGallery/Deliverables/` once the user
confirms it final. Whether Phase 6 runs at all is P3 in
`AI guides/MyGallery/Planning/open-questions.md`.

## 5. Decisions and conventions

- **Client profile:** none. `python scripts/client_profile.py list "AI guides/Clients"`
  reports "No client profiles in AI guides\Clients." The directory exists and
  holds only its `README.md`. The house defaults in `references/style.md` apply
  in full, and no rule is relaxed.
- **House verb style:** device-neutral. `select`, `open`, `enter`, `turn on`,
  `clear`. Never `click` or `tap`, which
  `AI guides/MyGallery/Planning/terminology.md` already records.
- **Terminology clashes:** one, and it is inside a label rather than a spelling.
  The empty-Gallery message reads `No photos yet. Click Upload to add your first
  photos.`, so a verbatim quotation of it carries `Click` into a manual whose own
  prose says `select`. The label is quoted exactly and the conventions section
  records why. The same message names a button `Upload` while the button reads
  `Upload photos`, which is new question Q6. No label carries a US spelling, so
  the Australian English clash that `02-labels.md` looked for does not arise.
- **Screenshot policy:** eight captures already exist in
  `AI guides/MyGallery/Documents/User Manual/Images/`, taken during the Phase 0
  walkthrough in Chromium at 1280 by 860 in the light presentation. They are the
  baseline, and `10-capture-list.json` defaults to 1440 by 900 with
  `colorScheme: light`, which does not match them. The client's own screenshots
  in `.brain/feedback/FB-0005` and `FB-0006` are described as the dark theme.
  New question Q7 settles the one theme and one viewport that every figure uses.
  Two captures stand outstanding as P1 and P2.
- **Localisation:** not needed. `02-labels.md` records that the application has
  no internationalisation catalogue, so the template is the only source of a
  label.
- **Compliance:** no standard, tender requirement or accessibility level is named
  anywhere in `.brain/`. Phase 5 maps the deliverable to the structure and
  quality attributes of ISO/IEC/IEEE 26514 and IEC/IEEE 82079-1, which is an
  alignment rather than a certification.

## 6. Assumptions

Things assumed in the absence of a confirmed answer. A1 to A4 were recorded at
Phase 0 and are carried forward unchanged; A5 and A6 are new at Phase 1.

| # | Assumption | Impact if wrong | Who can confirm |
| --- | --- | --- | --- |
| A1 | There is one reader group: the one person who uses MyGallery on their own PC. No administrator, no installer, no second user | The document set grows a second document, and the task inventory splits | Client |
| A2 | That reader is not technical, and the manual assumes no command line | Register and depth change throughout, and the Python steps shorten | Client |
| A3 | The manual is read on screen beside the application, not printed | Phase 6 runs, figure numbers and captions are needed, and section numbers replace links | Client |
| A4 | The application programming interface is out of scope, since no reader calls it | A reference chapter of routes is added for a group not yet named | Development team |
| A5 | The developer material in `README.md` under "Working on MyGallery", and everything in `.brain/`, is out of scope for this set | A file reference is needed for the maintainer group | Client, with the development team |
| A6 | `Ctrl+C` in the console window, and closing that window, are the supported ways to stop MyGallery | Task 3 documents an unsupported action. No acceptance criterion covers stopping | Development team |

## 7. Out of scope

| Not covered | Where the reader goes instead |
| --- | --- |
| Every `/api/` route, and `/static/<path:filename>` | Nowhere. `01-routes.md` records that no supported way exists for a reader to call one |
| The `MYGALLERY_DIR` environment variable | Held until Q5 answers whether moving the Gallery folder is a supported feature |
| Developing, testing or releasing MyGallery | `README.md` under "Working on MyGallery", and `.brain/index.md` |
| How Thumbnails are generated and stored | `ADR-0004`. The reader never reaches a Thumbnail as a file, and `.brain/glossary.md` records that a Thumbnail cannot be deleted alone |
| Any grouping of Photos below the Gallery | Nowhere. `.brain/glossary.md` forbids inventing an album or a collection, and the brief describes none |
| Recovering a deleted Photo | Nowhere. Deletion is permanent by the client's own answer, and the manual says so in the Delete topic rather than offering a route |
| Reaching MyGallery from a phone, a tablet or another computer | Nowhere. `REQ-GAL-011` c5 refuses the connection, and the concept topic on task 24 states it |
