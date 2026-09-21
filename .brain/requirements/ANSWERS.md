# Answers

Paste the client's reply here, under the question it answers. **Their words, not
a summary** — the wording behind every acceptance criterion stays in the
repository, and that is the point of this file.

Then run `/resolve-ambiguities`, which reads this file, writes the acceptance
criteria the answers produce, clears the questions from
`.brain/requirements/AMBIGUITIES.md` and `gal.yaml`, and moves the unblocked
requirements from `draft` to `agreed`.

Rules:

- An answer may be "I don't mind" — that is a real answer and closes the
  question. Record it as they said it.
- A question left blank stays open, and every requirement it blocks stays at
  `draft`.
- Nobody but the client closes a question. Not the developer, not an agent, and
  not by picking whichever reading is easier to build.

The full context for each question — what the brief says, what it could mean,
and what turns on the answer — is in `.brain/requirements/AMBIGUITIES.md`. This
file is only where the replies land.

---

## Is MyGallery a web application opened in a browser, or a program with its own window?

_Blocks: REQ-GAL-001, REQ-GAL-003, REQ-GAL-004, REQ-GAL-005, REQ-GAL-006, REQ-GAL-007, REQ-GAL-010, REQ-GAL-011_

_In plain words: When you want to look at your Gallery, do you expect to open your web browser, or to open MyGallery the way you open any other program on your PC?_

<!-- Paste the client's answer below, in their words. -->

I'd like to open it in my web browser. I'm happy to start it on my PC and then go to an address like http://localhost in Chrome or Edge. I don't need a separate program window.

---

## Does the application have any notion of a user, and may more than one person use it?

_Blocks: REQ-GAL-001, REQ-GAL-003, REQ-GAL-005, REQ-GAL-006, REQ-GAL-011_

_In plain words: Is MyGallery only ever used by you, on your own PC, with nobody needing to sign in?_

<!-- Paste the client's answer below, in their words. -->

Yes, it's just me, on my own PC. Nobody else uses it and I don't want to sign in. It only needs to work on this computer, not from other devices or over the internet.

---

## Must a Photo still be in the Gallery after the application is stopped and started again?

_Blocks: REQ-GAL-001, REQ-GAL-008_

_In plain words: If you close MyGallery and open it again tomorrow, should the photos you uploaded today still be there?_

<!-- Paste the client's answer below, in their words. -->

Yes, definitely. My photos must still be there tomorrow, and after I restart the PC. Please keep them in a normal folder on my disk that I can find and back up myself.

---

## Is a Thumbnail a separately stored smaller rendering of a Photo, or the Photo itself displayed small?

_Blocks: REQ-GAL-003_

_In plain words: If you upload fifty photos straight off a camera, is it acceptable for opening the Gallery to be slow the first time, or should it stay fast no matter how large the photos are?_

<!-- Paste the client's answer below, in their words. -->

It should stay fast. I'll often upload big photos straight off my phone, and I don't want to wait for the Gallery to open. If the app needs to make small preview copies to do that, that's fine.

---

## What may be installed on the client's PC, and which operating system must it run on?

_Blocks: REQ-GAL-011_

_In plain words: Which operating system is your PC running, and are you happy to install something once (and if so, what) before MyGallery will start?_

<!-- Paste the client's answer below, in their words. -->

I'm on Windows 11. I'm happy to install one thing once if you give me simple steps, like Python or Node.js. After that I want to start MyGallery by double-clicking a file or running one command, with nothing else to set up.

---

## Which image formats are accepted as a Photo?

_Blocks: REQ-GAL-001, REQ-GAL-010_

_In plain words: Which kinds of photo file do you expect to upload — what comes off your phone, your camera, or something else?_

<!-- Paste the client's answer below, in their words. -->

Normal photos: JPG/JPEG and PNG mostly, plus the occasional GIF or WebP. My phone is set to save JPG, so I don't need HEIC or camera RAW files. Please refuse anything else rather than trying to handle it.

---

## Is there a maximum size for a single Photo, or for the Gallery as a whole?

_Blocks: REQ-GAL-001, REQ-GAL-009_

_In plain words: What is the largest photo you would expect to upload, and roughly how many photos do you expect to keep in the Gallery?_

<!-- Paste the client's answer below, in their words. -->

My biggest photos are about 10 MB, so a limit of 25 MB per photo is fine and anything bigger can be refused. I expect to keep a few hundred photos, maybe up to 2,000 over time. I don't need a limit on the whole Gallery beyond my disk space.

---

## May more than one Photo be added in a single Upload?

_Blocks: REQ-GAL-001, REQ-GAL-009_

_In plain words: When you add photos, do you expect to pick them one at a time, or select a whole batch at once?_

<!-- Paste the client's answer below, in their words. -->

I want to select a whole batch at once, for example 20 or 30 photos from a folder. If some of them fail, keep the ones that worked and tell me which ones didn't go in.

---

## Is the Gallery shown all at once, or split into pages?

_Blocks: REQ-GAL-003_

_In plain words: Roughly how many photos do you expect to have in the Gallery — dozens, or thousands?_

<!-- Paste the client's answer below, in their words. -->

Hundreds, possibly a couple of thousand eventually. One scrolling page is fine, but it shouldn't get slow. Loading more as I scroll down is fine, and I don't want to click through numbered pages.

---

## In what order does the Gallery show Photos?

