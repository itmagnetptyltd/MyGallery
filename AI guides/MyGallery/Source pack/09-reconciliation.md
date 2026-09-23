# Freeze record and reconciliation

## Freeze record

| What | Value |
| --- | --- |
| Repository | `D:\practice\MyGallery` |
| Commit | `a00d0a40c55233de392118aeda6347d249382873` |
| Branch | `feat/gal-preview-and-description` |
| Working tree | Clean at harvest |
| Harvested | 2026-09-23 |
| Environment walked | The application itself, on a throwaway Gallery folder, driven by Playwright Chromium at 1280 by 860 |
| Application version | 0.1.0, from `pyproject.toml` |
| Python | 3.12 |

The walkthrough ran the real application through `werkzeug.serving.make_server`
on an ephemeral port, which is how `tests/conftest.py:139` runs it for belt B.
The Gallery folder was a throwaway directory, so no real Photo was touched.

## What was reconciled

Every label, message and limit was read from the repository, then confirmed
against a screenshot of the running application. The two agreed in every case,
so no label is carried on the repository's word alone.

| Source | Found | Confirmed against the app | Contradicted |
| --- | --- | --- | --- |
| Header, Gallery, popup, Larger view and confirmation labels | 21 | 20 | 0 |
| Upload refusal messages | 2 | 1 | 0 |
| Limits | 6 | 4 | 0 |
| Routes | 9 | 9 | 0 |

## Promoted to fact

| Fact | Was | Now | Because |
| --- | --- | --- | --- |
| The Gallery counts Photos in the header | Scraped as the literal `0` | A count of the Photos in the Gallery | `static/app.js:208` sets it from the total, and the walkthrough showed `6` after six Uploads |
| A refused file is reported as `<filename>: <reason>` | Inferred from `static/app.js:224` | Confirmed | `08-upload-refused.png` reads `notes.txt: not a supported image type` |
| A Thumbnail card carries `Download` and `Delete` without hovering | Inferred from `static/app.js:112,118` | Confirmed | `04-gallery-with-photos.png` shows both on all six cards |
| The description counter reads `<typed>/250` | Inferred from `static/app.js:303` | Confirmed | `03-upload-popup-chosen.png` reads `18/250` for 18 characters |

## Not confirmed against the running application

| Fact | Evidence it rests on | Why it was not reproduced |
| --- | --- | --- |
| `The Gallery could not be read.` | `templates/gallery.html:28`, `src/mygallery/web/api.py:79` | Needs an unreadable Gallery, which the walkthrough had no safe way to produce. The element is present and hidden in a healthy Gallery |
| `file is too large (max 25 MB)` | `src/mygallery/photos/validation.py:20-26`, `config.py:MAX_PHOTO_BYTES` | Not exercised. The message is assembled from the limit, so the number follows the configuration rather than being written out |

Both are documented from code evidence, and each is noted here so a later pass
can capture them rather than assume they were checked.

## Observed behaviour worth recording

**A batch of chosen files makes a tall Upload popup.** Each preview is as wide
as the description field, so choosing several files gives a popup the reader
scrolls. This is the agreed criterion of `REQ-GAL-015@v2`, asserted by
`tests/e2e/test_upload_preview_size_browser.py:56`, and not a defect. The manual
describes what the reader sees and does not present it as a fault.

**The Larger view opens on the Thumbnail the reader activates**, and its
description field carries that Photo's description, or is empty where it has
none. `06-larger-view.png` shows `0/250` for a Photo uploaded without one.

## Limits

| Limit | Value | Evidence |
| --- | --- | --- |
| Largest Photo | 25 MB | `config.py:MAX_PHOTO_BYTES` |
| Most files in one Upload | 30 | `config.py:MAX_BATCH_PHOTOS` |
| Accepted formats | JPEG, PNG, GIF, WebP | `config.py:ACCEPTED_FORMATS` |
| Longest description | 250 characters | `templates/gallery.html:80`, confirmed by the counter |
| Thumbnails loaded at a time | 60 | `config.py:PAGE_SIZE` |
| Address | `http://127.0.0.1:8765` | `config.py:HOST`, `config.py:PORT` |

The format list is matched on the file's content rather than its extension, so a
file renamed to `.jpg` is still refused. `src/mygallery/photos/validation.py:4`
records this, and `.brain/glossary.md` fixes it as part of the definition of an
accepted image format.
