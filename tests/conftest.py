"""Shared fixtures.

Parsing lives here rather than in the test bodies, so each test is an
assertion and nothing else.
"""

import re
import socket
import threading
from dataclasses import dataclass
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def project_root() -> Path:
    return PROJECT_ROOT


# --- the start instructions -------------------------------------------------


@pytest.fixture(scope="session")
def readme_text() -> str:
    return (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def readme_sections(readme_text: str) -> dict[str, str]:
    """`## Heading` -> the lines beneath it, up to the next `## `."""
    sections: dict[str, str] = {}
    heading: str | None = None
    body: list[str] = []
    for line in readme_text.splitlines():
        match = re.match(r"^##\s+(.*)$", line)
        if match:
            if heading is not None:
                sections[heading] = "\n".join(body)
            heading, body = match.group(1).strip(), []
        elif heading is not None:
            body.append(line)
    if heading is not None:
        sections[heading] = "\n".join(body)
    return sections


def _bullets(section: str) -> list[str]:
    return [
        line.strip()[2:].strip()
        for line in section.splitlines()
        if line.strip().startswith("- ")
    ]


@pytest.fixture(scope="session")
def prerequisites(readme_sections: dict[str, str]) -> list[str]:
    """What the client must install before MyGallery will start.

    Only the "Before you start" section counts. Anything a *developer* needs
    lives under a different heading and is deliberately not counted here —
    see the criterion-3 reading in the slice 1 plan.
    """
    return _bullets(readme_sections["Before you start"])


@pytest.fixture(scope="session")
def run_steps(readme_sections: dict[str, str]) -> list[str]:
    return _bullets(readme_sections["Run MyGallery"])


@pytest.fixture(scope="session")
def documented_start_file(run_steps: list[str]) -> str:
    match = re.search(r"`([^`]+)`", run_steps[0])
    assert match is not None, "the run step names no file or command in backticks"
    return match.group(1)


@pytest.fixture(scope="session")
def documented_port(readme_text: str) -> int:
    ports = {int(p) for p in re.findall(r"127\.0\.0\.1:(\d+)", readme_text)}
    assert len(ports) == 1, f"the start instructions name {len(ports)} ports, expected 1"
    return ports.pop()


# --- photos -----------------------------------------------------------------


def an_image(fmt: str = "JPEG", size: tuple[int, int] = (64, 48)) -> bytes:
    """Real encoded image bytes. Validation reads content, so fakes will not do."""
    from io import BytesIO

    from PIL import Image

    buffer = BytesIO()
    Image.new("RGB", size, (200, 120, 60)).save(buffer, format=fmt)
    return buffer.getvalue()


@pytest.fixture
def gallery_dir(tmp_path, monkeypatch):
    """Point the application at a throwaway Gallery folder for one test."""
    from mygallery import config

    root = tmp_path / "MyGallery"
    monkeypatch.setattr(config, "GALLERY_DIR", root)
    monkeypatch.setattr(config, "PHOTO_DIR", root / "photos")
    monkeypatch.setattr(config, "THUMBNAIL_DIR", root / "thumbnails")
    monkeypatch.setattr(config, "INDEX_PATH", root / "index.db")
    return root


@pytest.fixture
def store(gallery_dir):
    from mygallery.photos.store import PhotoStore

    return PhotoStore.open()


# --- the application --------------------------------------------------------


@pytest.fixture
def client(gallery_dir):
    from mygallery.app import create_app

    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


@dataclass(frozen=True)
class RunningServer:
    host: str
    port: int


@pytest.fixture
def running_server(gallery_dir):
    """The real app on a real socket, bound the way the application binds it."""
    from werkzeug.serving import make_server

    from mygallery import config
    from mygallery.app import create_app

    # Port 0 so tests never collide with a real instance; the host under test
    # is config.HOST, which is the thing the criterion is about.
    server = make_server(config.HOST, 0, create_app())
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield RunningServer(host=server.server_address[0], port=server.server_address[1])
    finally:
        server.shutdown()
        thread.join(timeout=5)


def lan_ipv4() -> str | None:
    """A non-loopback IPv4 address of this machine, or None if it has none."""
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            address = info[4][0]
            if not address.startswith("127."):
                return address
    except OSError:
        return None
    return None


def a_noisy_image(size: tuple[int, int] = (1400, 1100)) -> bytes:
    """A large PNG that does not compress away.

    REQ-GAL-003 compares a Thumbnail's byte size against its Photo's, so the
    Photo has to be genuinely big. A flat colour compresses to a few hundred
    bytes and would make that comparison meaningless.
    """
    import random
    from io import BytesIO

    from PIL import Image

    rng = random.Random(1234)  # noqa: S311 - test fixture, not security
    image = Image.new("RGB", size)
    image.putdata([
        (rng.randrange(256), rng.randrange(256), rng.randrange(256))
        for _ in range(size[0] * size[1])
    ])
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def a_coloured_image(colour: tuple[int, int, int], size: tuple[int, int] = (64, 48)) -> bytes:
    """A flat image of a known colour, so a Thumbnail can be traced to its Photo."""
    from io import BytesIO

    from PIL import Image

    buffer = BytesIO()
    Image.new("RGB", size, colour).save(buffer, format="PNG")
    return buffer.getvalue()


def dominant_colour(content: bytes) -> tuple[int, int, int]:
    from io import BytesIO

    from PIL import Image

    with Image.open(BytesIO(content)) as image:
        return image.convert("RGB").resize((1, 1)).getpixel((0, 0))


# --- driving the Upload popup in a browser ----------------------------------


def upload_files(page, paths) -> None:
    """Choose files in the Upload popup and make the Upload.

    REQ-GAL-001@v3 separated the two: choosing files no longer uploads them,
    because criterion 15 requires the popup to show a preview of what was
    chosen *before* the Upload is made. Every belt B test goes through here so
    that the flow is written down once.

    Opens the popup only when it is not already open: some callers open it
    themselves first in order to assert something about it, and clicking the
    opener again while the dialog is modal hits the backdrop instead.
    """
    if not page.get_by_test_id("upload-popup").is_visible():
        page.get_by_test_id("upload-open").click()
    page.get_by_test_id("upload-input").set_input_files(paths)
    page.get_by_test_id("upload-submit").click()
