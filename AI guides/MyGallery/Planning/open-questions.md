# Open questions

Every missing fact, assumption and production step for the MyGallery
documentation. Nothing here appears in a draft: a question is answered before
the sentence that needs it is written.

Raised at Phase 0, 2026-09-23, against commit `a00d0a4`.

## Blocking a sentence in the draft

| # | Question | Where it affects the draft | Owner | Answer |
| --- | --- | --- | --- | --- |
| Q1 | Does the manual document the Controlled Folder Access problem, or is the application changed so it does not arise? | Getting started, and troubleshooting. See the note below | Client, with the development team | **Answered 2026-09-23.** Document it as a troubleshooting entry against the current behaviour. The application is not changed for v1.0 |
| Q2 | Which Windows 11 builds are supported, and is any other operating system in scope? | System requirements | Client | |
| Q3 | What is the reader told to do when the Gallery cannot be read? The message names no action | Troubleshooting | Development team | Partly settled by Q1: Controlled Folder Access is one cause and has its own entry. The general case stands open |
| Q4 | Is the Gallery folder's location, `Pictures\MyGallery`, told to the reader? `REQ-GAL-008` makes the Photos ordinary copyable files, which is only useful if the reader knows where they are | Backing up, and the concept topic on where Photos live | Client | **Answered 2026-09-23.** Yes. The manual names `Pictures\MyGallery` and says the Photos there can be copied |
| Q5 | Is there a supported way to move the Gallery folder, or to point the application at another one? `MYGALLERY_DIR` exists in `config.py` but is not a documented feature | Backing up, or omitted entirely | Development team | **Answered 2026-09-23.** No. `MYGALLERY_DIR` stays undocumented and unsupported, and the manual does not mention it |
| Q6 | The empty-Gallery message reads `No photos yet. Click Upload to add your first photos.`, but the button it names is labelled `Upload photos`. Does the manual quote both and name the button, or is one of them changed? | The empty-Gallery topic, Getting started, and the conventions section | Development team, with the client | **Answered 2026-09-23, and applied.** The message was corrected to name the real button. See the note below |
| Q7 | Which theme and which viewport do the manual's figures use? The eight Phase 0 captures are light at 1280 by 860, `10-capture-list.json` defaults to 1440 by 900, and the client's own screenshots in `FB-0005` and `FB-0006` are dark. Does the application follow the reader's system setting? | Every figure, and the conventions section | Writer, with the development team | **Assumed 2026-09-23**, not asked: light at 1280 by 860, matching the eight captures already taken. Correct this if the client wants dark |
| Q8 | Which web browsers are supported? The client named Chrome and Edge, the walkthrough used Chromium, and nothing records Firefox. `06-config-limits.md` found no browserslist | System requirements | Development team | **Answered 2026-09-23.** Chrome and Edge, as the client's own answer names. The manual is silent on others rather than claiming them |
| Q9 | Is closing the console window, or `Ctrl+C` in it, the supported way to stop MyGallery? `README.md` says both, and no acceptance criterion covers stopping | The Stop MyGallery topic | Development team | **Assumed 2026-09-23**, not asked: both, as `README.md` states. A6 carries the assumption |

| Q10 | What is the reader told to do about the Controlled Folder Access refusal? Q1 settled that the manual documents it, and the record holds the symptom, the cause and its evidence, but not the remedy. The remedy is a path through Windows Security, which is in no repository and in no part of the source pack | Troubleshooting topic 13.8 in `outline.md`, which is otherwise complete | Client, with the development team | **Answered 2026-09-23.** The path was read off a real machine. See the note below |

| Q11 | How does the reader get a copy of MyGallery onto their PC, and where do they put it? `REQ-GAL-011` c1 assumes "a copy of the application" is already present, and no `README.md` section, requirement or test says how it arrives | Topic 3.1, and step 1 of topic 4.1, which opens `scripts/start.cmd` without naming the folder it sits in | Client, with the development team | |
| Q12 | Is resting the pointer on a Thumbnail a documented way to read its description? `src/mygallery/static/app.js:81-83` sets the image's `title` to the same text as its alt text, and the comment there records it as answering FB-0004's "on mousemove" ask. No acceptance criterion covers it, no test asserts it, and the source pack does not record it | Topics 9.1 and 6.2, which state the alt text alone | Development team, with the client | |

| Q13 | Where does a reader report an error in the manual? Chapter 12 of the `references/structure.md` skeleton, Support and feedback, was dropped because no support channel, hours or defect channel is recorded anywhere in `.brain/`, which `outline.md` section 2 argues. The consequence is that a reader who finds a wrong instruction has nowhere to send it, and `references/qa-checklist.md` section 9 asks for one. Naming a channel would be invention | The manual as a whole. A one-line answer restores the dropped chapter as a short closing section | Client | |

Raised at Phase 1, 2026-09-23: Q6 to Q9. Answered at the Phase 1 gate,
2026-09-23: Q1, Q4, Q5, Q6 and Q8 by the client. Q7 and Q9 were not put to
them, and carry the writer's assumption until they are. Raised at Phase 2,
2026-09-23: Q10. Raised at Phase 3, 2026-09-23: Q11 and Q12. Raised at Phase 5,
2026-09-23: Q13.

Q10 is the sentence Q1's answer does not supply. Naming a menu path in Windows
Security from memory is the invention the no-invention rule exists to stop, so
the answer comes from a path read off a real machine, or the entry states the
cause and stops there.

## Q10, and the path that was verified

The client chose to have the path verified rather than recalled. Windows
Security was opened on the build machine on 2026-09-23 and photographed twice,
and the two captures agree. They are `Source pack/cfa-01.png` and
`Source pack/cfa-03.png`.