_Blocks: REQ-GAL-003_

_In plain words: When you open the Gallery, which photo do you expect to see first?_

<!-- Paste the client's answer below, in their words. -->

The newest one I uploaded should be first, with older ones further down.

---

## Is a deleted Photo recoverable, or is it gone for good?

_Blocks: REQ-GAL-005, REQ-GAL-008_

_In plain words: If you delete a photo by mistake, do you expect to be able to get it back?_

<!-- Paste the client's answer below, in their words. -->

No, once I delete it, it's gone. I don't need a recycle bin. That's why I want it to ask me first (see the confirmation question).

---

## Does Download deliver the Photo as it was uploaded, or its Thumbnail?

_Blocks: REQ-GAL-006_

_In plain words: When you download a photo, should you get back exactly the file you uploaded, at full quality?_

<!-- Paste the client's answer below, in their words. -->

Yes. I want exactly the file I uploaded, full size and full quality, never the small preview.

---

## Is the Larger view shown over the Gallery, or on a page of its own?

_Blocks: REQ-GAL-004_

_In plain words: After you have looked at a photo close up, how do you expect to get back to the Gallery — close it, or go back?_

<!-- Paste the client's answer below, in their words. -->

It should open on top of the Gallery and I'll close it with an X or the Escape key to get back to where I was. I don't need a separate page or a link for each photo.

---

## Is the user asked to confirm before a Photo is deleted?

_Blocks: REQ-GAL-005_

_In plain words: Should MyGallery ask "are you sure?" before deleting a photo?_

<!-- Paste the client's answer below, in their words. -->

Yes, please ask "Are you sure you want to delete this photo?" and only delete it if I say yes.

---

## What filename does a downloaded Photo carry on the user's machine?

_Blocks: REQ-GAL-006_

_In plain words: When you download a photo, what should the file be called in your downloads folder?_

<!-- Paste the client's answer below, in their words. -->

The same name it had when I uploaded it, e.g. IMG_1234.jpg. If that isn't possible for some reason, anything sensible that still ends in the right extension.

---

## What is the user shown when an Upload does not succeed?

_Blocks: REQ-GAL-009, REQ-GAL-010_

_In plain words: If a photo cannot be added, should MyGallery tell you, and would you want to know the reason?_

<!-- Paste the client's answer below, in their words. -->

Yes, always tell me, and tell me why in plain words, e.g. "not a supported image type", "file is too large (max 25 MB)" or "upload failed, please try again". For a batch, show which files failed and the reason for each.

---

## What does the Gallery show when it holds no Photos?

_Blocks: REQ-GAL-007_

_In plain words: The very first time you open MyGallery, before you have uploaded anything — what would you expect to see?_

<!-- Paste the client's answer below, in their words. -->

A friendly message like "No photos yet. Click Upload to add your first photos", with the Upload button easy to see. If something is actually broken, I'd want an error message instead of an empty screen.

---

# Questions raised 2026-09-21 (FB-0004)

The four below are **open**. Paste the client's reply under each, in their
words, then run `/resolve-ambiguities`.

---

## What is shown of the chosen files before the Upload is made?

_Blocks: REQ-GAL-001, REQ-GAL-013, REQ-GAL-015_

_In plain words: After you pick photos - or drop them in - but before they are added, what would you expect to see of them? Just the file names, one picture, or all of them? And what should that look like when you have picked thirty at once?_

<!-- Paste the client's answer below, in their words. -->

preview of that uploadede image.

## Is the 250-character description limit a refusal, or a typing limit?

_Blocks: REQ-GAL-001, REQ-GAL-017_

_In plain words: If you paste a description longer than 250 characters, should MyGallery refuse the upload and tell you why - or simply stop you typing past 250?_

<!-- Paste the client's answer below, in their words. -->

it will not allow to type/pest more then 250, and a count on ke prass 1/150 like this will indicate

## Can a description be changed after Upload, and what do existing Photos carry?

_Blocks: REQ-GAL-002, REQ-GAL-008, REQ-GAL-017_

_In plain words: Once a photo is in the Gallery, do you expect to be able to add or change its description later? And the photos already in your Gallery - should they stay without one?_

<!-- Paste the client's answer below, in their words. -->

Yes

## Tooltip or alt text?

_Blocks: REQ-GAL-003, REQ-GAL-012, REQ-GAL-018_

_In plain words: When you rest the mouse on a photo, should the description appear in the little box that pops up next to the pointer? Or should it be the photo's alt text - the words a screen reader reads out in place of the image?_

<!-- Paste the client's answer below, in their words. -->

photo's alt

---

# Questions raised 2026-09-21, second round

What the four answers above did not settle. Both were narrowed to exactly what
is missing rather than asked again in full.

---

## When several files are chosen at once, is every one previewed?

_Blocks: REQ-GAL-001, REQ-GAL-013, REQ-GAL-015_

_In plain words: You said you want a preview of the image before it is added. When you pick thirty photos at once, would you expect to see a small preview of all thirty, or just one?_

<!-- Paste the client's answer below, in their words. -->

---

## Where is a description changed after Upload?

_Blocks: REQ-GAL-002, REQ-GAL-008, REQ-GAL-017_

_In plain words: You said you want to be able to change a photo's description later. Where would you go to do that - open the photo large and edit it there, or somewhere on the Gallery page itself?_

<!-- Paste the client's answer below, in their words. -->

