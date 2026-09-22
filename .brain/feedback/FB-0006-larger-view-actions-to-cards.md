# FB-0006 — Download and Delete move from the Larger view to each card

- **Received:** 2026-09-22
- **From:** KCB / DEV
- **Channel:** Chat, with one screenshot
- **Anchors:** REQ-GAL-004, REQ-GAL-014, REQ-GAL-005, REQ-GAL-006, REQ-GAL-003, REQ-GAL-012
- **Triage:** proposed — see What was done
- **Sentiment:** neutral — a change to where delivered controls sit, not a report that something is broken

## What they said

> In Preview there will be Save Description and close button, and with item
> bottom there will be download and delete

The screenshot shows the delivered Larger view in the dark theme: a round
white close (×) at top right, the Photo, "Description" with a 33/250 count
and the text "A screenshoot of existing project", and a row of three buttons
beneath it — "Save description", "Download" and "Delete". Nothing else was
said.

## What we think it means

A reading, not a fact. "Preview" is read as the Larger view — the panel in the
screenshot. "item" is read as a Thumbnail card in the Gallery. Three separate
asks:

1. **The Larger view keeps only Save description and the close control.**
   Download and Delete are no longer in it.
2. **Each Thumbnail card carries a Download control at its bottom.**
3. **Each Thumbnail card carries a Delete control at its bottom.**

The sentence does not say whether the card controls are always shown or only
on hover, and does not say whether Delete on a card still asks "Are you sure
you want to delete this photo?" first (REQ-GAL-005@v1 c4 requires it
wherever Delete is).

One thing in the record bears directly on asks 1 and 3. FB-0003 (2026-09-18)
asked for the Larger view controls to sit inside the panel, and the absorbed
decision placed Delete inside the Larger view panel: REQ-GAL-004@v2 c7 and
REQ-GAL-014@v1 c2. This ask moves Delete out of that panel.

## What was done

`/find-variation` run 2026-09-22. `variation-agent` judged the three asks
against the agreed record. No duplicate was found: FB-0003 set where Delete
sits and is the answer ask 1 reverses, not the same ask.

| Ask | Verdict | Classification | Change record |
|---|---|---|---|
| 1 — Larger view keeps only Save description and close | contradicts REQ-GAL-014@v1 c2, REQ-GAL-004@v2 c7 | variation | CHG-0014 |
| 2 — Download at the bottom of each card | not-covered | variation | CHG-0015 |
| 3 — Delete at the bottom of each card | not-covered | variation | CHG-0016 |

`decision:` and `commercial:` are blank in all three. No requirement version
has been moved. Absorbed, varied, deferred or declined is a person's call and
has not been made.
