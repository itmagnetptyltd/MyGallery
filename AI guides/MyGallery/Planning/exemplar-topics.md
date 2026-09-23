# Exemplar topics: MyGallery user manual

This file is the voice reference for the manual, and its prose is copied verbatim into the draft rather than rewritten.

## 1. About this manual

MyGallery 0.1.0 on Windows 11 is what this manual describes. It covers starting
the application, adding Photos, looking at them, describing them, downloading
them and deleting them.

| What | Value |
| --- | --- |
| Product | MyGallery 0.1.0 |
| Document version | 1.0 |
| Date | 2026-09-23 |
| Audience | The person who uses MyGallery on their own Windows 11 PC |

Developing MyGallery is not covered here. `README.md` holds that material, in
its "Working on MyGallery" section.

### Conventions

**Bold** names a control you act on, such as a button, a field label or a key.
`Code font` names a file, a folder or a web address. Text the application
displays is quoted in double quotation marks, exactly as it appears on screen.

A callout is one of five kinds:

| Callout | What it means |
| --- | --- |
| **Note** | Worth noticing even when you are skimming |
| **Tip** | Optional advice that saves you time |
| **Important** | Essential to getting the task done |
| **Caution** | You could lose work, or have to do something again |
| **Warning** | Certain or severe: something is removed for good |

Photo, Gallery, Thumbnail, Upload, Download and Delete carry a capital letter,
because each names something particular in MyGallery. Larger view carries a
capital L alone. A photo in lower case is one you have not added yet, and it
becomes a Photo at its Upload.

A label or message is quoted exactly as it is written on screen, even where its
wording differs from this manual's. An empty Gallery reads "No photos yet. Click
Upload photos to add your first photos." This manual's own instructions say
select rather than click. Windows Security is Microsoft's product, not part of
MyGallery. Its labels keep the United States spelling and the ampersand the
screen shows, as in **Virus & threat protection**.

## 2. What MyGallery is

MyGallery keeps your photos on your own PC and shows them together as one
Gallery. A photo you add becomes a Photo, with a Thumbnail in the Gallery. From
its Thumbnail you can see a Photo at a larger size, describe it, download it, or
delete it.

