# QA report: MyGallery User Manual v1.0 draft 01, and MyGallery Quick Start v1.0 draft 01

**Phase 5, 2026-09-23.** Worked against `references/qa-checklist.md`, sections 1
to 12, with sections 1 to 8 of `references/style.md` as the house rule.

**Files reviewed**

| File | Words |
| --- | --- |
| `Documents/User Manual/MyGallery User Manual v1.0 draft 01.md` | 4,706 |
| `Documents/Quick Start/MyGallery Quick Start v1.0 draft 01.md` | 325 |

**Reviewed against:** `Planning/outline.md`, `Planning/documentation-plan.md`,
`Planning/terminology.md`, `Planning/open-questions.md`,
`Source pack/02-labels.md`, `Source pack/09-reconciliation.md`,
`Source pack/05-errors.md`, `Source pack/06-config-limits.md`,
`.brain/requirements/gal.yaml`, `README.md`, and the draft's lint report.

A finding marked **verified** was checked against a named file and line. A
finding marked **inferred** rests on reading rather than on a citation, and is
reported rather than dropped.

---

## Summary

The draft is accurate where it is hardest to be accurate: all thirty-three
tasks are present in the topics the outline assigns them, every quoted label
matches `02-labels.md` character for character, no label is paraphrased, and
no sentence in either document depends on Q2, Q3, Q11 or Q12. The quick start
holds the rule that governs it, stating no fact `README.md` states.

The one change that would improve it most is **qualifying the three claims the
acceptance criteria do not support**: the downloaded filename (C1), the preview
width (C4), and the Gallery folder's contents (C3). Each reads as a guarantee,
and a reader who meets the exception loses trust in the parts that are right.

Two findings are structural and cheap to fix: the drag-and-drop procedure is an
unnumbered heading that is absent from the contents list and has taken topic
7.1's **See also** block with it (S1), and no chapter carries an opener (S2).

**Counts:** 9 critical, 13 structural and procedural, 13 style. 35 findings.
None is unsafe. None is a fabricated label, path, message or shortcut.

---

## Findings

### Critical: wrong, unverifiable, or unsafe

