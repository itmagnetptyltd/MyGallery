# ADR-0002 — Flask is the HTTP layer, chosen at slice 1 for slice 2's sake

- **Status:** accepted
- **Date:** 2026-09-18
- **Governs:** src/mygallery/app.py, src/mygallery/web/**, src/mygallery/templates/**, src/mygallery/static/**, pyproject.toml `[project].dependencies`

## Context

[[ADR-0001]] chose Python 3.12+ and explicitly left the HTTP layer open —
"stdlib `http.server`, or a small framework such as Flask or FastAPI" — on the
grounds that it was cheap to decide once slice 1 was planned. This is that
decision.

Slice 1 (`REQ-GAL-011`) needs almost nothing from an HTTP layer: it serves one
page, one stylesheet, and binds to loopback. On slice 1's own merits the
standard library wins outright.

The pressure comes from slice 2. `REQ-GAL-001` requires uploading a batch of
thirty files in one Upload, which is a `multipart/form-data` body. Python's only
standard-library multipart parser lived in the `cgi` module, which was
deprecated in 3.11 and **removed in 3.13** — a version ADR-0001's "3.12 or
later" explicitly permits. There is no stdlib replacement.

## Decision

**Flask** (`>=3.0,<4.0`), adopted in slice 1 rather than deferred. The
application is a Flask app created by a factory in `src/mygallery/app.py`;
routes are blueprints under `src/mygallery/web/`; Flask serves the template and
static asset.

The developer was shown both options with their costs and chose this one.

## Alternatives considered

**Standard library `http.server` now, a framework later.** Genuinely viable, and
the honest YAGNI answer for slice 1 in isolation: zero runtime dependencies, and
a hand-written handler of perhaps forty lines. It lost on what happens next —
either hand-rolling multipart parsing in slice 2 (not a thing to do to save one
dependency) or swapping the HTTP layer at slice 2, which rewrites `app.py` and
invalidates slice 1's tests. Deciding once is cheaper than deciding twice.

**FastAPI.** Named in ADR-0001 alongside Flask. Not chosen: it brings an ASGI
server and Pydantic for an application with no API contract to validate and one
user, and its advantages are concurrency and typed schemas — neither of which
this project needs. Flask is the smaller commitment.

**Deferring the decision to slice 2.** Rejected because it is not a real option:
slice 1 has to serve a page somehow, and whatever serves it becomes the thing
slice 2 either keeps or rewrites. A deferred decision here is just an undocumented
one.

## Consequences

**Makes easy.** Multipart upload in slice 2 arrives free via Werkzeug, including
the batch case and per-file access. Routing, content types, safe static serving
and `url_for` are all handled by code that is already correct — which matters
more than it looks, because a hand-rolled static server is the single most
common place this class of project develops a path-traversal hole.

**Makes hard / costs.**

- Slice 1 carries a dependency it does not need. A reviewer looking only at this
  slice would be right to call it over-engineering; the justification is
  entirely in slice 2, and that is why it is written down here.
- **Flask's built-in server is the production server for this project.** For a
  single-user application bound to loopback that is defensible, and adding
  Waitress or Gunicorn would be a second dependency for no benefit the client
  can observe. Recorded deliberately so it is not later read as an oversight. It
  stops being defensible the moment this application is exposed beyond loopback
  — which `REQ-GAL-011` forbids.
- One more thing the start script must install. See [[ADR-0003]], which settles
  whether that breaches `REQ-GAL-011`'s one-prerequisite criterion.

**Rules out.** A zero-dependency MyGallery. That was already impossible from
slice 2 onward because `REQ-GAL-003` needs Pillow for Thumbnails, so this
decision does not close a door that was open.

**Revisit if** the client ever asks to reach MyGallery from another device.
That would contradict `REQ-GAL-011` and require a change record, but it would
also make the built-in server inadequate, and this ADR would need superseding
rather than amending.
