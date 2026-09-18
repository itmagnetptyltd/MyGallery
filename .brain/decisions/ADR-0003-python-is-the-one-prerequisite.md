# ADR-0003 — Python is the one prerequisite; the application's own dependencies are part of the application

- **Status:** accepted
- **Date:** 2026-09-18
- **Governs:** README.md ("Before you start" and "Working on MyGallery"), scripts/start.cmd, tests/test_start_instructions.py

## Context

`REQ-GAL-011` carries the acceptance criterion:

> **given** The project's start instructions
> **when** The software they require to be installed is counted
> **then** At most one prerequisite must be installed before the application will start

That criterion came from the client's own words, which named a count without
naming what counts:

> "I'm happy to install one thing once if you give me simple steps, like Python
> or Node.js. After that I want to start MyGallery by double-clicking a file or
> running one command, with nothing else to set up."
> — `.brain/requirements/ANSWERS.md`, 2026-09-18

By slice 2 the application will never have zero pip dependencies: `REQ-GAL-003`
needs Pillow for Thumbnails, and [[ADR-0002]] adds Flask. So "one install" had
to mean something more precise than "one `pip` invocation", and the test for
that criterion had to count *something* specific.

## Decision

**Python 3.12+ is the one prerequisite.** Installing the application's own
dependencies is part of installing MyGallery, not a second prerequisite.

Concretely:

- `README.md` has a section **"Before you start"** listing exactly one item,
  Python. `tests/test_start_instructions.py` parses that section and asserts it
  holds one entry — so the criterion is measured against the client-facing list
  and nothing else.
- Everything a *developer* needs — pytest, ruff, Playwright, browser binaries —
  lives under **"Working on MyGallery"**, a separate heading the criterion-3
  test deliberately does not read.
- `scripts/start.cmd` does the dependency install itself, on first run, so the
  client still performs a single action: open one file.

The developer was shown this reading against the strict alternative and chose it.

## Alternatives considered

**"One install, full stop" — the strictest reading.** Takes the client at their
most literal: nothing may be installed after Python, `pip` included. It is a
legitimate reading of what they said. It was rejected because satisfying it
requires bundling the runtime into an executable (PyInstaller or similar), which
[[ADR-0001]] had already considered and rejected for putting a build step
between the source and the thing that runs. Choosing it would mean superseding
ADR-0001, not just this decision.

**Documenting two steps honestly** — "install Python, then run `pip install -r
requirements.txt`, then start". Rejected because it fails the criterion as
written (`then: Starting it takes a single command or a single file to open`)
and because it pushes a step onto a client who told us they wanted none.

## Consequences

**Makes easy.** The client's experience is one install and one double-click,
which is what they asked for. The criterion becomes mechanically testable
against a specific section of a specific file, rather than against a judgement.

**Makes hard.**

- **`README.md` is now load-bearing.** Moving Python out of "Before you start",
  renaming that heading, or adding a second bullet to it will fail
  `tests/test_start_instructions.py`. That is intentional — the test exists so
  the instructions and the criterion cannot drift apart — but it will surprise
  someone editing prose.
- The first run is slow, because `start.cmd` builds a virtual environment and
  installs dependencies before the Gallery appears. `README.md` says so.
- If `pip install` fails offline or behind a proxy, the client sees it at first
  run rather than at install time, and the error is pip's rather than ours.

**Not settled with the client.** This is a developer's reading of the client's
words, not an answer they gave. It was not put to them, because it only became
concrete once dependencies existed. **Worth one sentence to them before slice 2
adds Pillow** — if they meant the strict reading, the cost of finding out now is
one conversation, and the cost of finding out at delivery is a repackaging job
and the supersession of two ADRs.