Verified, and safe to write:

| Step | Read from the screen |
| --- | --- |
| 1 | Open **Windows Security** |
| 2 | **Virus & threat protection**, in the list on the left |
| 3 | The page is titled **Ransomware protection** |
| 4 | The section is **Controlled folder access**, above a switch reading **On** |
| 5 | The link is **Allow an app through Controlled folder access** |

Two neighbouring links are on the same page and are **not** the remedy:
**Block history** and **Protected folders**. Naming them is how a reader ends up
on the wrong screen, so the topic names only the third.

**Not verified: what is on the page behind that link.** Three attempts to open
it closed the Windows Security window instead, so the final control was never
read. The topic therefore ends at step 5 and tells the reader to allow MyGallery
on the page that opens, without naming a button that was not seen. That is the
boundary of the evidence, and the sentence stops at it.

These labels are Microsoft's, not this product's, and they are quoted with the
US spelling and the ampersand exactly as the screen shows them. The house rule
on Australian English does not reach another vendor's interface. A later Windows
version may rename them, which is recorded in the maintainer's note.

## Q6, and what was changed in the application

The client chose to correct the message rather than document the mismatch. The
wording was never a criterion: `REQ-GAL-007@v2` requires only that "a message
stating that there are no Photos yet is shown", unlike `REQ-GAL-005`, whose
confirmation wording the client gave verbatim.

`src/mygallery/templates/gallery.html:24` now reads:

> `No photos yet. Click Upload photos to add your first photos.`

No test asserted the old string, so none needed changing: the three tests that
touch the message assert its visibility by test id. Belt A passed at 166 tests,
and the 20 belt B tests covering the Gallery and the visual check passed.

Two things follow from this, and neither is the documentation's to decide:

- **Nothing asserts the message names a real control**, which is why the
  mismatch survived to a documentation pass. A test pinning the message to the
  button's label would stop it recurring.
- **The verb is still `Click`**, which is a device verb the manual's own house
  style forbids in its prose. The manual quotes the label verbatim regardless.
  Making the application's voice device-neutral was not asked for and was not
  done.

`.brain/` records nothing about this change. Writing to `.brain/` outside a
reviewed pull request is forbidden by `CLAUDE.md`, so the change belongs in the
pull request that carries it.

## Q1, in full

Windows Defender Controlled Folder Access is enabled on the machine this was
built on, and it blocks the application from creating `Pictures\MyGallery`.
The Gallery page loads, and every request for a Photo then fails. Windows
reports the refusal as `WinError 2`, "the system cannot find the file
specified", rather than as a refusal, so the failure does not name its cause.

This is not reproducible from the repository, and it is not a defect in the
application's code. It is an interaction between the default Gallery location
and a Windows security feature that is on by default in some configurations.

It matters to the manual because it strikes on first run, before the reader has
done anything, and the application gives them nothing to act on. Documenting it
is possible. Changing the application so a blocked folder is reported in words
is better, and is a development decision rather than a documentation one.

Evidence: event 1123 in `Microsoft-Windows-Windows Defender/Operational`, and
`(Get-MpPreference).EnableControlledFolderAccess` returning `1`.

## Assumptions carried into Phase 1

Each is the documentation's reading, not the client's word. Confirm or correct.

| # | Assumption | Rests on |
| --- | --- | --- |
| A1 | There is one reader group: the one person who uses MyGallery on their own PC. No administrator, no installer, no second user | `.brain/glossary.md`, "The user" |
| A2 | That reader is not technical, and the manual assumes no command line | The brief's start steps are a double-click, `REQ-GAL-011` |
| A3 | The manual is read on screen beside the application, not printed | No print requirement in `.brain/requirements/gal.yaml` |
| A4 | The application programming interface is out of scope, since no reader calls it | `01-routes.md`, "Not documented, with the reason" |
| A5 | The developer material in `README.md` under "Working on MyGallery", and everything in `.brain/`, is out of scope for this documentation set | `.brain/glossary.md`, "The user"; A1 |
| A6 | `Ctrl+C` in the console window, and closing that window, are the supported ways to stop MyGallery | `README.md`, "Run MyGallery". No requirement covers stopping. See Q9 |

## Production steps still to do

| # | Step | Blocked by |
| --- | --- | --- |
| P1 | Capture `The Gallery could not be read.` against a real unreadable Gallery | A safe way to produce one. **Blocks no topic**: the Phase 2 outline plans no figure for topic 13.9, which quotes the message instead |
| P2 | Capture the too-large refusal, `file is too large (max 25 MB)` | A photo over 25 MB. **Blocks no topic**: the Phase 2 outline plans no figure for topic 13.4, which quotes the message instead |
| P3 | Decide whether the manual is delivered as Markdown alone, or built to a formatted document at Phase 6 | **Closed at the Phase 1 gate, 2026-09-23.** Markdown alone, and Phase 6 does not run for v1.0 |
| P4 | Correct `Source pack/10-capture-list.json`: its defaults read 1440 by 900, and the eight captures taken are 1280 by 860. Add an entry for each of the eight | Nothing. A Phase 3 step for `manual-mechanic` |
| P5 | The quick start's `Next steps` table links the manual by relative path and in-file anchor, into a filename that carries this draft's version and draft number (`MyGallery User Manual v1.0 draft 01.md`). Decide whether a release renames both documents together, or the quick start's links are corrected at each release, so the two do not drift apart the way `README.md` and the quick start are kept from drifting in section 5 of `outline.md` | Nothing blocks Phase 3. A production step for the release process, raised at Phase 3, 2026-09-23 |