| # | Location | Finding | Confidence | Severity | Fix |
| --- | --- | --- | --- | --- | --- |
| C1 | Manual 10.2, lines 532-533 and 543-544; 10.1, lines 515-516 | The downloaded filename is promised three times without its exception. `REQ-GAL-006` c5 states that where a Photo's uploaded filename cannot be used as delivered, the delivered file's name ends in the extension of that Photo's image format. The manual says only "under the filename you uploaded it with" | Verified against `gal.yaml` REQ-GAL-006 c4, c5 | High | Qualify once, in 10.2's opening sentence, and leave the result statement observable: "usually under the filename you uploaded it with". State the fallback in 12.2 or in 10.2's **See also** |
| C2 | Manual 13.6, lines 758-759 | The result reads "Your Gallery is shown, either in the window already open or in your browser". The only window named in the preceding step is the black window MyGallery opened, which is a console and never shows the Gallery | Verified against `README.md` "Run MyGallery" and manual 4.1 step 1 | High | Name the black window as confirmation that MyGallery is running, and make the Gallery's appearance the browser's result alone |
| C3 | Manual 10.1, lines 510-511 | "That folder holds every Photo you have uploaded, the Thumbnails MyGallery renders from them, and the index MyGallery reads to show them." The Thumbnails folder and the index are in no part of the source pack. Section 7 of the documentation plan puts "How Thumbnails are generated and stored" out of scope. Only `Pictures\MyGallery` itself is authorised, by Q4 | Verified: true against `src/mygallery/config.py:29` (`INDEX_PATH`, `THUMBNAIL_DIR`), and absent from every file in `Source pack/` | High | Cut the Thumbnails and the index, or harvest them into the pack and lift the out-of-scope row. The sentence the reader needs is that the Photos are there as ordinary files |
| C4 | Manual 7.1 step 2, lines 328-329 | "A preview of each chosen file appears in the popup, as wide as the **Description (optional)** field." `REQ-GAL-015` c4 conditions that width on a file at least as wide as the field, and c6 says a narrower file's preview is centred instead | Verified against `gal.yaml` REQ-GAL-015 c4, c6 | Medium | Drop the width clause from the step. It is a layout fact the reader does not act on |
| C5 | Manual 3.1, lines 128-132; 4.1 step 1, line 171 | "What you need" names the operating system, Python and the browser, and is silent on a copy of the application, which `REQ-GAL-011` c1 lists as a precondition of its own. Step 1 of 4.1 then opens `scripts/start.cmd` with no folder to find it in. A reader who has not been handed the folder cannot complete chapter 4 | Verified against `gal.yaml` REQ-GAL-011 c1, and `open-questions.md` Q11 | High | Q11 owns this and is open, so the draft was right not to invent it. Escalate Q11 rather than fixing it here. The first-use path is blocked until it answers |
| C6 | Manual 9.2 step 1, line 467; 9.3 step 1, line 492 | Both say "a description of up to 250 characters" and stop. `REQ-GAL-017` c3 states that typing or pasting more than 250 leaves the field holding 250 and does not refuse the Upload. A reader who pastes 300 characters is silently truncated and the manual does not say so | Verified against `gal.yaml` REQ-GAL-017 c3 | Medium | One sentence in 9.2: the field stops at 250 characters and the Upload is not refused for length. Link it from 9.3 rather than repeating it |
| C7 | Manual 10.3, lines 559-561 | "In File Explorer, copy the files in `Pictures\MyGallery` to another location." `config.py` puts the Photos in a `photos` subfolder, with `thumbnails` and `index.db` beside it, so copying the files **in** that folder copies none of the Photos. The manual's own 10.1 lists three kinds of content there | Inferred from `src/mygallery/config.py:26-29`. The source pack does not record the folder's structure | Medium | Say copy the folder rather than the files in it, and confirm the structure into the pack before the next release |
| C8 | Manual 13.8, lines 786-789 | "Controlled folder access, part of Windows Security, is turned on and is stopping MyGallery from creating its Gallery folder." The manual asserts the reader's machine state as fact. Q1 evidences it on the build machine, not on theirs | Verified against `open-questions.md` Q1 | Medium | Write it as the condition to check: "This happens where Controlled folder access is turned on." The remedy steps then follow unchanged |
| C9 | Manual 13.3, line 710; 13.4, line 726 | Both results read "The file is accepted as a Photo". Each fix addresses one of the two refusal reasons, so the result holds only where the file also passes the other check | Verified against `gal.yaml` REQ-GAL-009 c6 and REQ-GAL-010 | Low | Make the result the observable one: a new Thumbnail card appears in the Gallery |

### Structural: coverage, organisation, content typing

