"""What a downloaded Photo is called.

REQ-GAL-006 criterion 4 requires the caller's own filename back. That string is
untrusted input kept since Upload, and this is the only place in the
application where it is handed to anything other than storage as data.

It is still never used as a path — ADR-0004 names the file on disk after the
identifier, and nothing here changes that. The name decided here becomes a
`Content-Disposition` header value and nothing else.
"""

from mygallery import config

# Anything below space, plus DEL. A newline here is header injection; a NUL
# truncates. None of them belongs in a filename a user actually chose.
_CONTROL_CHARACTERS = frozenset(chr(code) for code in list(range(32)) + [127])


def download_name(filename: str, image_format: str, photo_id: str) -> str:
    """The name to deliver a Photo under.

    Returns the uploaded filename when it can be used, and otherwise
    `<identifier><extension>` — REQ-GAL-006 criterion 5, which is the
    requirement's own escape hatch for a name that cannot be delivered.
    """
    candidate = (filename or "").strip()

    if _is_usable(candidate):
        return candidate

    extension = config.EXTENSION_FOR_FORMAT.get(image_format, ".bin")
    return f"{photo_id}{extension}"


def _is_usable(candidate: str) -> bool:
    if not candidate:
        return False
    # A separator is what makes traversal possible; "." and ".." name a
    # directory rather than a file. A name merely containing dots — say
    # "holiday..jpg" — is unusual, not dangerous, and is left alone.
    if "/" in candidate or "\\" in candidate:
        return False
    if candidate in {".", ".."}:
        return False
    return not any(character in _CONTROL_CHARACTERS for character in candidate)
