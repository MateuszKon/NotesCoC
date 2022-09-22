from typing import List, Set

from models import NoteModel
from routes.home import IHomeRouteLogic
from routes.i_request import ResponseData, ContextData, RequestData
from schemas.notes import note_schema, note_schema_without_visibility


class HomeLogic(IHomeRouteLogic):

    @classmethod
    def render_home_page(
            cls,
            data: RequestData
    ) -> ResponseData:
        common_data = {
            "notes": NoteModel.get_all_visible(data.context.person_visibility),
        }
        return cls._home_page_data(context_data=data.context, **common_data)

    @classmethod
    def render_home_page_filtered(
            cls,
            data: RequestData,
    ) -> ResponseData:
        filter_category = data.data.get('category')
        filter_subject = data.data.get('subject')
        filter_title_content = data.data.get("search")

        notes_for_searching = set(
            NoteModel.get_all_visible(data.context.person_visibility)
        )

        search_words = cls._prepare_words_for_search(filter_title_content)
        notes_filtered = cls._filter_notes_with_words(
            notes_for_searching,
            search_words,
        )

        return cls._home_page_data(
            context_data=data.context,
            search=filter_title_content,
            notes=list(notes_filtered),
        )

    @staticmethod
    def _home_page_data(
            context_data: ContextData,
            notes: List[NoteModel],
            search: str = "",
    ):
        schema = note_schema if context_data.get('jwt_admin') else \
            note_schema_without_visibility
        resource = schema.dump(notes, many=True)
        return ResponseData(
            template="index.html",
            resource=resource,
            search=search,
        )

    @staticmethod
    def _prepare_words_for_search(search_text: str) -> List[str]:
        return search_text.lower().split(" ")

    @staticmethod
    def _filter_notes_with_words(
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
