# Errors and system messages

Copy the literal text into troubleshooting entries, punctuation and casing included, or the reader's search will not find them. Messages only a developer can trigger belong in the not-documented list.

| Message | Trigger | User can fix? | What to do | Confidence | Reference |
| --- | --- | --- | --- | --- | --- |
| ${arg} needs a value |  |  |  | medium | .claude/itm-sdlc/scripts/add-slice.js:103 |
| unknown option ${arg} |  |  |  | medium | .claude/itm-sdlc/scripts/add-slice.js:122 |
| --to requires a status |  |  |  | medium | .claude/itm-sdlc/scripts/advance-status.js:452 |
| --project requires a path |  |  |  | medium | .claude/itm-sdlc/scripts/advance-status.js:457 |
| --requirements requires a glob |  |  |  | medium | .claude/itm-sdlc/scripts/advance-status.js:463 |
| unknown option: ${arg} |  |  |  | medium | .claude/itm-sdlc/scripts/advance-status.js:467 |
| --to is required |  |  |  | medium | .claude/itm-sdlc/scripts/advance-status.js:473 |
| name at least one requirement id |  |  |  | medium | .claude/itm-sdlc/scripts/advance-status.js:475 |
| --g7-status requires a path |  |  |  | medium | .claude/itm-sdlc/scripts/check-belt-gates.js:63 |
| --today is not a date: ${options.today} |  |  |  | medium | .claude/itm-sdlc/scripts/check-constraints.js:81 |
| ${arg} requires a value |  |  |  | medium | .claude/itm-sdlc/scripts/check-constraints.js:178 |
| --within takes a whole number of days |  |  |  | medium | .claude/itm-sdlc/scripts/check-constraints.js:194 |
| could not run ${command}: ${result.error.message} |  |  |  | medium | .claude/itm-sdlc/scripts/check-secrets.js:287 |
| --format must be one of: ${FORMATS.join( |  |  |  | medium | .claude/itm-sdlc/scripts/client-report.js:272 |
| --format both needs --out <path> — stdout can only hold one document |  |  |  | medium | .claude/itm-sdlc/scripts/client-report.js:275 |
| --slice requires a number |  |  |  | medium | .claude/itm-sdlc/scripts/close-slice.js:97 |
| project not found: ${project} |  |  |  | medium | .claude/itm-sdlc/scripts/close-slice.js:197 |
| no slice ${options.slice} in .brain/slices.yaml |  |  |  | medium | .claude/itm-sdlc/scripts/close-slice.js:212 |
| not a file name |  |  |  | medium | .claude/itm-sdlc/scripts/dashboard.js:1044 |
| file too large |  |  |  | medium | .claude/itm-sdlc/scripts/dashboard.js:1045 |
| unknown mode: ${mode} |  |  |  | medium | .claude/itm-sdlc/scripts/hook-prompt-log.js:270 |
| unknown argument: ${arg} |  |  |  | medium | .claude/itm-sdlc/scripts/legacy-discover.js:77 |
| missing --text |  |  |  | medium | .claude/itm-sdlc/scripts/note.js:44 |
| ${relativeTo(projectDir, file)} names no REQ- id in its affects field |  |  |  | medium | .claude/itm-sdlc/scripts/regression-select.js:195 |
| give a CHG- id, or one or more REQ- ids |  |  |  | medium | .claude/itm-sdlc/scripts/regression-select.js:286 |
| not a CHG- or REQ- id: ${unrecognised.join( |  |  |  | medium | .claude/itm-sdlc/scripts/regression-select.js:294 |
| cannot mix a CHG- id with REQ- ids — give one CHG- id, or one or more REQ- ids |  |  |  | medium | .claude/itm-sdlc/scripts/regression-select.js:297 |
| only one CHG- id at a time: ${chgIds.join( |  |  |  | medium | .claude/itm-sdlc/scripts/regression-select.js:300 |
| could not produce a diff for ${range}: ${detail} |  |  |  | medium | .claude/itm-sdlc/scripts/review-change.js:157 |
| reviewer command failed to start: ${result.error.message} |  |  |  | medium | .claude/itm-sdlc/scripts/review-change.js:374 |
| reviewer command exited ${result.status}: ${(result.stderr \|\| |  |  |  | medium | .claude/itm-sdlc/scripts/review-change.js:376 |
| the reviewer returned nothing. A review that produced no output is not a pass. |  |  |  | medium | .claude/itm-sdlc/scripts/review-change.js:384 |
| the reviewer did not return usable JSON (${err.message}). |  |  |  | medium | .claude/itm-sdlc/scripts/review-change.js:394 |
| the reviewer returned JSON with no |  |  |  | medium | .claude/itm-sdlc/scripts/review-change.js:399 |
| supply --requirements or --pr-description so the reviewer knows what to check against. |  |  |  | medium | .claude/itm-sdlc/scripts/review-change.js:425 |
| pull request description not found: ${options.prDescription} |  |  |  | medium | .claude/itm-sdlc/scripts/review-change.js:428 |
| --requirements requires a comma-separated list |  |  |  | medium | .claude/itm-sdlc/scripts/review-change.js:506 |
| --requirements contained no valid REQ ids: ${argv[i]} |  |  |  | medium | .claude/itm-sdlc/scripts/review-change.js:508 |
| --exclude requires a path or glob |  |  |  | medium | .claude/itm-sdlc/scripts/review-change.js:514 |
| --requirements-glob requires a glob |  |  |  | medium | .claude/itm-sdlc/scripts/review-change.js:521 |
| --base is required |  |  |  | medium | .claude/itm-sdlc/scripts/review-change.js:539 |
| adapter has no commands.e2e |  |  |  | medium | .claude/itm-sdlc/scripts/run-browsertest.js:54 |
| --min-detection takes a number between 0 and 1 |  |  |  | medium | .claude/itm-sdlc/scripts/run-golden-set.js:277 |
| golden set not found: ${dir} |  |  |  | medium | .claude/itm-sdlc/scripts/run-golden-set.js:283 |
| no cases found in ${options.set} |  |  |  | medium | .claude/itm-sdlc/scripts/run-golden-set.js:440 |
| --schema requires a path |  |  |  | medium | .claude/itm-sdlc/scripts/validate-requirements.js:74 |
| --cwd requires a path |  |  |  | medium | .claude/itm-sdlc/scripts/validate-requirements.js:79 |
| cannot load schema at ${schemaPath}: ${err.message} |  |  |  | medium | .claude/itm-sdlc/scripts/validate-requirements.js:350 |
| target does not exist: ${resolvedTarget} |  |  |  | medium | .claude/itm-sdlc/scripts/lib/installer.js:550 |
| target is not a directory: ${resolvedTarget} |  |  |  | medium | .claude/itm-sdlc/scripts/lib/installer.js:553 |
| not a file: ${source} |  |  |  | medium | .claude/itm-sdlc/scripts/lib/working.js:254 |
