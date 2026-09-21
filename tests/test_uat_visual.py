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


# @covers REQ-GAL-012@v2
# @covers REQ-GAL-003@v3
def test_gallery_css_sets_card_min_width_above_160px(project_root):
    assert _grid_min_px(_css(project_root)) > 160


# @covers REQ-GAL-012@v2
# @covers REQ-GAL-003@v3
def test_gallery_html_has_a_card_surface_around_each_thumbnail(project_root):
    script = _js(project_root)

    assert "thumbnail-card" in script
    assert 'dataset.testid = "thumbnail"' in script


# @covers REQ-GAL-013@v3
# @covers REQ-GAL-001@v3
def test_gallery_html_includes_an_upload_popup(client):
    page = client.get("/").get_data(as_text=True)

    assert 'data-testid="upload-popup"' in page
    assert 'data-testid="upload-input"' in page
    popup_at = page.index('data-testid="upload-popup"')
    input_at = page.index('data-testid="upload-input"')
    assert input_at > popup_at


# @covers REQ-GAL-013@v3
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


# --- REQ-GAL-012@v2 / REQ-GAL-013@v2, from CHG-0005, CHG-0008 and CHG-0009 ---


# @covers REQ-GAL-012@v2
# @covers REQ-GAL-018@v1
def test_a_thumbnails_alt_text_is_its_photos_description(project_root):
    """The client chose alt over a tooltip when asked, on 2026-09-21."""
    script = _js(project_root)

    assert "tile.alt = photo.description || photo.filename" in script


# @covers REQ-GAL-013@v3
# @covers REQ-GAL-019@v2
def test_the_upload_popup_has_a_close_control(client):
    page = client.get("/").get_data(as_text=True)

    assert 'data-testid="upload-popup-close"' in page


# @covers REQ-GAL-013@v3
# @covers REQ-GAL-019@v2
def test_the_upload_popup_close_control_is_inside_the_popup(client):
    page = client.get("/").get_data(as_text=True)

    popup_at = page.index('data-testid="upload-popup"')
    close_at = page.index('data-testid="upload-popup-close"')
    end_at = page.index("</dialog>", popup_at)
    assert popup_at < close_at < end_at


# @covers REQ-GAL-013@v3
# @covers REQ-GAL-019@v2
def test_the_upload_popup_close_control_is_placed_at_the_top_right(project_root):
    css = _css(project_root)

    match = re.search(r"\.upload-popup-close\s*\{([^}]*)\}", css, re.DOTALL)
    assert match is not None, "the popup close control has no rule of its own"
    rule = match.group(1)
    assert "position: absolute" in rule
    assert "top:" in rule
    assert "right:" in rule


# @covers REQ-GAL-013@v3
# @covers REQ-GAL-019@v2
def test_the_upload_popup_close_control_closes_the_popup(project_root):
    script = _js(project_root)

    assert "uploadPopupClose" in script
    assert "uploadPopup.close()" in script


# @covers REQ-GAL-013@v3
# @covers REQ-GAL-015@v2
def test_the_upload_popup_shows_a_preview_of_each_chosen_file(project_root):
    script = _js(project_root)

    assert 'dataset.testid = "upload-preview"' in script
    assert "createObjectURL" in script


# --- REQ-GAL-016@v1 / REQ-GAL-019@v1 — slice 8 ------------------------------


# @covers REQ-GAL-016@v1
def test_the_upload_popup_accepts_dropped_files(project_root):
    script = _js(project_root)

    assert 'uploadPopup.addEventListener("drop"' in script
    assert "dataTransfer" in script


# @covers REQ-GAL-016@v1
def test_dropping_on_the_upload_popup_is_not_the_only_way_to_choose(client):
    """REQ-GAL-001@v3 still requires files to be chosen from the popup.

    The client said "in upload or drag-drop": dropping is an addition, so the
    picker has to survive it.
    """
    page = client.get("/").get_data(as_text=True)

    assert 'data-testid="upload-input"' in page


# @covers REQ-GAL-019@v2
def test_closing_the_upload_popup_leaves_it_reusable(project_root):
    """Closing has to be close(), not remove() or hidden.

    REQ-GAL-019 c3 requires the popup to open again afterwards, and only a
    dialog that is still in the document can be shown by showModal().
    """
    script = _js(project_root)

    assert "uploadPopup.close()" in script
    assert "uploadPopup.remove()" not in script


# --- REQ-GAL-017@v1 — the description character count. Slice 9. -------------


# @covers REQ-GAL-017@v1
def test_the_upload_popup_shows_a_character_count_for_the_description(client):
    page = client.get("/").get_data(as_text=True)

    assert 'data-testid="description-count"' in page


# @covers REQ-GAL-017@v1
def test_the_character_count_reads_its_limit_from_the_field(project_root):
    """One source for 250, and it is the markup that enforces it.

    A count that says /250 while maxlength stops the field somewhere else is
    worse than no count, so the script must not carry its own copy.
    """
    script = _js(project_root)

    assert "maxLength" in script
    assert "/250" not in script
