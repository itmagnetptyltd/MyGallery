# Routes and screens

The harvester does not recognise Flask, so it returned no routes. This table is
taken from the application's own URL map, printed from `create_app()` at the
frozen commit, and confirmed against the running application.

Command used:

```
.venv/Scripts/python.exe -c "from mygallery.app import create_app; [print(sorted(r.methods-{'HEAD','OPTIONS'}), r.rule) for r in create_app().url_map.iter_rules()]"
```

## Screens

One screen: the application is a single page, and both the Upload popup and the
Larger view are `<dialog>` elements over it rather than addresses of their own.

| Screen | Address | In scope | Evidence |
| --- | --- | --- | --- |
| Gallery | `/` | Yes | `src/mygallery/web/pages.py`, `templates/gallery.html:1` |
| Upload popup | No address | Yes | `templates/gallery.html:44` |
| Larger view | No address | Yes | `templates/gallery.html:94` |
| Delete confirmation | No address | Yes | `templates/gallery.html:140` |

The Larger view has no address of its own by design: `.brain/glossary.md`
defines it as displayed over the Gallery, and `templates/gallery.html:40` records
that a native `<dialog>` keeps the Gallery's scroll position underneath.

## Application programming interface

Not documented for the end user, who never calls these directly. Listed so the
manual's authors can trace a screen behaviour to its request.

| Method | Route | Serves |
| --- | --- | --- |
| GET | `/` | The Gallery page |
| POST | `/api/photos` | Upload, one or more files in one request |
| GET | `/api/photos` | The Gallery's Photos, a page at a time |
| GET | `/api/photos/<photo_id>` | One Photo, full size, for the Larger view |
| GET | `/api/photos/<photo_id>/thumbnail` | One Thumbnail |
| GET | `/api/photos/<photo_id>/download` | One Photo as a download |
| DELETE | `/api/photos/<photo_id>` | Delete |
| PATCH | `/api/photos/<photo_id>/description` | Change a description |

## Not documented, with the reason

| Route | Reason |
| --- | --- |
| `/static/<path:filename>` | The application's own stylesheet and script, never requested by the reader |
| Every `/api/` route | Reached by the page, not by the user. No supported way for a reader to call one |
