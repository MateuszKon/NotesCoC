from unittest.mock import MagicMock

from werkzeug.exceptions import NotFound

from NotesApp.config_routes import configure_subject_routes
from NotesApp.routes.i_request import RequestData, RequestPayload, ContextData
from NotesApp.tests.integration.base_integration_test import BaseIntegrationTest


class TestSubjectResourceResponseDataPreparation(BaseIntegrationTest):
    # TODO: test cases
    """
    test for viewing single subject by user (check ResponseData.resource)
    test for viewing single subject by user (404 when person do not see notes)
    test for viewing all subjects by user (only visible subjects and only visible notes)
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        app_mock = MagicMock()
        config_mock = MagicMock()
        debug_dict = {"DEBUG": False}
        config_mock.__getitem__.side_effect = debug_dict.__getitem__
        app_mock.config = config_mock
        cls.routes = configure_subject_routes(app_mock)

    def test_viewing_subject_by_user(self):
        with self.app_context():
            data = RequestData(
                RequestPayload(
                    {}
                ),
                ContextData(
                    {"jwt_scope": self.person_logged.name}
                )
            )
            for sub_i, subject in enumerate(self.subjects_visible):
                with self.subTest(subject=subject.name):
                    subj_name = subject.name
                    identifier = self.routes.identifier.new_value(subj_name)
                    obj = self.routes.logic.get_by_identifier(identifier).read(data)
                    resource = self.routes.create_resource_dict(data, obj)

                    user_subject_keys = ['name', 'notes']
                    self.assertEqual(
                        len(resource),
                        len(user_subject_keys),
                        "Number of keys of resource dictionary is incorrect!"
                    )
                    for i, key in enumerate(user_subject_keys):
                        with self.subTest(i=i):
                            self.assertIn(
                                key,
                                resource,
                                "Resource does not contain key!"
                            )
                    for i, note in enumerate(resource['notes']):
                        with self.subTest(j=i):
                            self.assertIn(
                                note['title'],
                                self.visible_titles
                            )
                    self.assertEqual(
                        len(resource['notes']),
                        5-sub_i,
                        "Number of visible notes are incorrect"
                    )
                    user_note_keys = ['title', 'id']
                    for i, key in enumerate(user_note_keys):
                        with self.subTest(note_key=i):
                            self.assertIn(
                                key,
                                resource['notes'][0],
                                "Resource does not contain key!"
                            )

    def test_not_visible_subject_for_user_404(self):
        with self.app_context():
            data = RequestData(
                RequestPayload(
                    {}
                ),
                ContextData(
                    {"jwt_scope": self.person_logged.name}
                )
            )
            for subject in self.subjects_invisible:
                with self.subTest(subject=subject.name):
                    with self.assertRaises(NotFound):
                        identifier = self.routes.identifier.new_value(subject.name)
                        obj = self.routes.logic.get_by_identifier(identifier).read(data)

    def test_displaying_all_subjects_for_user(self):
        with self.app_context():
            data = RequestData(
                RequestPayload(
                    {}
                ),
                ContextData(
                    {"jwt_scope": self.person_logged.name}
                )
            )
            objs = self.routes.logic.list(data)
            resource = self.routes.create_resource_dict(data, objs)

            self.assertEqual(
                len(resource['list']),
                len(self.subjects_visible),
                "Number of visible subjects is incorrect!"
            )
            for i, subject in enumerate(resource['list']):
                with self.subTest(subject=i):
                    self.assertIn(
                        subject['name'],
                        self.visible_subjects_names,
                        "Showed subject is not in visible subject!"
                    )
                    for j, note in enumerate(subject['notes']):
                        with self.subTest(note=j):
                            self.assertIn(
                                note['title'],
                                self.visible_titles,
                                "Showed note is not visible note!"
                            )
            user_note_keys = ['id', 'title']
            for key in resource['list'][0]['notes'][0]:
                with self.subTest(note_key=i):
                    self.assertIn(
                        key,
                        user_note_keys,
                        "Subject has not valid key!"
                    )
