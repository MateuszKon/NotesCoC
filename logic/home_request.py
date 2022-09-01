from typing import List, Set

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
        common_data = cls._prepare_common_data(data)

        search_string = data["search"]
        search_words = cls._prepare_words_for_search(search_string)
        notes_for_searching = set(common_data.pop("notes"))

        notes_filtered = cls._filter_notes_with_words(
            notes_for_searching,
            search_words,
        )

        return cls._render_page_html(
            search=search_string,
            notes=list(notes_filtered),
            **common_data
        )

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

    @classmethod
    def _prepare_words_for_search(cls, search_text: str) -> List[str]:
        return search_text.lower().split(" ")

    @classmethod
    def _filter_notes_with_words(
            cls,
            notes: Set[NoteModel],
            words: List[str]
    ) -> Set[NoteModel]:
        notes_filtered = set()
        for word in words:
            notes_to_remove_from_search = set()
            for note in notes:
                if any(
                        word in note_word.lower() for note_word in
                        note.get_subjects_and_categories_words()
                ) \
                        or word in note.title.lower() \
                        or word in note.content.lower():
                    notes_filtered.add(note)
                    notes_to_remove_from_search.add(note)
            notes = notes - notes_to_remove_from_search
        return notes_filtered
