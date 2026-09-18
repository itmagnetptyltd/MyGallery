# G3 traceability reports PASS having scanned nothing, when no adapter manifest exists

- **Discovered:** 2026-09-18
- **Review by:** 2026-12-18
- **Source:** measured on this repository, 2026-09-18 —
  `node .claude/itm-sdlc/scripts/check-traceability.js --project . --strict`;
  adapter detection rules in `.claude/itm-sdlc/adapters/python.json`
- **Affects:** `.github/workflows/gates.yml` (G3), `/verifyReq`, `pyproject.toml`
- **Status:** **cleared by slice 1, pending merge.** Delete this file at the
  first checkpoint after `feat/gal-boot` reaches `main`. Still true of `main`
  itself, which has no `pyproject.toml` until that merge lands.

## The constraint

An adapter is selected by detecting a manifest file, not by the presence of
source code. The python adapter's `detect` list is
`["**/pyproject.toml", "**/setup.py", "**/setup.cfg"]`. None of those exists on
this project yet.

With no adapter matched, `check-traceability.js` scans **zero** test files, finds
**zero** annotations, finds zero orphans as a result — and **exits 0, reporting
`PASS`, even under `--strict`**, which is the mode G3 runs on a pull request.

The script is honest about it: it emits `WARNING [no-adapters]` whose text ends
"No test file was scanned, so this result proves nothing." But the verdict line
directly beneath still reads `PASS`, and the exit code is 0. Anything reading the
exit code — CI, a script, a person skimming — sees a pass.

**A green G3 on this project currently means "not measured", not "traceable".**

## How we know

```
$ node .claude/itm-sdlc/scripts/check-traceability.js --project . --strict

  itm-sdlc | traceability (gate G3)
  adapters   (none detected)
  scanned    0 test file(s), 0 annotation(s)
  coverage   0/0 requirement(s) at 'in_progress' or beyond are annotated

  WARNING  [no-adapters]  no language adapter matched D:\practice\MyGallery.
           No test file was scanned, so this result proves nothing.

  0 orphan(s), 1 warning(s)  |  mode: strict
  PASS
$ echo $?
0
```

Re-measure with the same command. The condition is visible in one line of the
output: `adapters (none detected)`.

## What we do about it

Until a `pyproject.toml` exists, **read `adapters` and `scanned` before trusting
the verdict.** A G3 pass whose `scanned` count is 0 carries no information, and
must not be cited as evidence that requirements are covered.

Slice 1 created `pyproject.toml`, and the re-measured output on
`feat/gal-boot` is no longer vacuous:

```
$ node .claude/itm-sdlc/scripts/check-traceability.js --project . --strict
  adapters   python
  scanned    7 test file(s), 16 annotation(s)
  coverage   1/1 requirement(s) at 'in_progress' or beyond are annotated
  0 orphan(s), 0 warning(s)  |  mode: strict
  PASS
```

**That is true of `feat/gal-boot`, not of `main`.** `main` is still at the
toolkit install commit and has no `pyproject.toml`, so a G3 run there would
still scan nothing and still report PASS. The file therefore stays until slice 1
merges — deleting it now would claim `main` was fixed by a branch nobody has
accepted yet. Delete it at the first checkpoint after that merge, and leave it
in place if slice 1 is rejected.

The same trap applies to any future language added to this project before its
manifest lands, which is why the review-by date is three months rather than the
usual six: it should be revisited at slice 1, not left to expire on its own.
