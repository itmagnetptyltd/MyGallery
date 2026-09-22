"""Belt A — the size of a chosen file's preview (REQ-GAL-015@v2).

The client asked for previews "width like description box and height as per
image pixel", centred when narrower. These read the stylesheet; the browser
belt measures what it renders.
"""

import re


def _rule(project_root, selector: str) -> str:
    css = (project_root / "src/mygallery/static/app.css").read_text(encoding="utf-8")
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    match = re.search(rf"(?m)^{re.escape(selector)}\s*\{{([^}}]*)\}}", css)
    assert match is not None, f"no rule for {selector}"
    return match.group(1)


def _declarations(block: str) -> dict[str, str]:
    return {
        name.strip(): value.strip()
        for name, value in re.findall(r"([a-z-]+)\s*:\s*([^;]+);", block)
    }


# @covers REQ-GAL-015@v2
def test_previews_are_laid_out_one_to_a_row(project_root):
    previews = _declarations(_rule(project_root, ".upload-previews"))

    assert previews.get("grid-template-columns") == "1fr"


# @covers REQ-GAL-015@v2
def test_a_preview_is_capped_at_the_column_width_and_keeps_its_height_in_proportion(
    project_root,
):
    image = _declarations(_rule(project_root, ".upload-preview-image"))

    assert image.get("max-width") == "100%"
    assert image.get("height") == "auto"


# @covers REQ-GAL-015@v2
def test_the_preview_list_hides_its_scrollbar_so_previews_keep_the_fields_width(
    project_root,
):
    """A visible scrollbar in the list's own scroll box would take ~15px from
    every preview. The browser belt cannot see this: Playwright runs headless
    Chromium with --hide-scrollbars, so it is pinned here instead."""
    previews = _declarations(_rule(project_root, ".upload-previews"))

    assert previews.get("overflow-y") == "auto"
    assert previews.get("scrollbar-width") == "none"


# @covers REQ-GAL-015@v2
def test_a_preview_is_never_cropped(project_root):
    image = _declarations(_rule(project_root, ".upload-preview-image"))

    assert image.get("object-fit", "fill") != "cover"


# @covers REQ-GAL-015@v2
def test_a_narrow_preview_is_centred(project_root):
    image = _declarations(_rule(project_root, ".upload-preview-image"))

    assert image.get("margin-inline") == "auto"
