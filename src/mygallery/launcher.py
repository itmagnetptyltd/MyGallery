"""Starting MyGallery.

Separate from __main__.py so that starting the application is testable: the
entry point is a shim over `start()` and holds no logic of its own.
"""

import webbrowser
from collections.abc import Callable

from mygallery import config
from mygallery.app import create_app


def address() -> str:
    """Where the Gallery is reachable — the address README.md names."""
    return f"http://{config.HOST}:{config.PORT}"


def start(
    app_factory: Callable[[], object] = create_app,
    open_browser: Callable[[str], object] = webbrowser.open,
    announce: Callable[[str], object] = print,
) -> None:
    """Start the application and show it to the user.

    One step, because REQ-GAL-011 requires starting to be a single command or
    a single file to open — so this opens the browser rather than asking the
    user to.
    """
    url = address()
    announce(f"MyGallery is running at {url}")
    open_browser(url)
    app_factory().run(host=config.HOST, port=config.PORT)
