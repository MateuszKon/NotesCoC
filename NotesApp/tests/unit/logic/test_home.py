from unittest.mock import patch, MagicMock

from NotesApp.logic.home import HomeLogic
from NotesApp.routes.i_request import RequestPayload, ContextData, RequestData
from NotesApp.tests.unit.base_unit_database_test import BaseTestUnitDatabase


class TestHomeLogic(BaseTestUnitDatabase):

    @patch("database.models.notes.NoteModel.get_all_visible")
    def test_get_all_visible_called(self, mock: MagicMock):
        person = 'person_logged'
        data = RequestData(
            RequestPayload(
                {}
            ),
            ContextData(
                {"jwt_scope": person}
            )
        )
        HomeLogic.render_home_page_filtered(data)
        mock.assert_called_once_with(person)
