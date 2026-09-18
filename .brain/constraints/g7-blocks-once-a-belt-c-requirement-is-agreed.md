# G7 blocks every pull request as soon as one belt-C requirement reaches `agreed`

- **Discovered:** 2026-09-18
- **Review by:** 2027-03-18
- **Source:** measured on this repository, 2026-09-18 — `check-belt-gates.js --json`;
  `.github/workflows/gates.yml` job `g7-conformance` (lines 800–803);
  `.claude/itm-sdlc/scripts/lib/belts.js` `COUNTED_STATUSES` and `g7MustFail`
- **Affects:** `.github/workflows/gates.yml`, every pull request on this project;
  REQ-GAL-001, REQ-GAL-003, REQ-GAL-005, REQ-GAL-006, REQ-GAL-009, REQ-GAL-010

## The constraint

G7 becomes **fail-closed the moment a belt-C requirement reaches `agreed`** — not
when belt-C code is written, and not when a belt-C test is due. On this project
that happened on 2026-09-18, when `/resolve-ambiguities` moved eleven
requirements from `draft` to `agreed`. Six of them list belt C.

The chain, each link verified:

1. `belts.js` counts a requirement toward `requiresC` when its status is any of
   `agreed`, `in_progress`, `verified`, `signed_off` — `COUNTED_STATUSES`,
   line 133. `agreed` is the first of those, so the trigger is agreement, not
   implementation.
2. `check-belt-gates.js --json` now reports `requiresC: true`,
   `integrationDeclared: false`.
3. `gates.yml` line 803 sets `continue-on-error: ${{ needs.detect.outputs.requires_c != 'true' }}`.
   With `requires_c == true` that evaluates to `false`, so the job blocks the
   merge instead of reporting.
4. `g7MustFail(requiresC, state)` (`belts.js` line 128) fails the job when the
   G7 state is any of `not-configured`, `not-installed`, `no-output`,
   `harness-error`.
5. A GitHub-hosted runner has no `claude` binary, and this repository has no
   `ITM_SDLC_REVIEWER_CMD` secret set. `review-change.js` therefore resolves to
   **`not-configured`**, which is in that list.

**Consequence: the first pull request opened on this repository will fail G7,
for a reason that has nothing to do with what is in it.** A slice 1 pull request
containing only `REQ-GAL-011` — which lists belts A and B, no C — fails anyway,
because `requires_c` is a property of the whole requirement record, not of the
diff.

## How we know

```
$ node .claude/itm-sdlc/scripts/check-belt-gates.js --project . --json
requiresB: True
requiresC: True
integrationDeclared: False
idsC: REQ-GAL-001, REQ-GAL-003, REQ-GAL-005, REQ-GAL-006, REQ-GAL-009, REQ-GAL-010
```

```
$ node .claude/itm-sdlc/scripts/check-belt-gates.js --project .
belts  B=REQ-GAL-001,...,REQ-GAL-011  C=REQ-GAL-001,...,REQ-GAL-010  integration=missing
```

Re-measure by running either command from the project root. The gate header
comment at `gates.yml` lines 17–18 states the same rule in prose; the behaviour
above was read from the job definition and `belts.js` rather than taken from the
comment, because a header comment can describe an intention the code does not
implement.

## What we do about it

**Nothing is in place yet.** This is recorded as an open trap, not a solved
problem. Three routes, none applied:

1. **Configure a reviewer.** Set the `ITM_SDLC_REVIEWER_CMD` repository secret so
   `review-change.js` resolves to something. This is the route the gate was
   designed for, and the only one that makes G7 do its job rather than merely
   stop failing.
2. **Declare the belt-C integration command.** Under ADR-0001 the python
   adapter supplies `pytest -q -m integration`. Slice 1 landed the
   `pyproject.toml` that makes the adapter detectable and registered the
   `integration` marker in it, which clears `integration=missing`. It does
   **not** on its own clear a `not-configured` G7.

   **Measured 2026-09-18, after slice 1:** that command exits **5**, not 0.

   ```
   $ .venv/Scripts/python.exe -m pytest -q -m integration
   19 deselected in 0.02s
   EXIT: 5
   ```

   5 is pytest's `EXIT_NOTESTSCOLLECTED`, and belt C has no tests until slice 2
   writes them. So the command the gate is told to run reports failure for a
   suite that is simply empty. This was written into the slice 1 plan as an
   expectation to verify; it is now verified, and it is unfixed.

   The fix is a wrapper that treats exit 5 as success — **not** a placeholder
   integration test. A test that cannot fail is worse than no test, because it
   makes the gate report a belt that is not being exercised.
3. **Run the reviewer locally before pushing**, per `/verifyReq` step 4c:
   `review-change.js --base main --head HEAD --requirements REQ-...`. A local
   machine usually does have a `claude` binary. This gets the review done but
   does not change what CI reports.

Do **not** resolve this by moving requirements back to `draft`, by removing belt
C from a requirement that needs it, or by adding G7 to an allow-list. The gate
is correct; the project is simply not configured for it yet.
