"""Belt B — criterion 1, and the closest mechanical proxy for criterion 2.

This test performs only what the start instructions document: it starts the
application and opens the address the README names. If reaching a displayed
Gallery needed a step that is not written down, this test would not pass.

That is a proxy, not proof. The real check for criterion 2 is following
README.md on a clean Windows 11 machine.
"""

import pytest
from playwright.sync_api import expect


@pytest.fixture
def gallery_url(running_server) -> str:
    return f"http://{running_server.host}:{running_server.port}"


# @covers REQ-GAL-011@v1
def test_following_the_documented_start_steps_displays_the_gallery(page, gallery_url):
    page.goto(gallery_url)

    expect(page.get_by_test_id("gallery")).to_be_visible()


# @covers REQ-GAL-011@v1
def test_the_gallery_page_is_titled_for_the_application(page, gallery_url):
    page.goto(gallery_url)

    expect(page).to_have_title("MyGallery")
