from unittest.mock import MagicMock

from werkzeug.exceptions import NotFound

from config_routes import configure_subject_categories_routes
from routes.i_request import RequestData, RequestPayload, ContextData
from tests.integration.base_integration_test import BaseIntegrationTest


class TestCategoriesResourceResponseDataPreparation(BaseIntegrationTest):
    # TODO: test cases
    """
    test for viewing single category by user (check ResponseData.resource)
    test for viewing single category by user (404 when person do not see any notes)
    test for viewing all categories by user (only visible categories and only visible subjects)
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        app_mock = MagicMock()
        cls.routes = configure_subject_categories_routes(app_mock)

    def test_viewing_category_by_user(self):
        with self.app_context():
            data = RequestData(
                RequestPayload(
                    {}
                ),
                ContextData(
                    {"jwt_scope": self.person_logged.name}
                )
            )
            for cat_i, category in enumerate(self.categories_visible):
                with self.subTest(category=category.name):
                    identifier = self.routes.identifier.new_value(category.name)
                    obj = self.routes.logic.get_by_identifier(identifier).read(data)
                    resource = self.routes.create_resource_dict(data, obj)

                    user_category_keys = ['name', 'subjects']
                    self.assertEqual(
                        len(resource),
                        len(user_category_keys),
                        "Number of keys of resource dictionary is incorrect!"
                    )
                    for i, key in enumerate(user_category_keys):
                        with self.subTest(i=i):
                            self.assertIn(
                                key,
                                resource,
                                "Resource does not contain key!"
                            )
                    for i, subject in enumerate(resource['subjects']):
                        with self.subTest(j=i):
                            self.assertIn(
                                subject['name'],
                                self.visible_subjects_names
                            )
                    self.assertEqual(
                        len(resource['subjects']),
                        3-cat_i,
                        "Number of visible subjects are incorrect"
                    )
                    user_subject_keys = ['name']
                    for i, key in enumerate(user_subject_keys):
                        with self.subTest(subject_keys=i):
                            self.assertIn(
                                key,
                                resource['subjects'][0],
                                "Resource does not contain key!"
                            )

    def test_not_visible_category_for_user_404(self):
        with self.app_context():
            data = RequestData(
                RequestPayload(
                    {}
                ),
                ContextData(
                    {"jwt_scope": self.person_logged.name}
                )
            )
            for category in self.categories_invisible:
                with self.subTest(category=category.name):
                    with self.assertRaises(NotFound):
                        identifier = self.routes.identifier.new_value(category.name)
                        self.routes.logic.get_by_identifier(identifier).read(data)

    def test_displaying_all_categories_for_user(self):
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
                len(self.categories_visible),
                "Number of visible categories is incorrect!"
            )
            for i, category in enumerate(resource['list']):
                with self.subTest(category=category['name']):
                    self.assertIn(
                        category['name'],
                        self.visible_categories_names,
                        "Showed category is not in visible category!"
                    )
                    for j, subject in enumerate(category['subjects']):
                        with self.subTest(subject=j):
                            self.assertIn(
                                subject['name'],
                                self.visible_subjects_names,
                                "Showed note is not visible note!"
                            )
            user_subject_keys = ['name']
            for key in resource['list'][0]['subjects'][0]:
                with self.subTest(subject_key=i):
                    self.assertIn(
                        key,
                        user_subject_keys,
                        "Subject has not valid key!"
                    )
