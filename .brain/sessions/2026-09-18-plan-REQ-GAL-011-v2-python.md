# Plan — REQ-GAL-011@v1 (v2, Python)

Slice 1, **Boot** (`.brain/slices.yaml`, branch `feat/gal-boot`).

**Supersedes `2026-09-18-plan-REQ-GAL-011.md`**, which was written against
Node.js before ADR-0001 chose Python. Do not build from that file.

Gate: `close-slice.js --gate REQ-GAL-011` passes — no earlier slice exists.
`REQ-GAL-011` is `agreed`, `version: 1`, no `depends_on`, and is the only id in
the slice. Belts **A and B**; no belt C here.

Governing record read before designing:

- **ADR-0001** — Python 3.12+, one prerequisite, no build step. Governs
  `src/**`, `tests/**`, `e2e/**`, `pyproject.toml`, `README.md`, so it governs
  every file this slice creates.
- **constraints/g3-passes-vacuously-with-no-adapter-manifest.md** — this slice
  lands the `pyproject.toml` that clears it.
- **constraints/g7-blocks-once-a-belt-c-requirement-is-agreed.md** — still
  unfixed, and it will fail this slice's pull request.
- `.brain/rejected/` is empty. Nothing here has been tried and abandoned.

---

## What must be true

1. **A browser on the client's PC reaches a displayed Gallery** after the
   documented start steps on Windows 11.
2. **The start instructions are complete** — no undocumented step is needed.
3. **Exactly one prerequisite** must be installed before the application starts.
4. **Starting is one command, or one file to open.**
5. **Not reachable from another device.** A connection from elsewhere on the
   network is refused.

Criterion 1 means the Gallery *page* loads with an empty Gallery region. What it
**says** when it holds no Photos is `REQ-GAL-007`, which is slice 2. Building the
no-Photos-yet message here would make slice 2's tests pass before slice 2 exists.

### The reading of criterion 3 this plan commits to

Pillow is required by `REQ-GAL-003` and Flask by this plan, so the application
will never have zero pip dependencies. Criterion 3 is therefore read as:
**Python is the one thing the client installs; the application's own
dependencies are part of installing the application, not a second
prerequisite.** `README.md` must keep "to run MyGallery" and "to work on
MyGallery" in visibly separate sections, because the criterion-3 test counts
only the first list. If you disagree with this reading, correct it now — it
shapes the README, the test, and the start script.

## Approach

Python 3.12+, **Flask** as the HTTP layer, served by the built-in server bound
explicitly to `127.0.0.1` — which is what satisfies criterion 5, as a property of
the bind address rather than a firewall the client configures. Standard
src-layout: the application is the package `src/mygallery`, so everything the app
is made of is under `src/`, including Flask's `static/` and `templates/`. A
`scripts/start.cmd` creates a virtual environment, installs dependencies and
starts the server, so the client has **one file to double-click**; `python -m
mygallery` is the equivalent single command for anyone who prefers a terminal.
Configuration lives in one module so the port the README names and the port the
server binds cannot drift apart — a test asserts they match.

**Flask rather than the standard library, and this is the part to argue with.**
Slice 1 alone does not need it: it serves three static files, and
`http.server` would do. The case for deciding now is slice 2, which needs
multipart upload of a thirty-file batch (`REQ-GAL-001`). Python's `cgi` module —
the stdlib's only multipart parser — was deprecated in 3.11 and **removed in
3.13**, which ADR-0001's "3.12 or later" explicitly permits. Hand-rolling
multipart parsing is not a thing to do to save one dependency, and switching the
HTTP layer at slice 2 would invalidate slice 1's tests. One well-known
dependency now is cheaper than a rewrite in a fortnight. The alternative —
stdlib now, framework later — is viable and costs a rewrite; say so if you
prefer it.

Files created:

```
pyproject.toml                      root — metadata, deps, pytest and ruff config
README.md                           root — start instructions; criteria 2-4 test this
scripts/start.cmd                   venv, install, run — the double-click route
src/mygallery/__init__.py
src/mygallery/__main__.py           python -m mygallery
src/mygallery/config.py             HOST 127.0.0.1, PORT, paths
src/mygallery/app.py                app factory, security headers
src/mygallery/web/__init__.py
src/mygallery/web/pages.py          the Gallery shell route
src/mygallery/templates/gallery.html
src/mygallery/static/app.css
tests/test_config.py
tests/test_app.py
tests/test_binding.py
tests/test_start_instructions.py
tests/e2e/test_boot.py              belt B
```

`tests/e2e/` rather than a root `e2e/`: the adapter's `e2eGlobs` include
`**/tests/e2e/**/*.py`, and a root `e2e/` is not on the list of directories
permitted beside `src/`.

## Test skeleton

Annotation form is `# @covers REQ-GAL-011@v1`. Tests marked *(hardening)* carry
no annotation — the rules require the behaviour, but no slice-1 requirement
names it.

**Belt A — `tests/` (`pytest -q`)**

`tests/test_config.py`
- `test_the_server_is_configured_to_listen_on_loopback_only`
  → host is `127.0.0.1`; not `0.0.0.0`, not empty. *(5)*
- `test_the_configured_port_matches_the_port_in_the_start_instructions`
  → parses `README.md`, asserts it equals `config.PORT`.

`tests/test_binding.py`
- `test_a_started_server_reports_a_loopback_bound_address` *(5)*
- `test_a_started_server_refuses_a_connection_to_the_machine_network_address`
  → connects to a non-loopback IPv4 from `socket`/`ifaddr` on the same port,
    expects `ConnectionRefusedError`. `skipif` when no such interface exists. *(5)*

