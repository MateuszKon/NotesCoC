from unittest.mock import patch

from werkzeug.exceptions import NotFound

from logic.notes import NoteLogic
from routes.i_request import RequestData, RequestPayload, ContextData
from tests.integration.base_integration_test import BaseIntegrationTest


class TestNotePageResponseDataPreparation(BaseIntegrationTest):
    """
    test for viewing note by user
    test for viewing (editing) note by admin
    test for viewing note not visible for user (404)

    ResponseData.resource should has only fields available for type of user
    (normal user do not see every field)
    """

    @patch("logic.notes.url_for")
    def test_note_resource_fields_displayed_for_user(self, mock):
        with self.app_context():
            data = RequestData(
                RequestPayload(
                    {}
                ),
                ContextData(
                    {"jwt_scope": self.person_logged.name}
                )
            )
            response = NoteLogic.render_edit_note(data, self.notes_visible[0].id)

            note = response.resource['note']
            user_note_keys = ['real_update_date', 'title', 'real_creation_date', 'content', 'id',
                              'game_creation_date', 'subjects', 'game_update_date', ]
            self.assertEqual(
                len(note),
                len(user_note_keys),
                "Number of keys of note dictionary is incorrect!"
            )
            for i, key in enumerate(user_note_keys):
                with self.subTest(i=i):
                    self.assertIn(
                        key,
                        note,
                        "Note does not contain key!"
                    )
            subject = note['subjects'][0]
            self.assertEqual(
                len(subject),
                1,
                "Number of keys of subject dictionary in note dictionary is incorrect!"
            )
            self.assertIn(
                'name',
                subject,
                "Subject dictionary in note dictionary does not contain key!"
            )
            self.assertIsNone(
                response.resource.get("all_subjects"),
                "All subjects should not be displayed for user!"
            )
            self.assertEqual(
                len(response.resource),
                1,
                "Some resource is displayed for user other that note!"
            )

    @patch("logic.notes.url_for")
    def test_note_resource_fields_displayed_for_admin(self, mock):
        with self.app_context():
            data = RequestData(
                RequestPayload(
                    {}
                ),
                ContextData(
                    {"jwt_admin": True}
                )
            )
            response = NoteLogic.render_edit_note(data, self.notes_visible[0].id)

            note = response.resource['note']
            user_note_keys = ['real_update_date', 'title', 'real_creation_date', 'content', 'id',
                              'game_creation_date', 'subjects', 'game_update_date',
                              'persons_visibility']
            self.assertEqual(
                len(note),
                len(user_note_keys),
                "Number of keys of note dictionary is incorrect!"
            )
            for i, key in enumerate(user_note_keys):
                with self.subTest(i=i):
                    self.assertIn(
                        key,
                        note,
                        "Note does not contain key!"
                    )
            subject = note['subjects'][0]
            self.assertEqual(
                len(subject),
                1,
                "Number of keys of subject dictionary in note dictionary is incorrect!"
            )
            self.assertIn(
                'name',
                subject,
                "Subject dictionary in note dictionary does not contain key!"
            )
            self.assertIsNotNone(
                response.resource.get("all_subjects"),
                "All subjects should be displayed for admin!"
            )

    @patch("logic.notes.url_for")
    def test_not_visible_note_for_user_404(self, mock):
        with self.app_context():
            data = RequestData(
                RequestPayload(
                    {}
                ),
                ContextData(
                    {"jwt_scope": self.person_logged.name}
                )
            )
            with self.assertRaises(NotFound):
                NoteLogic.render_edit_note(data, self.notes_invisible[0].id)

