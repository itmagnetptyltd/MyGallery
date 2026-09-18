"""The application factory."""

from flask import Flask

from mygallery import config
from mygallery.web.api import api
from mygallery.web.pages import pages

SECURITY_HEADERS = {
    "Content-Security-Policy": "default-src 'self'",
    "X-Content-Type-Options": "nosniff",
}


def create_app() -> Flask:
    app = Flask(__name__)

    # REQ-GAL-001 allows a batch of Photos in one Upload, so this is the
    # ceiling for the whole request, not the 25 MB per-Photo limit — which
    # validation.py enforces. Setting it to the per-Photo limit would refuse
    # a legitimate batch of thirty.
    app.config["MAX_CONTENT_LENGTH"] = config.MAX_REQUEST_BYTES

    app.register_blueprint(pages)
    app.register_blueprint(api)

    @app.after_request
    def add_security_headers(response):
        for header, value in SECURITY_HEADERS.items():
            response.headers[header] = value
        return response

    return app
