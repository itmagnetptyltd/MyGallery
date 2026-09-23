# Limits, configuration and feature flags

Reference chapter material. A flag that is off for the documented audience makes its feature not-documented, so record the state, not just the name.

## Limits and settings

| Name | Value in code | Confidence | Reference |
| --- | --- | --- | --- |
| MAX_UPLOAD | 20 | medium | .claude/itm-sdlc/scripts/dashboard.js:1012 |
| CHECK_MAX_DEPTH | 12 | medium | .claude/itm-sdlc/scripts/lib/installer.js:1016 |
| CHECK_MAX_FILES | 20000 | medium | .claude/itm-sdlc/scripts/lib/installer.js:1017 |
| MAX_PHOTO_BYTES | 25 | medium | src/mygallery/config.py:34 |
| MAX_BATCH_PHOTOS | 30 | medium | src/mygallery/config.py:39 |
| MAX_REQUEST_BYTES | MAX_BATCH_PHOTOS | medium | src/mygallery/config.py:40 |
| PAGE_SIZE | 60 | medium | src/mygallery/config.py:45 |
| MAX_DESCRIPTION_CHARACTERS | 250 | medium | src/mygallery/photos/store.py:52 |

## Feature flags

| Flag | State for the documented audience | Reference |
| --- | --- | --- |

## Browser support

No browserslist found. Ask the team, then record it here.
