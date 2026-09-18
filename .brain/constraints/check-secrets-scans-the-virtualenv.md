# The local secret scan reads `.venv/` and buries real findings under third-party noise

- **Discovered:** 2026-09-18
- **Review by:** 2027-03-18
- **Source:** measured on this repository, 2026-09-18 —
  `node .claude/itm-sdlc/scripts/check-secrets.js --project . --advisory`,
  run before and after `python -m venv .venv`
- **Affects:** `/verifyReq` step 3, `.claude/itm-sdlc/scripts/check-secrets.js`;
  not CI

## The constraint

`check-secrets.js` walks the working tree without consulting `.gitignore`. Once a
virtual environment exists, it reads every file in it.

Measured on the same repository, hours apart:

| When | Files scanned | Blocking findings |
|---|---|---|
| Before `.venv/` existed | 101 | 0 |
| After slice 1 created `.venv/` | 3003 | **76** |

**All 76 are inside `.venv/`** — pip, requests, urllib3, werkzeug, Playwright.
They are that code's own handling of passwords and tokens, matched by the
`connection-string-password` and `assigned-secret` patterns. 31 distinct files.
Filtering the output for any path outside `.venv/` returns nothing, and
`git check-ignore` confirms `.gitignore:46` (`**/.venv/**`) excludes all of it,
so none can reach a commit.

**The risk is not the false positives. It is that a real credential in our own
code would now be one line among seventy-six**, in a check that still exits 0
because it ships advisory. The scan has not become wrong; it has become
unreadable, which for a security check is the same thing.

This does **not** affect CI. A GitHub runner checks out a fresh clone with no
`.venv/`, so the gate there still scans ~100 files. It is a local-only hazard,
which makes it worse rather than better: the local run is the one a developer
does before pushing, and it is the one that now says nothing useful.

## How we know

```
$ node .claude/itm-sdlc/scripts/check-secrets.js --project . --advisory
  scanned  3003 file(s)
  ... 76 BLOCKING ...
  76 blocking, 0 other  |  mode: advisory
  ADVISORY - reported, build not failed.          EXIT: 0

$ ... | grep -v '^\.venv/'        # every flagged path
  (no output)

$ git check-ignore -v .venv/Lib/site-packages/requests/auth.py
  .gitignore:46:**/.venv/**   .venv/Lib/site-packages/requests/auth.py
```

Re-measure by running the scan and checking whether any flagged path falls
outside `.venv/`. The moment one does, that finding is real and this constraint
does not apply to it.

## What we do about it

**Nothing is in place.** Recorded as a live hazard.

Until it is fixed, **read the scan by filtering to paths outside `.venv/`**
rather than by reading its verdict line. A run reporting "76 blocking" and a run
reporting "77 blocking" look identical at a glance, and the difference is the
one that matters.

The fix belongs in the toolkit, not this project: `check-secrets.js` should
respect `.gitignore`, or take an ignore list. Adding `.venv/` to some
project-level exclusion here would fix one directory and leave `node_modules/`
and every other vendored tree for the next person to rediscover.

Do **not** resolve this by deleting `.venv/` before scanning, or by moving the
virtual environment outside the project — both make the scan look clean while
changing nothing about what it would miss.
