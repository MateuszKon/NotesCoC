from logic.home import HomeLogic
from routes.i_request import RequestData, RequestPayload, ContextData
from tests.integration.base_integration_test import BaseIntegrationTest


class TestHomePageResponseDataPreparation(BaseIntegrationTest):
    """
    test for simple home page (without args)
    test for filtered by search
    test for filtered by category
    test for filtered by subject

    ResponseData.resource should has only notes visible for data.context.person_visibility
    """

    def test_home_page_without_filtering(self):
        with self.app_context():
            data = RequestData(
                RequestPayload(
                    {}
                ),
                ContextData(
                    {"jwt_scope": self.person_logged.name}
                )
            )
            response = HomeLogic.render_home_page_filtered(data)

            self.assertSetEqual(
                {note.title for note in self.notes_visible},
                {note['title'] for note in response.resource},
                "Notes titles are not the same as expected in non filtered home page"
            )
            self.assertEqual(
                len(self.notes_visible),
                len(response.resource),
                "Number of visible notes on non filtered home page incorrect"
            )

    def test_home_page_filtered_by_visible_category(self):
        with self.app_context():
            for i, category in enumerate(self.categories_visible):
                with self.subTest(i=i):
                    data = RequestData(
                        RequestPayload(
                            {'category': category.name}
                        ),
                        ContextData(
                            {"jwt_scope": self.person_logged.name}
                        )
                    )

                    response = HomeLogic.render_home_page_filtered(data)

                    self.assertEqual(
                        len(self.notes_visible) - i,
                        len(response.resource),
                        "Visible notes count is incorrect!"
                    )
                    for j, note in enumerate(response.resource):
                        with self.subTest(j=j):
                            self.assertIn(
                                note['title'],
                                self.visible_titles,
                                "Note should not be visible!"
                            )

    def test_home_page_filtered_by_non_visible_category(self):
        with self.app_context():
            for i, category in enumerate(self.categories_invisible):
                with self.subTest(i=i):
                    data = RequestData(
                        RequestPayload(
                            {'category': category.name}
                        ),
                        ContextData(
                            {"jwt_scope": self.person_logged.name}
                        )
                    )

                    response = HomeLogic.render_home_page_filtered(data)

                    self.assertEqual(
                        0,
                        len(response.resource),
                        "Visible notes count should be 0!"
                    )

    def test_home_page_filtered_by_visible_subject(self):
        with self.app_context():
            for i, subject in enumerate(self.subjects_visible):
                with self.subTest(i=i):
                    data = RequestData(
                        RequestPayload(
                            {'subject': subject.name}
                        ),
                        ContextData(
                            {"jwt_scope": self.person_logged.name}
                        )
                    )

                    response = HomeLogic.render_home_page_filtered(data)

                    self.assertEqual(
                        len(self.notes_visible) - i,
                        len(response.resource),
                        "Visible notes count is incorrect!"
                    )
                    for j, note in enumerate(response.resource):
                        with self.subTest(j=j):
                            self.assertIn(
                                note['title'],
                                self.visible_titles,
                                "Note should not be visible!"
                            )

    def test_home_page_filtered_by_invisible_subject(self):
        with self.app_context():
            for i, subject in enumerate(self.subjects_invisible):
                with self.subTest(i=i):
                    data = RequestData(
                        RequestPayload(
                            {'subject': subject.name}
                        ),
                        ContextData(
                            {"jwt_scope": self.person_logged.name}
                        )
                    )

                    response = HomeLogic.render_home_page_filtered(data)

                    self.assertEqual(
                        0,
                        len(response.resource),
                        "Visible notes count should be 0!"
                    )

    def test_home_page_filtered_by_visible_search(self):
        with self.app_context():
            data = RequestData(
                RequestPayload(
                    {'search': "visible"}
                ),
                ContextData(
                    {"jwt_scope": self.person_logged.name}
                )
            )

            response = HomeLogic.render_home_page_filtered(data)

            self.assertEqual(
                len(self.notes_visible),
                len(response.resource),
                "Visible notes count is incorrect!"
            )
            for j, note in enumerate(response.resource):
                with self.subTest(j=j):
                    self.assertIn(
                        note['title'],
                        self.visible_titles,
                        "Note should not be visible!"
                    )

    def test_home_page_filtered_by_invisible_search(self):
        with self.app_context():
            data = RequestData(
                RequestPayload(
                    {'search': "invisible"}
                ),
                ContextData(
                    {"jwt_scope": self.person_logged.name}
                )
            )

            response = HomeLogic.render_home_page_filtered(data)

            self.assertEqual(
                0,
                len(response.resource),
                "Visible notes count should be 0!"
            )

    def test_home_page_resource_fields_displayed_for_user(self):
        with self.app_context():
            data = RequestData(
                RequestPayload(
                    {}
                ),
                ContextData(
                    {"jwt_scope": self.person_logged.name}
                )
            )
            response = HomeLogic.render_home_page_filtered(data)

            note = response.resource[0]
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

    def test_home_page_resource_fields_displayed_for_admin(self):
        with self.app_context():
            data = RequestData(
                RequestPayload(
                    {}
                ),
                ContextData(
                    {"jwt_admin": True}
                )
            )
            response = HomeLogic.render_home_page_filtered(data)

            note = response.resource[0]
            user_note_keys = ['real_update_date', 'title', 'real_creation_date', 'content', 'id',
                              'game_creation_date', 'subjects', 'game_update_date',
                              'persons_visibility', ]
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
