# FB-0004 — A view and an optional description at Upload, shown as a tooltip on the Gallery; and a close control on the Upload popup

- **Received:** 2026-09-21
- **From:** KCB / DEV
- **Channel:** Chat
- **Anchors:** REQ-GAL-001, REQ-GAL-003, REQ-GAL-013
- **Triage:** proposed — variation
- **Sentiment:** neutral — a new feature, not a complaint about delivered work

## What they said

> In file upload after select file in upload or drag-drop a view and a
> description of max 250 char can given (not mandatory), on mousemove
> tooltip/alt will show this on gallery home items.

> On file upload popuo a close (X) on top right is needed so even without
> uploading I can close the popup

They stated, in the same exchange, that this is a new feature and not UAT on
the current popup.

## What we think it means

A reading, not a fact. Four separate asks, deliberately judged apart because
they can land on different sides of the scope line:

1. **A view of the selected file before it becomes a Photo.** After files are
   chosen — from the picker *or* by drag-and-drop — the popup shows the user
   what they picked, before the Upload happens.
2. **An optional description, at most 250 characters, given with the Upload.**
   "not mandatory" is explicit: an Upload with no description must still
   succeed. Whether the limit is enforced by refusing or by preventing
   over-typing is not stated.
3. **The description shown on Gallery home items on mousemove**, as a tooltip
   or as `alt`. The client names both and does not choose between them; they
   are different things to a screen reader.
4. **A close (X) control at top right of the Upload popup**, so it can be
   dismissed without uploading.

Ask 1 also introduces **drag-and-drop** as a way of choosing files. That is a
separate capability from showing a view of what was chosen, and is called out
here so it is not absorbed silently into ask 1.

Two things this ask does not settle, and which are not ours to settle:

- **Whether an existing Photo's description can be changed later.** The ask
  places the description at Upload only. Nothing says a Photo already in the
  Gallery can be given or given a new description.
- **What happens to the descriptions of Photos uploaded before this change.**
  Fourteen Photos are in the client's Gallery today with no description.

## What was done

`/find-variation` run 2026-09-21. `variation-agent` judged all five
elements against the agreed record: every one came back `not-covered`, so
every one is proposed as a **variation**. Five change records drafted:

| Ask | Change record |
|---|---|
| 1a — view of the selected file before Upload | CHG-0005 |
| 1b — drag-and-drop as a way of choosing files | CHG-0006 |
| 2 — optional description, max 250 characters | CHG-0007 |
| 3 — description on mousemove as tooltip/alt | CHG-0008 |
| 4 — close (X) on the Upload popup | CHG-0009 |

`decision:` and `commercial:` are blank in all five. No requirement version
has been moved. Absorbed, varied, deferred or declined is a person's call
and has not been made.
