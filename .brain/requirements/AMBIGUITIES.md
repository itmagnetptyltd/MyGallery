# Open questions for the client

**Two. Both are what is left of the four raised on 2026-09-21 by FB-0004,
after the client answered on 2026-09-21.**

The seventeen questions raised at decomposition were all answered on
2026-09-18. Those answers, in the client's own words, are in
[`ANSWERS.md`](ANSWERS.md) — that file is kept, not cleared, because it is the
record of what was said and when.

FB-0004 raised four more. The client answered all four on 2026-09-21. Two
closed outright — the 250-character limit is a typing limit, and the
description is the image's alt text — and their answers are now acceptance
criteria. The other two answered part of what was asked and left the rest open;
those remainders are below, narrowed to exactly what is still missing.

`agreed` and buildable: REQ-GAL-003, REQ-GAL-012, REQ-GAL-016, REQ-GAL-018,
REQ-GAL-019. Still `draft`: REQ-GAL-001, 002, 008, 013, 015, 017.

Paste the client's reply into [`ANSWERS.md`](ANSWERS.md) and run
`/resolve-ambiguities`.

---

## When several files are chosen at once, is every one previewed?

_Blocks: REQ-GAL-001, REQ-GAL-013, REQ-GAL-015_

_In plain words: You said you want a preview of the image before it is added.
When you pick thirty photos at once, would you expect to see a small preview of
all thirty, or just one?_

The client answered "preview of that uploadede image" on 2026-09-21, which
settles that a picture is shown rather than a filename — that is now a
criterion. It does not settle the batch. REQ-GAL-001@v3 requires an Upload of
thirty files to work, and thirty previews, one preview, or a scrolling strip
are three different pieces of work.

## Where is a description changed after Upload?

_Blocks: REQ-GAL-002, REQ-GAL-008, REQ-GAL-017_

_In plain words: You said you want to be able to change a photo's description
later. Where would you go to do that — open the photo large and edit it there,
or somewhere on the Gallery page itself?_

The client answered "Yes" on 2026-09-21, which settles that a description can
be added or changed after Upload, and that Photos already in the Gallery carry
none until one is given — both are now criteria. It does not say where the
editing happens, and every surface in this application is named by a
requirement rather than left to chance.

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
