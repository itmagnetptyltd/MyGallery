"""The application factory."""

from flask import Flask

from mygallery.web.pages import pages

SECURITY_HEADERS = {
    "Content-Security-Policy": "default-src 'self'",
    "X-Content-Type-Options": "nosniff",
}


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(pages)

    @app.after_request
    def add_security_headers(response):
        for header, value in SECURITY_HEADERS.items():
            response.headers[header] = value
        return response

    return app
