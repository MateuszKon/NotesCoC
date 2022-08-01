from flask import render_template, redirect, url_for

from models.notes import NoteModel


class HomeRoutes:

    @classmethod
    def index(cls):
        return redirect(url_for("home"))

    @classmethod
    def home(cls):
        return render_template(
            "index.html",
            notes=NoteModel.query.all(),
        )