| # | Location | Finding | Confidence | Severity | Fix |
| --- | --- | --- | --- | --- | --- |
| S1 | Manual line 343, and the contents list at lines 19-21 | "Choose files by dropping them on the popup" is an unnumbered `###`, a peer of 7.1 and 7.2 rather than a subsection of 7.1, and it appears nowhere in the contents list. Topic 7.1's **See also** block (lines 356-361) now sits after it and reads as the drop procedure's, although it links 7.2, 9.2, 12.2 and 13.1, which are 7.1's. Task 8 is reachable only by text search | Verified: heading levels and contents list checked mechanically; 0 of 31 `###` headings for this one is numbered or listed | High | Demote it to `####` under 7.1, or number it 7.1a and add it to the contents list. Move the **See also** block back above it |
| S2 | Manual, every `##` from 3 to 14 | No chapter carries an opener. Each chapter heading is followed immediately by a topic heading or a table. Chapter 2 is the only one with prose of its own, and chapter 13's symptom table has no lead sentence. `references/style.md` §Openers and closers names the chapter opener as a required element, and `references/structure.md` gives chapters 2, 5, 9 and 10 content of their own | Verified: 32 headings enumerated, 12 chapters checked | Medium | One line per chapter, written about the subject rather than the document, as the style exception requires |
| S3 | Manual lines 266 and 268 | Chapter 6 and topic 6.1 carry the identical title "The Gallery screen". Two headings at two levels with one title, and two anchors that differ only by a digit | Verified | Medium | Retitle the chapter around the goal, or fold 6.1's content directly under the chapter heading and keep 6.2 as the only topic |
| S4 | Manual 13.2, lines 673-693 | The topic duplicates 13.1 and adds no fact. 13.1 already states that each failed file is named on the page with its reason; 13.2's whole procedure is to read that. Its result, "You know which files were not added, and why", describes the reader's state rather than the product's, which `references/style.md` bans in the same family as "You should now understand" | Verified against 13.1, lines 657-659 | Medium | Fold 13.2 into 13.1 and keep its title as a symptom-index row pointing there. Task 28 is then still covered |
| S5 | Manual 13.3, lines 702-704 | The paragraph restates 12.1 in full, then links to 12.1. Three facts told twice: the four formats, the renamed extension, and HEIC and camera RAW | Verified against 12.1, lines 615-617 | Low | Cut to the link. 12.1 is one screen away |
| S6 | Manual 13.8 line 783 and 13.9 line 810 | Both topics open with the same quoted message in the same construction, and 13.9 carries no procedure and no result. 13.9 is a pointer to 13.8 | Verified. The shape follows the outline's plan, given Q3, so the finding is on the shape rather than on the decision | Medium | Keep 13.9 as a symptom-index row only, until Q3 answers and gives it a general case of its own |
| S7 | Manual 6.2 table, line 296 | "The Photo's Thumbnail. Select it to see the Photo at a larger size." A reference table carrying an instruction. `references/structure.md` §9 holds reference to stating and describing, with no instruction | Verified | Low | Cut the instruction. The **See also** already links 8.2 |
| S8 | Manual 8.1, lines 392-393 | "Optional: Scroll to the end of what is loaded. Further Thumbnails load as you reach it, rather than a numbered page control." The reader performs no optional action here. This is reference content about how the Gallery loads, in a task topic | Verified against `gal.yaml` REQ-GAL-003 c5, c6 | Low | Move it into the topic's opening paragraph as a statement, or into 12.2 beside the 60-Thumbnail row |
| S9 | Manual 7.1 step 2, lines 330-331 | The optional sub-bullet "Choose a batch of files" repeats what step 2 already instructs. The rest of it is a behaviour note about the popup's height | Verified | Low | Cut the sub-bullet. The batch limit is already in the topic's first paragraph |
| S10 | Manual 9.1, line 448 | "The Gallery holds one set, ordered by Upload time with the most recent Photo first." The third telling of the ordering, after 6.1 (line 280) and 8.1 (lines 386-387) | Verified | Low | Cut it and link 8.1 |
| S11 | Manual 13.1, line 653 | "One Upload carries up to 30 files" repeats 7.1's opening fact verbatim in substance | Verified against line 314 | Low | Cut the clause. The chapter is reached by a reader who is already past the Upload |
| S12 | Both documents | No way is documented for a reader to report an error in the manual, which `references/qa-checklist.md` §9 asks for. Chapter 12 "Support and feedback" was dropped for want of a recorded channel, and the outline argues the drop, but nothing tells a reader what to do with a wrong instruction | Verified against `outline.md` §2 and `documentation-plan.md` §4 | Low | Raised as **Q13** in `open-questions.md`. It needs a channel from the client, not a sentence from the writer |
| S13 | Manual 12.1, lines 608-613 | A one-column table of four rows is a list. `references/style.md` §Markdown conventions keeps tables for more than two parallel attributes | Verified | Low | Make it a sentence: the accepted formats are JPEG, PNG, GIF and WebP. 12.2 already carries the same row |

**Procedures and results.** Five procedures end in a statement the reader cannot
check. `references/style.md` calls the result statement the element that most
decides whether the reader trusts the document, so these are reported
individually.

| # | Location | Finding | Confidence | Severity | Fix |
| --- | --- | --- | --- | --- | --- |
| P1 | Manual 9.3, lines 497-498 | "The Photo carries the description you entered, and its Thumbnail's alt text changes with it." Alt text is invisible, and nothing named on screen confirms the save. This is the procedure whose result the reader most needs | Verified. `09-reconciliation.md` supports an observable check: the Larger view's field carries that Photo's description | Medium | Make the result the reopened Larger view holding the new text |
| P2 | Manual 9.2, lines 472-474 | "Each Photo added by that Upload carries the description you entered." Same problem, and the second sentence is a qualification rather than a result | Verified | Medium | Point at the Larger view as the check, and move the no-description sentence above the steps |
| P3 | Manual 4.3, line 220 | "MyGallery stops running." Asserted | Verified | Low | The observable is the black window closing and the address no longer answering |
| P4 | Manual 3.2, line 151 | "Python 3.12 or later is installed on your PC." Asserted | Verified | Low | The observable is the installer reporting success |
| P5 | Manual line 353 | "The dropped files are chosen for the Upload, the same as files chosen with **Choose files**." The observable is the previews appearing | Verified against `gal.yaml` REQ-GAL-016 c1 | Low | Make the previews the result |

