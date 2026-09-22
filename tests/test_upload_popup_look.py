"""Belt A — the Upload popup's size, border and controls (REQ-GAL-013@v3).

FB-0005 asked for a larger Upload popup whose border and controls look like
the Larger view's. These read the stylesheet and the rendered page; the browser
belt checks what those rules compute to.
"""

import re


def _css(project_root) -> str:
    return (project_root / "src/mygallery/static/app.css").read_text(encoding="utf-8")


def _rule(css: str, selector: str) -> str:
    """The declarations of the rule whose selector is exactly `selector`."""
    match = re.search(rf"(?m)^{re.escape(selector)}\s*\{{([^}}]*)\}}", css)
    assert match is not None, f"no rule for {selector}"
    return match.group(1)


def _declaration(block: str, name: str) -> str:
    match = re.search(rf"(?m)^\s*{re.escape(name)}\s*:\s*([^;]+);", block)
    assert match is not None, f"no {name} declared"
    return match.group(1).strip()


def _class_of(page: str, marker: str) -> str:
    """The class attribute of the element whose opening tag carries `marker`."""
    match = re.search(rf"<[a-z]+\b[^>]*{re.escape(marker)}[^>]*>", page)
    assert match is not None, f"no element carrying {marker}"
    classes = re.search(r'class="([^"]*)"', match.group(0))
    assert classes is not None, f"the element carrying {marker} has no class"
    return classes.group(1)


# @covers REQ-GAL-013@v3
def test_the_upload_popup_is_wider_than_the_delivered_680_pixels(project_root):
    popup = _rule(_css(project_root), ".upload-popup")

    max_width = _declaration(popup, "max-width")

    assert re.fullmatch(r"\d+px", max_width), f"max-width is not in pixels: {max_width}"
    assert int(max_width.removesuffix("px")) > 680


# @covers REQ-GAL-013@v3
# @covers REQ-GAL-019@v2
def test_the_upload_popup_and_larger_view_share_one_close_control_rule(project_root):
    css = re.sub(r"/\*.*?\*/", "", _css(project_root), flags=re.DOTALL)

    rules_naming_both = [
        body
        for selector, body in re.findall(r"([^{}]+)\{([^}]*)\}", css)
        if re.search(r"\.upload-popup-close\b(?!:)", selector)
        and re.search(r"\.larger-view-close\b(?!:)", selector)
    ]
    assert rules_naming_both, "no single rule styles both close controls"
    body = rules_naming_both[0]
    for name in ("width", "height", "border", "background", "color"):
        _declaration(body, name)


# @covers REQ-GAL-013@v3
def test_the_upload_popup_border_matches_the_larger_view_panels(project_root):
    css = _css(project_root)

    popup_border = _declaration(_rule(css, ".upload-popup"), "border")
    panel_border = _declaration(_rule(css, ".larger-view"), "border")

    assert popup_border == panel_border


# @covers REQ-GAL-013@v3
def test_choose_files_and_upload_use_the_save_description_button_look(client):
    page = client.get("/").get_data(as_text=True)

    choose = re.search(r'<span class="([^"]*)">\s*Choose files\s*</span>', page)
    upload = _class_of(page, 'data-testid="upload-submit"')
    save = _class_of(page, 'data-testid="description-save"')

    assert choose is not None, "Choose files is not a classed span"
    assert "outline-button" in save.split()
    assert "outline-button" in upload.split()
    assert "outline-button" in choose.group(1).split()
