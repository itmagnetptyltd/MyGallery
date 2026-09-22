# FB-0005 — A bigger Upload popup, bigger previews, a white border, and buttons like the other panels

- **Received:** 2026-09-21
- **From:** KCB / DEV — passed on as a PDF, "Increase Upload model size.pdf"; the document names no author
- **Channel:** Document (PDF with one screenshot)
- **Anchors:** REQ-GAL-013, REQ-GAL-015, REQ-GAL-019, REQ-GAL-014
- **Triage:** proposed — variation (see What was done)
- **Sentiment:** neutral — a change to the look of delivered work, not a report that something is broken

## What they said

> Increase Upload model size, after upload preview/show will be in a bigger
> way and border a white line and buttons and close buttons will be like as in
> other forms

The screenshot beneath it shows the delivered Upload popup in the dark theme:
the line "Choose photos to add to the Gallery.", a "Choose files" button, one
small preview tile of a chosen image, "Description (optional)" with a 59/250
count, an "Upload" button at bottom right, and a round white close (×) at top
right. Nothing else was said.

## What we think it means

A reading, not a fact. Four separate asks, judged apart because they can land
on different sides of the scope line:

1. **The Upload popup is larger.** "model" is read as *modal* — the Upload
   popup in the screenshot. No size is named.
2. **The previews of chosen files are shown larger.** "after upload" is read
   as *after files are chosen*: the screenshot shows the preview of a file
   that has been chosen but not yet uploaded, and once an Upload is made the
   popup no longer shows anything. No size is named.
3. **A white line as a border.** Read as a white border around the Upload
   popup, matching the white-bordered Larger view panel. The sentence does
   not say what the border goes around; it could also be read as a border
   around each preview.
4. **Buttons and the close button look as they do "in other forms".** The
   only other panel in the application is the Larger view, whose close
   control and Save description / Delete buttons are styled differently from
   the Upload popup's close control and Upload / Choose files buttons. Read
   as: make the Upload popup's controls match the Larger view's.

One thing in the record bears directly on ask 2. The client's recorded answer
of 2026-09-21 (ANSWERS.md, "When several files are chosen at once, is every
one previewed?") is: "Yes. A small preview of every chosen file, including
thirty." Larger previews move away from that answer, and with thirty files
chosen, larger previews mean more scrolling inside the popup.

## What was done

`/find-variation` run 2026-09-21. `variation-agent` judged the four asks
against the agreed record: every one came back `not-covered`, so every one is
proposed as a **variation**. No duplicate was found: FB-0001 concerned the
Gallery cards and FB-0003 the placement of the Larger view controls, and no
earlier feedback or change record asks about the Upload popup's size, border
or control styling. Four change records drafted:

| Ask | Change record |
|---|---|
| 1 — a larger Upload popup | CHG-0010 |
| 2 — larger previews of chosen files | CHG-0011 |
| 3 — a white border | CHG-0012 |
| 4 — buttons and close styled like the Larger view | CHG-0013 |

`decision:` and `commercial:` are blank in all four. No requirement version
has been moved. Absorbed, varied, deferred or declined is a person's call and
has not been made.