### Style and consistency

Section 1a was worked heading by heading over both documents. The first and last
sentence of each of the 32 manual headings and 6 quick-start headings was read on
its own. Findings are reported per section, as §13 requires.

| # | Location | Finding | Confidence | Severity | Fix |
| --- | --- | --- | --- | --- | --- |
| T1 | Manual 1, line 54 | "MyGallery 0.1.0 on Windows 11 is what this manual describes." The permitted scope statement, but written about the document. The style exception requires it as a statement about the subject: "Phase 0 runs where your team owns the code", not "This chapter covers Phase 0" | Verified against `references/style.md` §Openers and closers | Low | "MyGallery 0.1.0 runs on Windows 11." The coverage sentence that follows it already does the scope work |
| T2 | Manual 3.1, line 126 | "MyGallery needs the following before it will start." Pre-announces the table, which `references/style.md` §Concision names directly | Verified | Low | "MyGallery runs on Windows 11, needs Python 3.12 or later, and is used in Chrome or Edge." Then the table |
| T3 | Manual 4.2, line 188 | "You can open your Gallery again in your web browser at any time while MyGallery is running" restates the heading it sits under | Verified | Low | Lead with the fact the reader came for: the address stays live for the whole session |
| T4 | Manual 6.1, lines 270-271 | "...and its regions are named the same way throughout this manual." Meta-commentary about the document, in the first sentence | Verified | Low | Cut the clause |
| T5 | Manual 14, lines 835-837 | "These controls are named throughout this manual, but are not concepts of their own." Framed about the document. It carries the five labels, so it stays | Verified | Low | Reframe as a statement about the controls |
| T6 | Quick start, lines 43-44 | "What you just did" opens by replaying the three steps. The template asks the section to name the concepts the reader has met, which the second sentence does | Verified against `assets/quickstart-template.md` | Low | Cut the first sentence and lead with the concepts |
| T7 | Quick start, lines 38-39 | "A new Thumbnail card appears in your Gallery for each photo you added, with the most recently added first." Two slips: the images are Photos by then, and the manual says "most recently uploaded first" everywhere. `terminology.md` bans "add files" as a synonym for Upload | Verified against manual lines 340-341 and `terminology.md` | Medium | "...for each Photo you uploaded, with the most recently uploaded first" |
| T8 | Manual 8.2 line 404, and 14 line 828 | "Activating a Photo's Thumbnail" against "select the Photo's Thumbnail" in the step beneath it. Two verbs for one action. "Activate" is inherited from `.brain/glossary.md` through `terminology.md`, so the clash is the project's rather than the drafter's | Verified against `terminology.md` | Low | Use **select** in prose and record the glossary's "activate" in the conventions section, the way the `Click` clash is already recorded |
| T9 | Manual lines 374 and 420 | "select the **Close** cross" appends the control type, which `references/style.md` forbids. It is needed here, because two controls carry the label `Close` | Verified against `02-labels.md` Upload popup and Larger view | Low | Keep it and record the two `Close` controls in the conventions section |
| T10 | Manual lines 615, 697, 702 | Three sentences run to 26, 29 and 30 words. The linter reported them as INFO and the caller did not disposition them. All three are genuine | Verified against the lint report | Low | Split each. 697 also says the same thing twice: the reason is quoted, then the example repeats it |
| T11 | Manual 6.2, line 300 | "**Download** and **Delete** are the same width." An acceptance criterion (`REQ-GAL-003` c12) with nothing in it for a reader | Verified | Low | Cut. The rest of the sentence, that both are shown without resting the pointer on a card, is worth keeping |
| T12 | Manual 5.1 step 2, line 241 | "On the empty Gallery, read..." Reading is not an action toward the goal, and the step's committing action is in step 3 | Verified | Low | Make it the visible reaction of step 1, as `references/style.md` asks: state the reaction in the same step as the action |
| T13 | Manual, throughout | "your web browser" (lines 162, 173, 188, 197) against "your browser" (line 759) and "the browser" (lines 184, 646) | Verified | Low | One form. "your web browser" is the one the manual leads with |

