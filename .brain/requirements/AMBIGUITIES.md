# Open questions for the client

**None. Everything raised on this project has been answered.**

The seventeen questions raised at decomposition were answered by the client on
2026-09-18. FB-0004 raised four more on 2026-09-21; the client answered all
four the same day, two of them in full and two in part, and the two remainders
were narrowed and answered in a second round on 2026-09-21.
FB-0005 raised three more on 2026-09-21; the client answered two in a third
round and the last, narrowed, in a fourth round the same day.

The answers, in the client's own words, are in [`ANSWERS.md`](ANSWERS.md) -
that file is kept, not cleared, because it is the record of what was said and
when. Every answer was written into the acceptance criteria of the requirements
it affected.

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