`tests/test_app.py`
- `test_requesting_the_root_path_serves_the_gallery_page`
  → 200, `text/html`, body contains the Gallery region. *(1)*
- `test_the_gallery_page_is_served_with_a_content_security_policy` *(hardening)*
- `test_the_gallery_page_is_served_with_nosniff` *(hardening)*

`tests/test_start_instructions.py`
- `test_the_start_instructions_name_exactly_one_prerequisite`
  → parses the Prerequisites section of `README.md`, asserts one entry. *(3)*
- `test_the_start_instructions_reach_a_running_application_in_a_single_step`
  → asserts the run section names exactly one command or one file. *(4)*
- `test_the_documented_start_file_exists`
  → the file `README.md` tells the client to open is on disk. *(4)*

**Belt B — `tests/e2e/` (Playwright)**

`tests/e2e/test_boot.py`
- `test_following_the_documented_start_steps_displays_the_gallery`
  → starts the app with the documented command only, navigates, asserts the
    Gallery region is visible. *(1, 2)*
- `test_the_gallery_is_reachable_at_the_documented_address`
  → address read from `README.md`, not hardcoded, so the two cannot drift. *(1)*

| Criterion | Covered by |
|---|---|
| 1 displayed in a browser | `test_app.py`, `tests/e2e/test_boot.py` (both) |
| 2 instructions complete | `tests/e2e/test_boot.py` — proxy only |
| 3 one prerequisite | `test_start_instructions.py` |
| 4 one command / one file | `test_start_instructions.py` (two tests) |
| 5 refused from the network | `test_config.py`, `test_binding.py` |

## Decisions this forces

1. **The HTTP layer — Flask.** ADR-0001 explicitly left this open. Approving
   this plan settles it, and it should be written up as **ADR-0002** rather than
   left implicit in a slice-1 diff. The reasoning is in *Approach* above; the
   deciding factor is `cgi`'s removal in 3.13, not a preference for Flask.
2. **Flask's built-in server is the production server here.** For a
   single-user application bound to loopback that is defensible, and Waitress
   would be one more dependency for no gain the client can see. It belongs in
   ADR-0002 as a stated consequence, so nobody later reads it as an oversight.
3. **`pytest -q -m integration` exits 5 when no test matches.** This is
   pytest's `EXIT_NOTESTSCOLLECTED`, and belt C has no tests until slice 2 — so
   the command the G7 constraint says to declare may be read by the gate as a
   failure. **I have not measured this**, because pytest is not installed yet; it
   is an expectation to verify while wiring `pyproject.toml`, not a finding. If
   it holds, the fix is a wrapper that treats 5 as success, not a fake
   integration test — a test that cannot fail is worse than none.
4. **`scripts/start.cmd` versus a root `start.cmd`.** The rules permit
   `scripts/` for project tooling and do not list a root start file; but this one
   is user-facing, which is not what "tooling" means. I have put it in
   `scripts/` to stay inside the rule. **Your call** if you would rather it sat
   at the root where the client will look first.

Deferred, and not needed to close this slice: **where Photos are stored on
disk** (`REQ-GAL-008`). `config.py` gains that path in slice 2; it is its own ADR
when it lands.

## What I am unsure about

- **Criterion 2 cannot be mechanically tested.** "Followed by someone who has
  not worked on the project" is a human check. The e2e test performs only the
  documented steps, so it fails if something undocumented is needed — that is a
  proxy, and I would not report this criterion verified on it alone. The real
  check is the README on a clean Windows 11 machine.
- **Criterion 5's second test skips** on a machine with no non-loopback IPv4
  interface. The bind-address assertion always runs and is the load-bearing one.
  A skip that reads as a pass is exactly what `rules/python/testing.md` warns
  about, so it is flagged rather than hidden.
- **The criterion-3 reading above is a judgement, not a client answer.** If the
  client meant "one install, full stop", then `pip install` breaks it and the
  answer is a bundled runtime — which ADR-0001 considered and rejected. Worth
  one sentence to them before slice 2 adds Pillow.
- **Playwright's config location.** Python Playwright needs no config file, so
  the problem the Node plan had does not arise — but browser binaries still need
  `playwright install`, which is a developer step and must stay out of the
  client's prerequisites section or the criterion-3 test will measure the wrong
  list.
- **80% coverage** over a slice this small is sensitive to how much of
  `__main__.py` is the `run` call. If it comes in under, move logic out of the
  entry point rather than lowering the threshold.

## This slice's effect on the two open constraints

- **Clears `g3-passes-vacuously-with-no-adapter-manifest.md`.** `pyproject.toml`
  makes the python adapter detectable. After the first green run, re-run
  `check-traceability.js --project . --strict`, confirm `scanned` is non-zero,
  and delete that constraint file — leaving it would cast doubt on a gate that
  had started working.
- **Does not clear `g7-blocks-once-a-belt-c-requirement-is-agreed.md`.** This
  slice's pull request will still fail G7 as `not-configured`, because no
  reviewer is resolvable in CI. Expect it, and do not treat it as a defect in
  slice 1.

---

## Waiting for approval

**No code has been written.** Nothing outside `.brain/sessions/` was touched.

Approve or correct before `/tdd REQ-GAL-011`. The two worth your attention are
**Flask as the HTTP layer** (decision 1) and **the reading of criterion 3**
above — both are cheapest to change now.
