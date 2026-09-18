# FB-0003 — Larger view buttons and close sit outside the panel

- **Received:** 2026-09-18
- **From:** KCB / DEV
- **Channel:** Chat
- **Anchors:** REQ-GAL-004, REQ-GAL-005
- **Triage:** proposed — preference
- **Sentiment:** negative

## What they said

> Onclick details the pannel need to redesign button and cross are out of side

## What we think it means

A reading, not a fact: activating a Thumbnail opens the Larger view, and the
close control (the cross) and the action button sit outside the panel. That
matches what was built: the close control is positioned above-right of the
dialog, and Delete sits below it. They want those controls redesigned so they
are not outside.

REQ-GAL-004 requires a close control. It does not say the control must sit
inside the panel. Slice 4 already noted that where Delete lives was never put
to the client. So this is proposed as preference about placement and look.

If, on their machine, the cross or the button is clipped and cannot be used,
that would be a defect against the close/delete criteria — they would not
have a working control. That has not been stated. Check before treating it
as one.

## Resolution

Absorbed 2026-09-18, no charge. `/find-variation` split this into two
asks. Ask 1 (redesign the panel) was `not-covered` and is CHG-0004.
Ask 2 (controls outside the panel) was `partial`; the absorbed call
places close and Delete inside the Larger view panel as REQ-GAL-004@v2
criteria. REQ-GAL-004 moved v1 → v2.