---

## Checks that passed

Recorded so the caller can see what was examined rather than inferred from
silence.

| Check | Result |
| --- | --- |
| **Coverage, all 33 tasks** | **Complete.** Every task in `outline.md` §2 is present in the topic it assigns, and nothing extra is documented. Mapping verified one by one: 1→3.2, 2→4.1, 3→4.3, 4→4.2, 5→5.1, 6 and 7→7.1, 8→the drop subheading, 9→7.1 step 3, 10→9.2, 11→7.2, 12→8.1, 13 and 14→8.2, 15 and 16→9.3, 17→9.1, 18→10.2, 19→10.3, 20 and 21→11.1, 22→12.1, 23→12.2, 24→10.1, 25→13.1, 26→13.3, 27→13.4, 28→13.2, 29→13.5, 30→13.6, 31→13.7, 32→13.9, 33→13.8 |
| **Labels quoted exactly** | **Clean.** Every quoted label checked character by character against `02-labels.md`: `MyGallery`, `Upload photos`, `Choose files`, `Description (optional)`, `Description`, `Save description`, `Close` (both controls), `Upload`, `Download`, `Delete`, `Keep it`, `Are you sure you want to delete this photo?`, `No photos yet. Click Upload photos to add your first photos.`, `The Gallery could not be read.`, `18/250`. The two refusal messages match `09-reconciliation.md`. The six Windows Security labels match the verified table in `open-questions.md` Q10, ampersand and US spelling included. **No label is paraphrased or misquoted** |
| **Quoted labels confirmed at source** | The empty-Gallery message and the unreadable-Gallery message were re-read at `src/mygallery/templates/gallery.html:23-29` and match the manual exactly |
| **No invention** | No fabricated label, menu path, field name, default, error message, shortcut or system requirement. The two facts outside the pack boundary are C3 and 10.1's "inside your own user folder", both true against `config.py` and neither recorded in the pack |
| **Open questions Q2, Q3, Q11, Q12** | **No sentence in either draft depends on an unanswered question.** Q2: 3.1 names Windows 11 with no build. Q3: 13.9 claims one known cause, which is what the record supports. Q11: the gap is left open, which is C5. Q12: resting the pointer on a Thumbnail is mentioned nowhere, and 6.2 and 9.1 state the alt text alone |
| **Quick start against `README.md`** | **The rule holds.** The quick start states no prerequisite, no start file, no address, no first-run delay, no way to stop, no start-time failure and no privacy statement. Its **Before you begin** names the two README sections and quotes no value from either |
| **Content typing** | No task topic carries conceptual explanation. The three concept topics, 9.1, 10.1 and 13.1, carry no numbered instructions. The tutorial, 5.1, has a single path with no branch or option. One reference table carries an instruction, which is S7 |
| **Markers** | None. No `[VERIFY:]`, `TODO`, `<!-- CAPTURE -->` or open-questions section in either file |
| **Cross-references** | **All resolve.** Every in-file anchor checked mechanically against the heading slugs: 0 unresolved, 0 duplicate slugs. The quick start's five relative links carry the correct anchors, and their drift risk is already P5 |
| **Figures** | All eight captures placed, each with alt text naming what it conveys. No information sits only in an image |
| **Accessibility** | No directional language. No element identified by appearance or colour. Heading levels sequential. Real tables with header rows, real lists |
| **House style, mechanical** | 0 em dashes, 0 en dashes, 0 ellipses, 0 exclamation marks, 0 US spellings in prose, in either file |
| **Register** | No greeting, enthusiasm, reassurance, invitation, hedge or condescension. No first person. No banned AI-marker word or phrase |
| **Destructive actions** | 11.1 carries a **Warning** inside the step it governs, stating the hazard, the consequence and that no recovery exists. 10.1 states it a second time, which is acceptable duplication for a destructive action |
| **Callouts** | One in the whole manual, of the five permitted types. None adjacent. None carries information required to complete a step |
| **Interface tour without numbered callouts** | An approved departure, argued in `outline.md` §4 chapter 6. Every region names itself, so the accessibility rule is better served. Not a finding |

---

## The lint disposition

