# User interface labels

Verbatim. Every label below was read from the template or the script at the
frozen commit, then confirmed against a screenshot of the running application.
The manual quotes these exactly, including capitalisation and punctuation.

The application has no internationalisation catalogue, so the template is the
only source. The harvester's 153 scraped strings included class names and
script identifiers, and are superseded by this table.

## Header

| Label | Element | Evidence | Confirmed in |
| --- | --- | --- | --- |
| `MyGallery` | Page title and heading | `templates/gallery.html:6,11` | `01-empty-gallery.png` |
| `Upload photos` | Button | `templates/gallery.html:14` | `01-empty-gallery.png` |
| A count of Photos, as a number alone | Text | `static/app.js:208` | `04-gallery-with-photos.png` |

## Gallery

| Label | Element | Evidence | Confirmed in |
| --- | --- | --- | --- |
| `No photos yet. Click Upload photos to add your first photos.` | Empty-Gallery message | `templates/gallery.html:24` | `01-empty-gallery.png` |
| `The Gallery could not be read.` | Error message | `templates/gallery.html:28` | Not reproduced. See the note below |
| `Download` | Link on each Thumbnail card | `static/app.js:112` | `04-gallery-with-photos.png` |
| `Delete` | Button on each Thumbnail card | `static/app.js:118` | `04-gallery-with-photos.png` |

`The Gallery could not be read.` is served when the Gallery cannot be opened.
It is present but hidden in a healthy Gallery, which is what
`tests/e2e/test_gallery_browser.py:48` asserts. It was not reproduced during the
walkthrough, so it is evidenced from the template and the route at
`src/mygallery/web/api.py:79` rather than from a screenshot.

## Upload popup

| Label | Element | Evidence | Confirmed in |
| --- | --- | --- | --- |
| `Choose photos to add to the Gallery.` | Instruction | `templates/gallery.html:56` | `02-upload-popup-empty.png` |
| `Choose files` | Button | `templates/gallery.html:58` | `02-upload-popup-empty.png` |
| `Description (optional)` | Field label | `templates/gallery.html:74` | `03-upload-popup-chosen.png` |
| `What is this photo?` | Placeholder in the description field | `templates/gallery.html:83` | `02-upload-popup-empty.png` |
| `Upload` | Button | `templates/gallery.html:89` | `03-upload-popup-chosen.png` |
| `Close` | Accessible name of the cross, top right | `templates/gallery.html:52` | `02-upload-popup-empty.png` |
| A count, as `<typed>/250` | Character count | `static/app.js:303` | `03-upload-popup-chosen.png`, reading `18/250` |

The cross itself is the character `×`, and `Close` is its accessible name
rather than visible text.

## Larger view

| Label | Element | Evidence | Confirmed in |
| --- | --- | --- | --- |
| `Description` | Field label | `templates/gallery.html:110` | `06-larger-view.png` |
| `Save description` | Button | `templates/gallery.html:124` | `06-larger-view.png` |
| `Close` | Button | `templates/gallery.html:133` | `06-larger-view.png` |
| `Close` | Accessible name of the cross, top right | `templates/gallery.html:100` | `06-larger-view.png` |
| A count, as `<typed>/250` | Character count | `static/app.js:303` | `06-larger-view.png`, reading `0/250` |

The Larger view carries two controls that close it, the cross at the top right
and the `Close` button beside `Save description`. Both are evidenced, and
`REQ-GAL-014@v2` is the requirement that put the second one there.

## Delete confirmation

| Label | Element | Evidence | Confirmed in |
| --- | --- | --- | --- |
| `Are you sure you want to delete this photo?` | Question | `templates/gallery.html:142` | `07-delete-confirmation.png` |
| `Keep it` | Button, declines | `templates/gallery.html:145` | `07-delete-confirmation.png` |
| `Delete` | Button, confirms | `templates/gallery.html:146` | `07-delete-confirmation.png` |

`templates/gallery.html:138` records that the client gave the question's wording
verbatim and that it is a criterion of `REQ-GAL-005`, not a caption. It is
quoted exactly and never reworded.

## Australian English

The house style is Australian English, and no label above contradicts it. The
application's labels carry no US spelling, so the manual's conventions section
has no clash to record.
