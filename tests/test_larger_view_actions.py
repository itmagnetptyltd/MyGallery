"""Belt A — REQ-GAL-004@v3: the Larger view's actions are Save description and Close."""

import re


def _actions_row(page: str) -> str:
    match = re.search(r'<div class="larger-view-actions">(.*?)</div>', page, re.DOTALL)
    assert match is not None, "the page has no .larger-view-actions row"
    return match.group(1)


# @covers REQ-GAL-004@v3
# @covers REQ-GAL-014@v2
def test_the_larger_view_actions_are_save_description_and_close(client):
    page = client.get("/").get_data(as_text=True)

    row = _actions_row(page)
    assert re.findall(r'data-testid="([^"]+)"', row) == [
        "description-save",
        "larger-view-close-button",
    ]
    assert 'data-testid="download-photo"' not in page
    assert 'data-testid="delete-photo"' not in page
