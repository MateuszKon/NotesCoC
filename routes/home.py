from flask import render_template, redirect, url_for, request
from flask_jwt_extended import get_jwt

from libs.jwt_functions import jwt_required_with_redirect
from models.notes import NoteModel
from models.persons import PersonModel


class HomeRoutes:

    @classmethod
    def index(cls):
        return redirect(url_for("home"))

    @classmethod
    @jwt_required_with_redirect()
    def home(cls):
        jwt_data = get_jwt()
        visibility_selection = request.cookies.get("visibility_selection")
        notes = NoteModel.get_all_visible(visibility_selection)
        persons = PersonModel.get_all()
        search = ""
        if request.method == "POST":
            search = request.form["search"]
            search_words = search.split(" ")
            notes_searching = set(notes)
            notes_filtered = set()
            for word in search_words:
                notes_to_remove_from_search = set()
                for note in notes_searching:
                    if word in note.title or word in note.content:
                        notes_filtered.add(note)
                        notes_to_remove_from_search.add(note)
                notes_searching -= notes_to_remove_from_search
            notes = list(notes_filtered)

        return render_template(
            "index.html",
            notes=notes,
            persons=persons,
            search=search,
            csrf_token=jwt_data.get("csrf"),
            admin=jwt_data.get("admin"),
        )
