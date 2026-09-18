"""Starting the application — the part `python -m mygallery` performs.

This lives outside __main__.py so it can be tested. The entry point is a shim
over it and nothing else.
"""


class FakeApp:
    """Records how the application was told to listen."""

    def __init__(self) -> None:
        self.host: str | None = None
        self.port: int | None = None

    def run(self, host: str, port: int) -> None:
        self.host, self.port = host, port


# @covers REQ-GAL-011@v1
def test_the_application_is_launched_at_the_address_the_instructions_name(documented_port):
    from mygallery import launcher

    assert launcher.address() == f"http://127.0.0.1:{documented_port}"


# @covers REQ-GAL-011@v1
def test_starting_the_application_binds_it_to_loopback():
    from mygallery import launcher

    app = FakeApp()
    launcher.start(app_factory=lambda: app, open_browser=lambda url: None, announce=lambda m: None)

    assert app.host == "127.0.0.1"


# @covers REQ-GAL-011@v1
def test_starting_the_application_listens_on_the_documented_port(documented_port):
    from mygallery import launcher

    app = FakeApp()
    launcher.start(app_factory=lambda: app, open_browser=lambda url: None, announce=lambda m: None)

    assert app.port == documented_port


# @covers REQ-GAL-011@v1
def test_starting_the_application_opens_the_browser_at_the_gallery():
    from mygallery import launcher

    opened: list[str] = []
    launcher.start(app_factory=FakeApp, open_browser=opened.append, announce=lambda m: None)

    assert opened == [launcher.address()]
