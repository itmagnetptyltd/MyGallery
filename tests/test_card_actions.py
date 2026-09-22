"""Belt A — REQ-GAL-003@v4: Download and Delete on every Thumbnail card."""

import re


def _css(project_root) -> str:
    return (project_root / "src/mygallery/static/app.css").read_text(encoding="utf-8")


def _js(project_root) -> str:
    return (project_root / "src/mygallery/static/app.js").read_text(encoding="utf-8")


def _function(script: str, name: str) -> str:
    match = re.search(rf"function {name}\(photo\) \{{.*?\n\}}", script, re.DOTALL)
    assert match is not None, f"app.js has no {name}(photo) function"
    return match.group(0)


# @covers REQ-GAL-003@v4
# @covers REQ-GAL-012@v3
def test_a_thumbnail_card_is_built_with_download_and_delete_controls(project_root):
    script = _js(project_root)

    actions = _function(script, "cardActionsFor")
    assert '"card-download"' in actions
    assert '"card-delete"' in actions
    assert "cardActionsFor(photo)" in _function(script, "tileFor")


# @covers REQ-GAL-003@v4
# @covers REQ-GAL-012@v3
def test_the_card_controls_share_the_row_in_equal_columns(project_root):
    match = re.search(r"\.card-actions\s*\{([^}]*)\}", _css(project_root))

    assert match is not None, "app.css has no .card-actions rule"
    assert re.search(r"grid-template-columns:\s*1fr\s+1fr", match.group(1))
