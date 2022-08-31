from typing import List

from flask import render_template

from logic.interfaces.i_home_routes import IHomeRoute
from models import NoteModel, PersonModel


class HomeLogic(IHomeRoute):

    @classmethod
    def render_home_page(cls, data: dict) -> str:
        common_data = cls._prepare_common_data(data)
        return cls._render_page_html(**common_data)

    @classmethod
    def render_home_page_filtered(cls, data: dict) -> str:
        # TODO REFACTOR: organize code
        common_data = cls._prepare_common_data(data)
        search = data["search"]
        search_words = search.lower().split(" ")
        notes_searching = set(common_data.get("notes"))
        notes_filtered = set()
        for word in search_words:
            notes_to_remove_from_search = set()
            for note in notes_searching:
                if any(
                        word in note_word.lower() for note_word in
                        note.get_subjects_and_categories_words()
                ) \
                        or word in note.title.lower() \
                        or word in note.content.lower():
                    notes_filtered.add(note)
                    notes_to_remove_from_search.add(note)
            notes_searching -= notes_to_remove_from_search
        common_data["notes"] = list(notes_filtered)
        return cls._render_page_html(search=search, **common_data)

    @classmethod
    def _render_page_html(
            cls,
            notes: List[NoteModel],
            persons: List[PersonModel],
            search: str = "",
            csrf_token: str = None,
            admin: str = None,
    ):
        return render_template(
            "index.html",
            notes=notes,
            persons=persons,
            search=search,
            csrf_token=csrf_token,
            admin=admin,
        )

    @classmethod
    def _prepare_common_data(cls, data: dict) -> dict:
        if data.get("jwt_admin"):
            visibility_selection = data.get("visibility_selection")
        else:
            visibility_selection = data.get("scope")
        return {
            "notes": NoteModel.get_all_visible(visibility_selection),
            "persons": PersonModel.get_all(),
            "csrf_token": data.get("jwt_csrf"),
            "admin": data.get("jwt_admin")
        }
