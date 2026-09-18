"""Belt A — UAT visual: cards, upload popup, in-panel Larger view controls."""

import re


def _css(project_root) -> str:
    return (project_root / "src/mygallery/static/app.css").read_text(encoding="utf-8")


def _js(project_root) -> str:
    return (project_root / "src/mygallery/static/app.js").read_text(encoding="utf-8")


def _grid_min_px(css: str) -> int:
    match = re.search(
        r"\.gallery\s*\{[^}]*grid-template-columns:\s*repeat\([^,]+,\s*minmax\((\d+)px",
        css,
        re.DOTALL,
    )
    assert match is not None, "the Gallery grid names no minmax track size"
    return int(match.group(1))


# @covers REQ-GAL-012@v1
# @covers REQ-GAL-003@v2
def test_gallery_css_sets_card_min_width_above_160px(project_root):
    assert _grid_min_px(_css(project_root)) > 160


# @covers REQ-GAL-012@v1
# @covers REQ-GAL-003@v2
def test_gallery_html_has_a_card_surface_around_each_thumbnail(project_root):
    script = _js(project_root)

    assert "thumbnail-card" in script
    assert 'dataset.testid = "thumbnail"' in script


# @covers REQ-GAL-013@v1
# @covers REQ-GAL-001@v2
def test_gallery_html_includes_an_upload_popup(client):
    page = client.get("/").get_data(as_text=True)

    assert 'data-testid="upload-popup"' in page
    assert 'data-testid="upload-input"' in page
    popup_at = page.index('data-testid="upload-popup"')
    input_at = page.index('data-testid="upload-input"')
    assert input_at > popup_at


# @covers REQ-GAL-013@v1
# @covers REQ-GAL-007@v2
def test_empty_gallery_html_includes_a_control_that_opens_the_upload_popup(client):
    page = client.get("/").get_data(as_text=True)

    assert 'data-testid="upload-open"' in page


# @covers REQ-GAL-014@v1
# @covers REQ-GAL-004@v2
def test_larger_view_markup_places_close_inside_the_panel(project_root, client):
    page = client.get("/").get_data(as_text=True)
    css = _css(project_root)

    assert 'data-testid="larger-view-close"' in page
    assert not re.search(
        r"\.larger-view-close\s*\{[^}]*top:\s*-\d+px",
        css,
        re.DOTALL,
    )


# @covers REQ-GAL-014@v1
# @covers REQ-GAL-004@v2
def test_larger_view_markup_places_delete_inside_the_panel(project_root, client):
    page = client.get("/").get_data(as_text=True)
    css = _css(project_root)

    assert 'data-testid="delete-photo"' in page
    assert not re.search(
        r"\.larger-view-actions\s*\{[^}]*bottom:\s*-\d+px",
        css,
        re.DOTALL,
    )
