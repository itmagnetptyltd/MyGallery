# ADR-0001 — MyGallery is built on Python 3.12, with Python as the one prerequisite

- **Status:** accepted
- **Date:** 2026-09-18
- **Governs:** src/**, tests/**, e2e/**, pyproject.toml, README.md

## Context

`REQ-GAL-011` requires that the application start on the client's Windows 11 PC
after installing **at most one prerequisite**, and then start with a single
command or a single file to open. The client was asked which software they were
willing to install and answered:

> I'm happy to install one thing once if you give me simple steps, like Python
> or Node.js. After that I want to start MyGallery by double-clicking a file or
> running one command, with nothing else to set up.

(`.brain/requirements/ANSWERS.md`, 2026-09-18)

That answer fixed the *constraint* — one install, one command — without choosing
which runtime. It is the last thing standing between the agreed requirements and
slice 1, because nothing under `src/` can be written until it is settled.

Two further client answers bear on the choice. The Gallery must "stay fast" with
large phone photos, which means Thumbnails are generated and stored rather than
being full-size Photos shown small (`REQ-GAL-003`). And the application is
reached in a browser at a local address, never from another device
(`REQ-GAL-011`), so this is a local HTTP server, not a desktop GUI.

The toolkit ships working adapters for both candidates
(`.claude/itm-sdlc/adapters/`), so either would have been buildable and gateable.
This was a real choice between two viable options, not a formality.

## Decision

**Python 3.12 or later.** Python is the single prerequisite named in the start
instructions. The application is a local HTTP server serving a browser front end,
started with one command documented in `README.md`.

Thumbnail generation uses **Pillow**. Tests run under **pytest** with coverage
enforced at 80%, and **ruff** for linting, matching the commands the python
adapter already declares:

```
test        pytest -q
coverage    pytest --cov --cov-fail-under=80 -q
lint        ruff check .
integration pytest -q -m integration
```

Belt B (browser) uses Playwright's Python bindings.

## Alternatives considered

**Node.js 20+ with plain JavaScript.** This was the recommendation put to the
developer, and it lost. Its case was real: `node:test` is built into the runtime,
so belt A would have cost no dependency at all on a project whose rules argue
against unnecessary ones; the toolkit's `rules/javascript/` is several pages
against `rules/python/`'s four lines; and the CI container was already
`node:20-bookworm`. It was rejected in favour of Python on the developer's call.

**A packaged desktop application with its own window** (Electron, Tauri, PyQt).
Ruled out earlier, by the client rather than here: they said they expected to
open a browser and go to a local address, and did not want a separate program
window. It would also have meant an installer per operating system rather than
one runtime install.

**Bundling a runtime so there is no prerequisite at all** (PyInstaller, or a
Node single-executable build). This would have satisfied `REQ-GAL-011` most
literally — zero installs, one file to double-click. Rejected because it adds a
build step between the source and the thing that runs, which makes the
application harder to inspect and change, and because the client volunteered
that one install was acceptable. Worth revisiting only if the one install turns
out to be a real obstacle for them.

## Consequences

**Makes easy.** Thumbnail generation: Pillow is mature, pure-Python to install on
Windows, and needs no native toolchain. The standard library covers an HTTP
server, path handling and content-type detection, so slice 1 needs little beyond
the runtime. `pathlib.Path.resolve()` with a containment check is the idiomatic
answer to the path-traversal risk that `REQ-GAL-002` and the static file server
both carry.

**Makes hard.** Three things, stated plainly because they were the argument
against this option:

- **Testing needs installs the client does not need.** `pytest`, `pytest-cov`,
  `ruff` and Playwright are all beyond the one prerequisite. This does not
  violate `REQ-GAL-011` — that criterion is about *starting the application*, not
  about running its test suite — but the distinction has to be kept visible in
  `README.md`, which must separate "to run MyGallery" from "to work on
  MyGallery". If those two sections blur, the criterion's test will be measuring
  the wrong list.
- **`rules/python/` is thin.** Four lines, against several pages for JavaScript.
  The detailed guidance on secrets, input validation, static file serving and
  dependency review in `rules/javascript/security.md` has no Python counterpart
  in this repository, but the substance of it still applies. Reviewers should
  read it as the intent even though the adapter will not select it.
- **Packaging for a non-technical user is harder than `npm start`.** Getting from
  "Python is installed" to "one command" on Windows needs care — `py -m` versus
  `python`, and whether a `.cmd` shim is wanted for the double-click option.

**Rules out.** A TypeScript or JavaScript implementation of the same
application. Mixing runtimes — a Python server with a Node build step for the
front end — is specifically excluded: it would reintroduce the second install
this decision exists to avoid, and would break the one-prerequisite criterion.

**Consequence for work already in flight.** The slice 1 plan at
`.brain/sessions/2026-09-18-plan-REQ-GAL-011.md` was written against Node.js and
is now wrong in its Approach, file list and test skeleton. It must be reissued
against Python before `/tdd REQ-GAL-011`. Its non-runtime findings still hold —
in particular that belt C reports `integration=missing` while six agreed
requirements list belt C, which makes G7 fail-closed repository-wide; under this
decision the fix is a `pytest -q -m integration` path that exits clean over an
empty belt-C set, not an npm script.

**Not decided here.** Which HTTP layer — the standard library's `http.server`,
or a small framework such as Flask or FastAPI. That is a separate choice, cheap
to make once slice 1 is planned, and it does not change the prerequisite count
either way. Where Photos are stored on disk (`REQ-GAL-008`) is also still open
and belongs in its own ADR when slice 2 is planned.
