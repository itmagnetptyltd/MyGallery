# 2026-09-18 — Build slice 1, Boot

Second session of the day. The first decomposed the brief and agreed the record
(`2026-09-18-decompose-and-agree.md`); this one built the first slice.

## Worked on

`REQ-GAL-011` — the application starts on the client's PC.

- `/feature-plan REQ-GAL-011` reissued against Python after ADR-0001; the
  earlier Node plan is marked superseded rather than deleted.
- `/tdd REQ-GAL-011` — 19 tests, belts A and B, tests first.
- `/close-slice` — `in_progress -> verified`, slice 1 **Done (1/1)**.
- `/verifyReq` and `/pr-prepare` — record clean; commit `b3395de` pushed.

Slice 1 is the first and only slice at `verified`. Ten requirements remain
`agreed` across slices 2–6.

## Learned

Durable items were promoted — see below. Two things that are not worth a record
of their own:

**A fixture named `base_url` collides with `pytest-base-url`**, which
pytest-playwright pulls in and which defines its own session-scoped `base_url`.
The symptom is `ScopeMismatch` at setup, pointing into
`pytest_base_url/plugin.py`, not at your own code — which reads like a broken
install rather than a name clash. Renaming the fixture to `gallery_url` fixed
it. `tests/e2e/test_boot.py` carries no comment saying so, and probably should,
or someone will rename it back.

**Coverage came in at 66% before the entry point was split.** `__main__.py` was
10 of 29 statements and untestable by construction. Moving the work into
`launcher.py` behind injectable seams took it to 97%. The plan predicted this
and said to move the logic rather than lower the threshold, which turned out to
be the right call and took about five minutes.

## Left unfinished

- **Both pull requests merged while this checkpoint was being written** — #1
  (`brain/checkpoint-2026-09-18`) then #2 (`feat/gal-boot`), in that order and
  with merge commits rather than squashes, so the duplicate-brain-diff risk did
  not materialise. `main` is now `6477faf` and holds the record and slice 1.
  This checkpoint was branched before that and has had `main` merged into it.
- **`58fe9fc` was committed outside this session** and pushed to
  `feat/gal-boot`. It adds the two session plan files that `/pr-prepare` had
  deliberately kept out of the code pull request, so that pull request now
  carries brain knowledge beyond the parent-commit problem above. Its message,
  `Covers: REQ-GAL-011@v1`, is a trailer with no conventional-commit type. Not
  reverted — the developer's commit, the developer's call.
- **ADR-0003 has not been put to the client.** It reads their "install one
  thing" as *Python is the prerequisite, the app's dependencies are part of the
  app*. That reading should be confirmed in one sentence before slice 2 adds
  Pillow.
- **`.gitignore` has no `.coverage` entry.** One line; the artefact was removed
  by hand this session.
- **Slice 2 is not ready to plan.** It needs the storage-path ADR
  (`REQ-GAL-008` requires a folder the client can find and back up), and it is
  where the belt-C exit-5 problem lands.

## Promoted to the record

- `decisions/ADR-0002-flask-http-layer.md` — Flask, chosen at slice 1 for slice
  2's sake; `cgi` removed in 3.13 is the deciding fact. Records that Flask's
  built-in server is the production server here, deliberately.
- `decisions/ADR-0003-python-is-the-one-prerequisite.md` — what
  `REQ-GAL-011`'s "at most one prerequisite" counts, and why `README.md` is now
  load-bearing for a test.
- `constraints/check-secrets-scans-the-virtualenv.md` — the local secret scan
  went from 101 files and 0 findings to 3003 files and 76 findings, all of them
  inside `.venv/`. Local only; CI is unaffected.
- `constraints/g7-blocks-once-a-belt-c-requirement-is-agreed.md` — **updated.**
  `pytest -q -m integration` exits 5 on an empty belt-C set. Recorded last
  session as an unverified expectation; now measured.
- `constraints/g3-passes-vacuously-with-no-adapter-manifest.md` — **deleted.**
  It was first marked "cleared, pending merge"; slice 1 then merged to `main`
  mid-checkpoint, so its own deletion condition was met and it went. Re-measured
  on this branch with `main` merged in: `adapters python, scanned 7 test
  file(s)`. Leaving it would have cast doubt on a gate that had started working.
  It survives in history on `1155c3f` if the reasoning is ever needed.

Nothing was added to `rejected/`. The standard-library HTTP layer was argued
against and never written, so there is no evidence to record; it is in ADR-0002's
*Alternatives considered*, which is where an option rejected without being tried
belongs.
