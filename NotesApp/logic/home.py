from typing import List

from database.models import NoteModel
from NotesApp.routes.home import IHomeRouteLogic
from NotesApp.routes.i_request import ResponseData, ContextData, RequestData
from NotesApp.schemas.notes import note_schema, note_schema_without_visibility


class HomeLogic(IHomeRouteLogic):

    @classmethod
    def render_home_page_filtered(
            cls,
            data: RequestData,
    ) -> ResponseData:
        filter_category = data.data.get('category')
        filter_subject = data.data.get('subject')
        filter_title_content = data.data.get("search")

        notes_qs = NoteModel.get_all_visible(data.context.person_visibility)

        if filter_category is not None:
            notes_qs = NoteModel.category_filtering_qs(
                notes_qs,
                filter_category
            )

        if filter_subject is not None:
            notes_qs = NoteModel.subject_filtering_qs(
                notes_qs,
                filter_subject
            )

        if filter_title_content is not None:
            search_words = cls._prepare_words_for_search(filter_title_content)
            notes_qs = NoteModel.words_filtering_qs(notes_qs, search_words)

        notes_filtered = notes_qs.all()

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