**All four of the caller's dispositions are confirmed.** Lines re-read at source.

| Lint finding | Caller's disposition | Verdict |
| --- | --- | --- |
| Line 90 WARN "Click" | Verbatim quoted label. Sanctioned | **Confirmed.** Line 90 carries the quoted empty-Gallery message, which `02-labels.md` and `gallery.html:24` both spell with `Click` |
| Line 92 WARN "click" | The conventions sentence explaining the quoting rule. Sanctioned | **Confirmed.** Line 92 is "This manual's own instructions say select rather than click", which is the rule being stated |
| Line 241 WARN "Click" | Verbatim quoted label. Sanctioned | **Confirmed.** Step 2 of topic 5.1 quotes the same message |
| Line 38 WARN "step starts with when" | False positive | **Confirmed.** Line 38 is the contents-list entry "13. [When something does not work]". The linter reads the contents list as a procedure |
| Lines 327, 333, 467 INFO "Optional:" | The linter is catching the parenthesis in **Description (optional)**, not unmarked steps | **Confirmed.** Line 333 already carries an `Optional:` prefix **and** the label, which is proof of the match. Lines 327 and 467 both contain `Description (optional)` |

**Three further findings the caller did not disposition are the same contents-list
false positive:** line 29 INFO voice (28 words), line 38 INFO voice (96 words) and
line 38 INFO procedures (96 words). The linter counts the contents list as prose
and its link URLs as words. No action.

**Three are genuine and are reported above as T10:** lines 615, 697 and 702, at
26, 29 and 30 words.

So the draft's real mechanical debt is three long sentences, against a report of
4 warnings and 9 info findings. The linter's own summary is a fair reading once
the false positives are removed: **0 errors stands**.

---

## Standards mapping

Per §11 of the checklist. The normative text of both standards is paywalled, so
this mapping is built from published clause listings. The deliverable is
**aligned with the structure and quality attributes** of these standards, and is
not certified conformant.

### ISO/IEC/IEEE 26514, design and development of information for users

| What it expects | Where this deliverable meets it | Gap |
| --- | --- | --- |
| Documented audience and task analysis | `Planning/documentation-plan.md` §2 and §3: one reader group, evidenced from `.brain/glossary.md` and the client's own words, and a 33-task inventory with a requirement and a test behind each | None |
| Stated usability objectives | The plan states frequency and pressure per task, and names first-use blockers | Partial. No measurable objective, such as time to first Photo, is set |
| Modular topic-based authoring | The topic anatomy in `references/structure.md` is held: **Before you begin**, numbered steps, **Result**, **See also**. 30 numbered topics, each completable from search | S1: one topic is outside the numbering and the contents list |
| Conceptual, instructional and reference information | Concept 9.1, 10.1, 13.1. Instruction across chapters 3 to 11 and 13. Reference chapters 12 and 14 | S7, S8: two instances of one kind leaking into another |
| Commands | Not applicable. No command-line surface is in scope, per assumption A2 | None |
| Troubleshooting and error messages | Chapter 13, organised by symptom, opening with a symptom index carrying the literal message where one exists | None |
| Glossary | Chapter 14, nine entries, each leading with the definition and never restating the term | None |
| FAQ | Deliberately dropped. `references/structure.md` forbids inventing FAQ entries, and no support ticket record exists | Recorded, argued in `outline.md` §2 |
| Correctness | C1 to C9 are the exceptions | 9 findings |
| Consistency | One term per thing holds across both documents, with T7 and T8 as the exceptions | 2 findings |
| Comprehensibility | Sentences under 25 words, with three exceptions at T10 | 3 findings |
| Conciseness and minimalism | S4, S5, S10, S11 are the four places a point is made twice | 4 findings |
| Accessibility | Held throughout. No directional language, no element named by appearance, alt text on all eight figures, real tables and lists, sequential heading levels | None |

### IEC/IEEE 82079-1, preparation of information for use

