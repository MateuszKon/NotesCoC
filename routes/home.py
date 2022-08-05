from flask import render_template, redirect, url_for, request

from models.notes import NoteModel
from models.persons import PersonModel


class HomeRoutes:

    @classmethod
    def index(cls):
        return redirect(url_for("home"))

    @classmethod
    def home(cls):
        visibility_selection = request.cookies.get("visibility_selection")
        return render_template(
            "index.html",
            notes=NoteModel.get_all_visible(visibility_selection),
            persons=PersonModel.get_all(),
        )
