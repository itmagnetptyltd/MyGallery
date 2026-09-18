"""The pages a browser asks for."""

from flask import Blueprint, render_template

pages = Blueprint("pages", __name__)


@pages.get("/")
def gallery():
    """The Gallery.

    Slice 1 renders the shell. What it says when it holds no Photos is
    REQ-GAL-007, which is slice 2 — deliberately not built here.
    """
    return render_template("gallery.html")
