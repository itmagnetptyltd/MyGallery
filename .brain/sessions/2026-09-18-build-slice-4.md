# 2026-09-18 — Build slice 4, Delete and durability

Fifth session of the day. A thin checkpoint: the slice produced no new
decisions and no new constraints, and this note says why rather than
manufacturing either.

## Worked on

`REQ-GAL-005` (delete) and `REQ-GAL-008` (durability), both now `verified`.
Slice 4 is **Done (2/2)**.

- `/feature-plan` for both, then `/tdd`, tests first.
- 22 new tests. Whole suite **115 passed**, coverage **95%**, ruff clean.
- Commit `8a97014`, merged to `main` as pull request **#8**.

Nine of eleven requirements are `verified`. Two remain `agreed`:
`REQ-GAL-006` (Download, slice 5) and `REQ-GAL-009` (Upload failure reporting,
slice 6).

## Learned

**Branching from `main` produced the first genuinely clean pull request.**
Last session's lesson held: one commit in the range, and the only `.brain/`
file was `gal.yaml` carrying `status` and `verified_by`. No stacked parent, no
session notes riding along. Worth doing the same for slices 5 and 6 — the cost
of getting it wrong was five requirements reaching `main` unreviewed.

**Four durability tests passed the moment they were written**, because
[[ADR-0004]] had already put every fact on disk. A test that has never failed
has not been verified, so two of them were made to fail deliberately: adding
`self._index_path.unlink(missing_ok=True)` to `PhotoStore._prepare()` turned
both reopen tests red, and removing it turned them green. The other two — the
file exists, its bytes match — were not force-failed and rest on weaker
evidence. Worth remembering that a requirement satisfied by an earlier slice's
design still needs its tests proven, or the slice reports coverage it has not
earned.

**Deleting had to remove three things, and only the criterion made that
obvious.** Criterion 6 says "neither that Photo nor its Thumbnail is retained
anywhere", which is the only reason `test_delete.py` checks the Photo file and
the Thumbnail file rather than just the index row. An implementation that
removed the row and left both files on disk would have passed a laxer test and
failed the requirement.

## Left unfinished

- **The stale-row problem has now been deferred three times, and needs a
  decision rather than a fourth deferral.** A Photo the client deletes in
  Explorer leaves its index row: the Gallery lists it and its Thumbnail 404s,
  so they see a broken tile. [[ADR-0004]] says in as many words that it "should
  be dealt with when REQ-GAL-005 (delete) is built in slice 4". Slice 4 did not
  deal with it, and was right not to — **no acceptance criterion in
  `REQ-GAL-005` or `REQ-GAL-008` describes that case**, so building it would
  have been scope no requirement asked for.

  That leaves ADR-0004 carrying an expectation that was not met. It is not
  superseded and must not be edited, so this note is the record of the
  divergence. The way out is one of:
  - a new requirement, via `/decompose` on a short brief to the client; or
  - `/find-variation` if it is to be treated as chargeable scope; or
  - the client accepting the behaviour, recorded as such.

  It is a decision for the developer and the client, not something a build
  slice can resolve.

- **`.gitignore` still has no `.coverage` entry.** Flagged in four consecutive
  sessions; the artefact has been removed by hand each time. It never fits
  inside a slice's scope, so it wants a small `chore:` commit of its own rather
  than another mention here.

- **`tests/`, `tests/api/` and `tests/e2e/` still have no `__init__.py`.** The
  naming convention in
  `constraints/test-basenames-must-be-unique-across-belts.md` is holding, and
  the permanent fix is still two minutes' work.

- **Where the delete control lives was never put to the client.** It sits in
  the Larger view on my reading of the brief's ordering; "delete this one" from
  the grid is an equally fair reading and less tedious for tidying up. One
  sentence would settle it, and it is cheap to move.

## Promoted to the record

**Nothing.** No new decision was made that reversing would be expensive, and no
new limit was discovered.

The three real choices in this slice — the delete control in the Larger view,
a `<dialog>` rather than the browser's `confirm()`, and unlinking the files
before removing the index row — are each confined to one method or one
template, and each is cheap to reverse. The last has a comment at the code
saying why that order fails safer than the reverse. Writing ADRs for them would
put noise in the directory that has to stay trustworthy, and the next person
could not tell them apart from the four decisions that genuinely constrain
what can be built.

Nothing was added to `rejected/` either: nothing was tried and abandoned.
