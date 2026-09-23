# Terminology

One term per thing, across the manual and every companion document.

These terms are **fixed by the project**, in `.brain/glossary.md`, which states
that they are settled and that no synonym may be used in requirements, code,
tests or conversation with the client. The manual inherits that ruling: a term
below is not a documentation preference and is not renamed to read more easily.

A term used in the manual but absent from `.brain/glossary.md` is an ambiguity
for the client to settle, not a choice the writer makes.

## Fixed by the project

| Term | Means | Never called |
| --- | --- | --- |
| Photo | One image the reader has uploaded | image, file, picture, asset |
| Gallery | The complete set of Photos the application shows. There is one | library, collection, album |
| Thumbnail | The small rendering of a Photo shown in the Gallery | preview, tile, icon |
| Larger view | The Photo shown bigger over the Gallery, after the reader activates its Thumbnail | lightbox, modal, full screen, detail page |
| Upload | Adding one or more Photos to the Gallery | import, add files, attach |
| Download | Retrieving a Photo as a file, exactly as uploaded | export, save as, get |
| Delete | Removing a Photo and its Thumbnail, permanently | remove, discard, trash, archive |
| Accepted image format | JPEG, PNG, GIF or WebP, judged by content and not by extension | supported file type, allowed format |

## Capitalisation

`.brain/glossary.md` capitalises Photo, Gallery, Thumbnail, Upload, Download and
Delete as the defined terms of this product, and the manual follows it. Where a
word is used in its ordinary sense rather than as the defined term, it is lower
case: "a photo you took on your phone" is not yet a Photo, and becomes one at
its Upload.

`Larger view` carries a capital `L` and a lower-case `v`, as the glossary spells
it.

## Terms the interface uses that the glossary does not define

Each is a label rather than a concept, quoted verbatim from `02-labels.md` and
formatted as a control rather than as a term.

| Label | What it is |
| --- | --- |
| `Upload photos` | The button that opens the Upload popup |
| `Choose files` | The button that opens the file picker |
| `Description (optional)` | The description field in the Upload popup |
| `Save description` | The button that stores a changed description |
| `Keep it` | The button that declines a deletion |

## Words this manual does not use

| Not this | Because |
| --- | --- |
| click, tap | Device verbs. The house style uses `select`, `open`, `enter` |
| simply, just, easily | Tells the reader how they should feel about a step |
| dialog, modal, popup as a noun for the Larger view | The glossary names it the Larger view |
| app | The manual says "the application", or "MyGallery" |

`popup` is used for the Upload popup alone, because `REQ-GAL-013` names it that
and the client's own words are "Upload is started from a popup".
