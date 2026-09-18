# FB-0002 — File upload should be from a popup

- **Received:** 2026-09-18
- **From:** KCB / DEV
- **Channel:** Chat
- **Anchors:** REQ-GAL-001
- **Triage:** proposed — variation
- **Sentiment:** negative

## What they said

> File upload should be from a popup

## What we think it means

A reading, not a fact: Upload should open in a dialog, not sit as the header
control it is today. REQ-GAL-001 is satisfied by picking files and having them
become Photos. No agreed criterion requires a popup. Putting Upload behind a
new surface is extra behaviour, so this is proposed as a variation, not a
defect.

REQ-GAL-009's failure list would need a home on that popup if the change is
taken.

## Resolution

Absorbed 2026-09-18, no charge. `/find-variation` returned `not-covered`.
CHG-0003 moved REQ-GAL-001 and REQ-GAL-007 v1 → v2. Upload is started
from a popup; the empty Gallery still shows a control that opens it.
