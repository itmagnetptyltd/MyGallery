# 2026-09-18 — Decompose the brief, agree the record, choose the runtime

## Worked on

The whole of module GAL, from a three-sentence client brief to an agreed
requirement record and a build order.

- `/decompose` — brief captured verbatim, REQ-GAL-001 … REQ-GAL-011 allocated at
  `draft`, seventeen open questions raised.
- `/resolve-ambiguities` — the client answered all seventeen. Acceptance criteria
  written from their words, register cleared, all eleven moved to `agreed`, and
  the first task sequence written into `slices.yaml` as six slices.
- `/feature-plan REQ-GAL-011` — slice 1 planned. **Written against Node.js, and
  now stale** — see Left unfinished.
- `/adr-write` — ADR-0001, the runtime.
- `/verifyReq` — record verified; two traps found and promoted to `constraints/`.

No code was written. `src/` still holds only `.gitkeep`.

## Learned

Everything durable was promoted. Pointers only:

- The runtime choice and its consequences → **ADR-0001**.
- Two CI traps, both measured rather than assumed → **constraints/** (see
  Promoted to the record).

One thing that is not durable enough for its own record but is worth a line:
**six of the seventeen questions were answered with more than was asked.** The
sign-in question came back with "not from other devices or over the internet",
which is a network exposure constraint nobody had asked about; it became an
acceptance criterion on REQ-GAL-011 (the server refuses connections from other
devices). Worth expecting on this client: their answers carry extra requirements
in the margins, and reading only the sentence that answers the question would
have lost it.

## Left unfinished

- **The slice 1 plan is stale.** `.brain/sessions/2026-09-18-plan-REQ-GAL-011.md`
  is written against Node.js — `package.json`, `node:http`, `node:test` — and
  ADR-0001 chose Python. Its approach, file list and entire test skeleton need
  reissuing with `/feature-plan REQ-GAL-011` before `/tdd`. Its non-runtime
  findings still hold and are worth carrying over: criterion 2 of REQ-GAL-011
  ("followed by someone who has not worked on the project") is not mechanically
  testable and only has a proxy; criterion 5's cross-device test skips on a
  machine with no non-loopback interface.
- **Slice 1 is Not started (0/1).** Nothing is `in_progress`, nothing is
  `verified`.
- **Two decisions deliberately deferred**, both noted at the foot of ADR-0001:
  the HTTP layer (stdlib `http.server` versus a small framework), and where
  Photos are stored on disk — the latter belongs in its own ADR when slice 2 is
  planned, since REQ-GAL-008 requires the client be able to find and back the
  folder up themselves.
- **Three branches sit on the same commit** — `main`, `feat/decompose-gallery`
  and `feat/gal-boot` all point at `671d1a3`. Both feature branches are empty;
  all of this session's work was uncommitted until this checkpoint. They can be
  deleted once this pull request lands.

## Promoted to the record

- `decisions/ADR-0001-python-runtime.md` — Python 3.12+, one prerequisite, no
  build step. Node.js considered and rejected on the developer's call.
- `constraints/g7-blocks-once-a-belt-c-requirement-is-agreed.md` — G7 became
  fail-closed when the requirements reached `agreed`, so the first pull request
  will fail it regardless of contents. No fix applied yet.
- `constraints/g3-passes-vacuously-with-no-adapter-manifest.md` — G3 exits 0
  under `--strict` having scanned zero files, because no `pyproject.toml` exists
  to select an adapter. Delete once slice 1 lands one.
- `glossary.md` — the seven terms the brief left undefined are now defined, plus
  new entries for *Accepted image format*, *Delete* and *The user*. The shipped
  `Engagement` template example was removed; it was sitting under **Agreed
  terms** next to the real entries.

Nothing was added to `rejected/`. Node.js lost an argument but was never tried —
no code was written against it, so there is no evidence to record. It is in
ADR-0001's *Alternatives considered*, which is where a rejected-without-trying
option belongs.
