# Harvest summary

First pass over the repository. It finds candidates. It does not confirm them.

**Stack detected:** unrecognised
**Commit:** `a00d0a40c55233de392118aeda6347d249382873` on `feat/gal-preview-and-description`

| What | Found | Where |
| --- | --- | --- |
| Routes and screens | 0 | `01-routes.md` |
| UI labels | 153 | `02-labels.md` |
| Validation files | 0 | `03-fields.md` |
| Roles and permissions | 0 | `04-permissions.md` |
| Error messages | 51 | `05-errors.md` |
| Limits and settings | 8 | `06-config-limits.md` |
| Feature flags | 0 | `06-config-limits.md` |
| End-to-end tests | 75 | `07-tasks.md` |
| Commits since last tag | 52 | `08-release-history.md` |
| Screens queued for capture | 0 | `10-capture-list.json` |
| Images already in the repository | 0 | `11-existing-images.md` |

## Next

1. Confirm the freeze record, from `assets/source-pack-template.md`, names this commit (`a00d0a40c55233de392118aeda6347d249382873`) and the environment. The target is frozen before the harvest, so every fact here is true as at that commit.
2. Mark each route in scope or out of scope. Out-of-scope routes go on the not-documented list with a reason.
3. Prune `10-capture-list.json` to the screens the manual needs, fill in any route parameters, then capture:
   `python scripts/capture_shots.py --list 10-capture-list.json --base-url <staging-url> --out images/`
4. Walk the in-scope routes in the running app, one record per screen.
5. Reconcile, then continue with Phase 1 of the manual workflow.

Confidence is the harvester's, not the product's. Confirm every `low` row against the running app before it reaches the manual, and treat `medium` as a prompt to look.