You reach MyGallery in your web browser, from a program you start on your PC.
There is no sign-in and no account, and no other device on your network can
reach it. See [Where your Photos are kept, and who can reach them](#101-where-your-photos-are-kept-and-who-can-reach-them).

| To | Chapter |
| --- | --- |
| Get MyGallery running the first time | [3. Before you start](#3-before-you-start) |
| Start and stop MyGallery | [4. Starting and stopping MyGallery](#4-starting-and-stopping-mygallery) |
| Add your first Photo | [5. Getting started: your first Photo](#5-getting-started-your-first-photo) |
| Learn what is on the screen | [6. The Gallery screen](#6-the-gallery-screen) |
| Add more Photos | [7. Adding Photos](#7-adding-photos) |
| Find a Photo and see it larger | [8. Looking at Photos](#8-looking-at-photos) |
| Describe a Photo | [9. Describing Photos](#9-describing-photos) |
| Download a Photo, or back up your Gallery | [10. Getting your Photos back out](#10-getting-your-photos-back-out) |
| Delete a Photo | [11. Removing Photos](#11-removing-photos) |
| Check a limit or an accepted format | [12. Reference](#12-reference) |
| Find out why something is not working | [13. When something does not work](#13-when-something-does-not-work) |
| Check what a word means | [14. Glossary](#14-glossary) |

## 4. Starting and stopping MyGallery

### 4.1 Start MyGallery

Starting MyGallery opens your Gallery in your web browser, and you do it at the
start of every session.

**Before you begin**

- Python 3.12 or later is installed. See [3.2 Install Python](#32-install-python).

**To start MyGallery:**

1. Open `scripts/start.cmd`. A black window opens, and MyGallery runs only
   while that window stays open.
2. Wait for your web browser to open at `http://127.0.0.1:8765`. The first run
   takes a minute while MyGallery prepares itself, and every run after that is
   immediate.

**Result:** Your Gallery is shown in your web browser at
`http://127.0.0.1:8765`.

**See also:**

- [4.3 Stop MyGallery](#43-stop-mygallery)
- [13.8 Windows blocked MyGallery from creating its Gallery folder](#138-windows-blocked-mygallery-from-creating-its-gallery-folder)
- [13. When something does not work](#13-when-something-does-not-work), where MyGallery will not start or the browser does not open

## 9. Describing Photos

### 9.1 Where a description is shown

A Photo's description is the alt text of its Thumbnail. Alt text is what a
screen reader announces in place of an image, and what a browser shows where the
image itself cannot be displayed.

A Photo with no description carries its filename as alt text instead, so every
Thumbnail has something to announce.

The same description is in the **Description** field of that Photo's Larger
view, which is where you change it. Changing it there changes the Thumbnail's
alt text with it.

A description is yours alone, because MyGallery is reached from your own PC
only. It does not rename the Photo's file, and it does not group Photos. The
Gallery holds one set, ordered by Upload time with the most recent Photo first.

**See also:**

- [9.2 Describe a Photo as you upload it](#92-describe-a-photo-as-you-upload-it)
- [9.3 Change a Photo's description](#93-change-a-photos-description)
- [6.2 What a Thumbnail card shows](#62-what-a-thumbnail-card-shows)

## 10. Getting your Photos back out

### 10.1 Where your Photos are kept, and who can reach them

Your Photos are files in `Pictures\MyGallery`, inside your own user folder. That
folder holds every Photo you have uploaded, the Thumbnails MyGallery renders
from them, and the index MyGallery reads to show them.

A Photo is an ordinary file there, so you can copy it in File Explorer. Its file
is named for the identifier MyGallery issued at its Upload, not for the name you
uploaded it under. A Download delivers the Photo under the filename you uploaded
it with.

Nothing leaves your PC, because MyGallery listens on your own machine only. A
connection from another computer, phone or tablet on your network is refused.

Deleting a Photo removes its file and its Thumbnail from that folder. Nothing is
kept anywhere else, so a deleted Photo cannot be recovered.

**See also:**

- [10.2 Download a Photo](#102-download-a-photo)
- [10.3 Back up your Gallery](#103-back-up-your-gallery)
- [11.1 Delete a Photo](#111-delete-a-photo)

## 13. When something does not work

### 13.1 What happens when part of an Upload fails

One Upload carries up to 30 files, and each file in it succeeds or fails on its
own. The files that worked are Photos in the Gallery, and one file failing does
not undo them.

Each file that failed is named on the Gallery page, with the reason beside its
name, as in "notes.txt: not a supported image type". A file is refused where it
is not in an accepted image format, or where it is larger than 25 MB.

A file that fails leaves nothing behind: no Photo is added for it, and no part
of it is kept.

**See also:**

- [13.2 Some of the files you chose are not in the Gallery](#132-some-of-the-files-you-chose-are-not-in-the-gallery)
- [13.3 A file was refused as not a supported image type](#133-a-file-was-refused-as-not-a-supported-image-type)
- [13.4 A file was refused as too large](#134-a-file-was-refused-as-too-large)
- [12.1 Which files become a Photo](#121-which-files-become-a-photo)
- [12.2 Limits](#122-limits)

### 13.8 Windows blocked MyGallery from creating its Gallery folder

MyGallery shows "The Gallery could not be read." where it could not create its
Gallery folder. This happens on the first run, before you have uploaded
anything.

Controlled folder access, part of Windows Security, is turned on and is stopping
MyGallery from creating its Gallery folder at `Pictures\MyGallery`. Windows does
not report that block as a refusal, so nothing on the screen names the cause.

**To allow MyGallery through Controlled folder access:**

1. Open **Windows Security**.
2. Select **Virus & threat protection**.
3. Go to **Ransomware protection**. Its **Controlled folder access** section
   shows a switch reading **On** while the feature is turned on.
4. In that section, select **Allow an app through Controlled folder access**.
5. On the page that opens, allow MyGallery.
6. Start MyGallery again. See [4.1 Start MyGallery](#41-start-mygallery).

**Result:** Your Gallery is shown in place of the message.

**See also:**

- [13.9 The Gallery says it could not be read](#139-the-gallery-says-it-could-not-be-read)
- [10.1 Where your Photos are kept, and who can reach them](#101-where-your-photos-are-kept-and-who-can-reach-them)
