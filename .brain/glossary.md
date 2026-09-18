# Glossary

Terms are **fixed** on this project. Use these words, spelled this way, and no
synonyms — in requirements, in code, in tests, in conversation with the client.

A term used in a requirement but not defined here is an **ambiguity**, not a
decision anyone may make on the client's behalf. Record it and ask.

---

## Why this file exists

A client described one thing three ways in a single meeting:

> "When a **job** comes in we assign it to a crew."
> "Each **engagement** has a start date and a purchase order."
> "The customer can cancel a **booking** up to 24 hours before."

Three words. The team built:

- a `Job` table for scheduling,
- an `Engagement` record for billing, because it "obviously" carried the PO,
- a `Booking` API for the customer-facing app.

They were the same entity. It was discovered in UAT, when cancelling a booking
left the job scheduled and the engagement billable. The fix touched three
schemas, two APIs and a migration — about three weeks — and none of it was
visible as a defect until real users produced all three views of one record.

**The cost was not the rework. It was that nobody could see it coming**, because
each team was individually consistent and the disagreement lived in the gaps
between them.

Pinning one word at discovery would have cost five minutes.

---

## How to write an entry

**Term** — what it means here, in one sentence. Then, where it matters:
- **Not to be confused with:** the near-synonym people reach for, and how it differs
- **Also called:** what the client says, when it differs from the agreed term
- **Identified by:** what makes two of these the same one

Define the term the *client's business* uses, not the one the database uses. If
they diverge, that divergence is itself worth writing down.

---

## Agreed terms

All terms below are settled. The client answered every open question on
2026-09-18; their words are in `requirements/ANSWERS.md`.

**Photo** — one image the user has uploaded to this application.
- **Not to be confused with:** a *Thumbnail*, which is a rendering of a Photo,
  not a Photo in its own right. Deleting a Photo removes its Thumbnail; there is
  no way to delete a Thumbnail alone.
- **Also called:** the client says "photo" throughout the brief. Not "image",
  "file", "picture" or "asset" — none of those words appear in our code.
- **Identified by:** an identifier the application issues on Upload. Not the
  caller-supplied filename, which is not unique and is not trusted.

**Accepted image format** — JPEG, PNG, GIF or WebP. Nothing else is a Photo.
HEIC and camera RAW are explicitly excluded, and unsupported content is refused
rather than converted or guessed at.
- **Identified by:** the content of the file, not its extension. A file renamed
  to `.jpg` is not a JPEG.

**Gallery** — the complete set of Photos the application shows. Singular: there
is one Gallery in this application, belonging to the one person who uses it.
- **Not to be confused with:** an *album* or a *collection*. The brief describes
  no grouping of Photos below the Gallery, and none may be invented.
- **Ordered by:** Upload time, most recently uploaded Photo first.

**Thumbnail** — the small rendering of a Photo shown in the Gallery, stored
separately from the Photo and smaller than it, so that opening the Gallery does
not transfer full-size Photos.

**Larger view** — the Photo shown bigger after the user activates its Thumbnail,
displayed **over** the Gallery and dismissed with Escape or a close control,
returning to the same place in the Gallery. It is not a separate page and has no
address of its own.

**Upload** — the act of adding one or more Photos to the Gallery. One Upload may
carry a batch of files; each file in it succeeds or fails on its own.

**Download** — the act of retrieving a Photo as a file onto the user's machine.
Always the Photo exactly as it was uploaded, byte for byte, under its original
filename — never the Thumbnail.

**Delete** — the act of removing a Photo and its Thumbnail from the Gallery.
Permanent: there is no recycle bin and nothing is recoverable. The user is
asked to confirm before it happens.

**The user** — the one person who uses MyGallery, on their own Windows 11 PC.
There is no sign-in, no account, and no second user. The application is reached
in a web browser on that PC only, and refuses connections from other devices.

---

## Appears in source documents, not yet defined

Nothing. Every term the brief used without settling is defined above.

A term used in a future requirement but not defined here is an **ambiguity**,
not a decision anyone may make on the client's behalf. Add it here, add the
matching question to `requirements/AMBIGUITIES.md`, and ask.