| What it expects | Where this deliverable meets it | Gap |
| --- | --- | --- |
| The three information types distinguished | The Diátaxis typing is recorded per task in `outline.md` §2 and holds in the draft | S7, S8 |
| Product identification | Chapter 1's table: product and version, document version, date, audience | None |
| Intended use | Chapter 2 states what MyGallery is for and who reaches it | None |
| Reasonably foreseeable misuse | Not stated. The nearest is 10.1's statement that no other device can reach the application | Not a regulated product. Recorded as a deliberate omission |
| Safety information | Not applicable. No physical hazard. The one data-loss hazard, permanent deletion, carries a **Warning** stating the hazard, the consequence and the avoidance action, inside the step it governs | None |
| Install | Chapter 3. Python is the single prerequisite | **C5.** Getting a copy of the application onto the PC is undocumented, and Q11 owns it |
| Commission | Chapter 4.1, and the tutorial at 5.1 | None |
| Operate | Chapters 5 to 11 | None |
| Maintain | 10.3, backing up the Gallery | C7 |
| Troubleshoot | Chapter 13, nine entries in three families | Q3 leaves 13.9's general case open |
| Decommission and data deletion | 11.1 deletes one Photo. Nothing covers removing MyGallery from the PC or deleting the whole Gallery | Recorded. Not in the task inventory, and not asked for |

**For a regulated or safety-relevant product**, the three elements that would
need adding are an intended-use and limitations statement, a
reasonably-foreseeable-misuse note, and a decommissioning and data-deletion
section. None is required here: no standard, tender requirement or accessibility
level is named anywhere in `.brain/`, which `documentation-plan.md` §5 records.

---

## Prioritised fix list

Ranked by what a reader loses. The caller decides how far down to act.

1. **C2** Manual 13.6: the Gallery is not shown in the black window. One sentence, and it is the only outright error in the draft.
2. **S1** Manual line 343: renumber the drop procedure, add it to the contents list, and move topic 7.1's **See also** block back above it. One task is currently unfindable.
3. **C1** Manual 10.2 and 10.1: qualify the downloaded filename, in one place.
4. **C3** Manual 10.1: cut the Thumbnails folder and the index, or harvest them into the source pack and lift the out-of-scope row.
5. **C5** Escalate Q11. The first-use path is blocked, and no fix belongs in the draft until it answers.
6. **C6** Manual 9.2: one sentence on what happens past 250 characters.
7. **C4** Manual 7.1 step 2: drop the preview width clause.
8. **C8** Manual 13.8: write the cause as a condition to check rather than as the reader's machine state.
9. **P1, P2** Manual 9.3 and 9.2: make both results observable through the Larger view.
10. **C7** Manual 10.3: copy the folder, not the files in it.
11. **S2** One chapter opener per chapter, written about the subject.
12. **S4, S6** Fold 13.2 into 13.1, and hold 13.9 to a symptom-index row until Q3 answers.
13. **S3** Retitle chapter 6 or topic 6.1.
14. **T7** Quick start line 38: "Photo", and "most recently uploaded first".
15. **T10** Split the three long sentences at lines 615, 697 and 702.
16. **C9, S5, S7, S8, S9, S10, S11, S13** The remaining duplication and typing cleanups.
17. **T1 to T6, T8, T9, T11, T12, T13** The section 1a and consistency cleanups.
18. **S12** Q13, raised in `open-questions.md`. Needs a channel from the client.

## Delivery package

Against §12 of the checklist, for the caller rather than as a finding on the
draft.

| Item | Present |
| --- | --- |
| The manual, in Markdown | Yes |
| The quick start, in Markdown | Yes |
| The change log, one row per change this round | Not checked. `outline.md` §6 places it beside each document |
| `open-questions.md` | Yes. Q13 appended by this pass |
| The screenshot capture list | `Source pack/10-capture-list.json`, whose `captures` array is empty and whose defaults do not match the eight captures taken. P4 is open |
| The terminology list | Yes |
| The source pack | Yes, with the two gaps at C3 |
| The Phase 1 documentation plan | Yes |
| A maintainer's note for the next release | Not produced. `outline.md` §5 specifies its content: re-read `README.md` under "Before you start", "Run MyGallery" and "If something goes wrong", and confirm topics 3.1, 3.2, 4.1, 4.2, 4.3 and 13.5 to 13.7 still match |
| The formatted document | Not applicable. Phase 6 does not run for v1.0, closed as P3 |

One arithmetic note for the caller, on the plan rather than the draft:
`outline.md` §1 records "Twenty-nine topics carry the 33 tasks", and §4 lists
thirty numbered topics plus the drop procedure. The draft follows §4.
