"""The Gallery page itself."""


# @covers REQ-GAL-011@v1
def test_requesting_the_root_path_serves_the_gallery_page(client):
    response = client.get("/")

    assert response.status_code == 200


# @covers REQ-GAL-011@v1
def test_the_gallery_page_presents_the_gallery_region(client):
    response = client.get("/")

    assert b'data-testid="gallery"' in response.data


def test_the_gallery_page_is_served_as_html(client):
    response = client.get("/")

    assert response.headers["Content-Type"].startswith("text/html")


# Hardening. No slice 1 requirement names these; rules/javascript/security.md
# makes both blocking review findings, and the substance applies here too.
def test_the_gallery_page_is_served_with_a_content_security_policy(client):
    response = client.get("/")

    assert response.headers["Content-Security-Policy"] == "default-src 'self'"


def test_the_gallery_page_is_served_with_nosniff(client):
    response = client.get("/")

    assert response.headers["X-Content-Type-Options"] == "nosniff"
