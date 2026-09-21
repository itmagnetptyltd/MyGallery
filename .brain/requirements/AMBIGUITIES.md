# Open questions for the client

**Four. Raised 2026-09-21 by FB-0004, absorbed as CHG-0005–CHG-0009.**

The seventeen questions raised at decomposition were all answered by the client
on 2026-09-18. Those answers, in the client's own words, are in
[`ANSWERS.md`](ANSWERS.md) — that file is kept, not cleared, because it is the
record of what was said and when. Every one was written into the acceptance
criteria of the requirements it affected, and each affected requirement's
`source` carries `clarified by client answers 2026-09-18 (ANSWERS.md)`.

FB-0004 then put four new questions back. Until the client answers them, the
requirements they block are at `draft`: REQ-GAL-001, 002, 003, 008, 012, 013,
015, 017 and 018. REQ-GAL-016 and REQ-GAL-019 carry no open question and are at
`agreed` — they are the two that can be built now.

Paste the client's reply into [`ANSWERS.md`](ANSWERS.md) and run
`/resolve-ambiguities`.

---

## What is shown of the chosen files before the Upload is made?

_Blocks: REQ-GAL-001, REQ-GAL-013, REQ-GAL-015_

_In plain words: After you pick photos — or drop them in — but before they are
added, what would you expect to see of them? Just the file names, one picture,
or all of them? And what should that look like when you have picked thirty at
once?_

The ask says "a view" and names no observable. A list of filenames, a single
preview and a grid of thirty thumbnails are three different pieces of work, and
nothing in the ask chooses between them. REQ-GAL-001@v3 requires an Upload of
thirty files to work, so whatever is shown has to hold thirty.

## Is the 250-character description limit a refusal, or a typing limit?

_Blocks: REQ-GAL-001, REQ-GAL-017_

_In plain words: If you paste a description longer than 250 characters, should
MyGallery refuse the upload and tell you why — or simply stop you typing past
250?_

Both honour "max 250 char" and they behave differently. If it is a refusal,
REQ-GAL-009@v1 applies: the file is named and a reason is shown. If it is a
typing limit, there is no failure to report and no reason to show.

## Can a description be changed after Upload, and what do existing Photos carry?

_Blocks: REQ-GAL-002, REQ-GAL-008, REQ-GAL-017_

_In plain words: Once a photo is in the Gallery, do you expect to be able to add
or change its description later? And the photos already in your Gallery —
should they stay without one?_

The ask places the description at Upload only. Editing later is a separate
capability and is not implied by it. There are Photos in the client's Gallery
today that were uploaded before this change existed.

## Tooltip or alt text?

_Blocks: REQ-GAL-003, REQ-GAL-012, REQ-GAL-018_

_In plain words: When you rest the mouse on a photo, should the description
appear in the little box that pops up next to the pointer? Or should it be the
photo's alt text — the words a screen reader reads out in place of the image?_

The ask says "tooltip/alt" and does not choose. They are not the same thing: a
tooltip is not announced by a screen reader, and alt text replaces the image
rather than accompanying it. Today alt carries the Photo's filename, so
answering "alt" also decides what happens to that.

---

## What this file is for

Every point where a source document does not actually say what it appears to
say, phrased as a question for the client. A question listed here is **open**,
and an open question blocks the requirement it affects from moving `draft` →
`agreed`.

Questions are closed by the client answering them. Never by an agent, a
developer, or anyone else choosing the reading that is easier to build. A
resolved question is deleted from this file — it is not marked answered — and
the resolution survives as the acceptance criterion it produced.

This file and the `ambiguities:` lists in `gal.yaml` are two views of one list.
They must not diverge.

## When questions come back

New scope, a changed brief, or a discovered gap puts questions back here:

- `/decompose` on a new or amended brief writes new requirements and new
  questions.
- `/find-variation` decides whether a new ask is inside agreed scope.
- `/change-record` captures an agreed change to something already `agreed` —
  which supersedes a requirement version rather than editing it.

Then paste the client's reply into `ANSWERS.md` and run
`/resolve-ambiguities` again.

---

## Settled here, but not by this file

Three things the answers raised are **not** ambiguities and are not tracked
here. They are recorded so they are not mistaken for open questions:

- **Which runtime — Node.js or Python.** The client said "like Python or
  Node.js", which answers the question that was asked (*at most one
  prerequisite, installed once*) without choosing a stack. That choice is a
  real decision between alternatives and belongs in `.brain/decisions/` as an
  ADR — `/adr-write`. REQ-GAL-011 constrains it to one prerequisite and a
  single-command start; it does not name the runtime.

- **What "fast" means.** The client asked twice for the Gallery to stay fast
  and gave no number. REQ-GAL-003 captures the observable consequences —
  Thumbnails are smaller than their Photos, and the Gallery loads in parts
  rather than all at once. A numeric budget, if one is wanted, is a
  `.brain/constraints/` entry, not a requirement.

- **Where Photos are stored on disk.** The client asked for "a normal folder on
  my disk that I can find and back up myself". REQ-GAL-008 requires that the
  Photos be present there as ordinary copyable files; the actual path is a
  design decision, and belongs in an ADR if it is not obvious.
