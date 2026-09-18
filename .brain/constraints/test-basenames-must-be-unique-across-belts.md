# pytest cannot collect two test files sharing a basename across the belt directories

- **Discovered:** 2026-09-18
- **Review by:** 2027-03-18
- **Source:** measured on this repository, 2026-09-18 — `pytest` collection
  error after slice 2 created `tests/test_gallery.py` alongside
  `tests/e2e/test_gallery.py`
- **Affects:** `tests/`, `tests/api/`, `tests/e2e/` — every test file this
  project will ever add

## The constraint

The three belts live in three directories — `tests/` (A), `tests/e2e/` (B) and
`tests/api/` (C) — and none of them has an `__init__.py`. Without packages,
pytest imports each test file as a top-level module named after its basename,
so two files called `test_gallery.py` in different belt directories are two
modules with the same name, and collection fails:

```
ERROR collecting tests/test_gallery.py
import file mismatch:
imported module 'test_gallery' has this __file__ attribute:
  D:\practice\MyGallery\tests\e2e\test_gallery.py
which is not the same as the test file we want to collect:
  D:\practice\MyGallery\tests\test_gallery.py
HINT: remove __pycache__ / .pyc files and/or use a unique basename
```

**The trap is that each file passes on its own.** `pytest tests/e2e` was green
and `pytest tests/` was green; only the full suite failed. A developer running
the belt they are working on sees nothing wrong, and the failure surfaces later
— in CI, or for whoever runs everything next.

This will keep happening, because the belts naturally want the same names. One
requirement's behaviour gets a unit file, an API file and a browser file, and
the obvious name for all three is the same word.

## How we know

Reproduce by creating `tests/thing_test.py` and `tests/e2e/thing_test.py`, each
containing one passing test, then running `pytest` from the project root. Each
directory passes alone; together they error at collection.

Observed at commit `e1f5006` when `tests/test_gallery.py` (REQ-GAL-003 ordering
and paging) met `tests/e2e/test_gallery.py` (the same requirement in a browser).

## What we do about it

**In place now:** the e2e file was renamed to `tests/e2e/test_gallery_browser.py`.
The convention this project follows is that a belt-B file ends `_browser` and a
belt-C file ends `_http`, so basenames stay unique by construction:

| Belt | Directory | Suffix |
|---|---|---|
| A | `tests/` | none — `test_gallery.py` |
| B | `tests/e2e/` | `_browser` — `test_gallery_browser.py` |
| C | `tests/api/` | `_http` — `test_photos_http.py` |

**The permanent fix, not applied:** add an empty `__init__.py` to `tests/`,
`tests/api/` and `tests/e2e/`. That makes each file a distinct module by
package path and removes the constraint entirely. It was not done in slice 2
because no acceptance criterion called for it and `/tdd` forbids scope the plan
did not name. It is a two-minute change worth making deliberately.

**Do not** resolve a future collision by deleting `__pycache__` — the hint in
pytest's own message is misleading here. The caches are a symptom; the shared
module name is the cause, and it recurs on the next clean checkout.
