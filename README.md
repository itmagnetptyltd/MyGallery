# MyGallery

A private photo gallery that runs on your own PC. Your photos stay on your
machine — MyGallery is not reachable from any other device.

## Before you start

- **Python 3.12 or later** — download it from [python.org](https://www.python.org/downloads/windows/), and tick *"Add python.exe to PATH"* in the installer.

That is the only thing you need to install. MyGallery sets up everything else
for itself the first time it runs.

## Run MyGallery

- Double-click `scripts/start.cmd`. Your web browser opens at http://127.0.0.1:8765 with your Gallery.

The first run takes a minute while MyGallery prepares itself. Every run after
that is immediate.

Leave the black window open while you are using MyGallery — closing it stops
the application. To stop it deliberately, close that window or press `Ctrl+C`
in it.

## If something goes wrong

**"Python was not found"** — Python is not installed, or was installed without
*"Add python.exe to PATH"*. Re-run the Python installer and tick that box.

**"Address already in use"** — MyGallery is already running. Look for the black
window, or open http://127.0.0.1:8765 in your browser.

**The browser did not open** — MyGallery may still be running. Type
http://127.0.0.1:8765 into your browser yourself.

## Your photos are yours

MyGallery listens only on your own machine. Another computer, phone or tablet
on your network cannot reach it, and nothing is sent anywhere over the
internet.

---

## Working on MyGallery

Everything below is for developing MyGallery, **not** for running it. Nothing
here is needed to use the application.

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -e ".[dev]"
.venv/Scripts/python.exe -m playwright install chromium
```

| Task | Command |
|---|---|
| Unit tests (belt A) | `.venv/Scripts/python.exe -m pytest tests/ --ignore=tests/e2e -q` |
| Browser tests (belt B) | `/run-Browsertest`, or double-click `scripts/run-Browsertest.cmd` |
| Coverage (80% floor) | `.venv/Scripts/python.exe -m pytest --cov --cov-fail-under=80 -q` |
| Lint | `.venv/Scripts/python.exe -m ruff check .` |

The requirements this application is built against are in `.brain/`. Start at
`.brain/index.md`.
