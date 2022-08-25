from sqlalchemy.exc import NoResultFound

from models.persons import PersonModel
from tests.unit.models.base_unit_models_test import BaseTestUnitModels


class TestPersonModel(BaseTestUnitModels):

    def test_find_by_name_allow_none_true(self):
        with self.app_context():
            self.assertIsNone(
                PersonModel.find_by_name("test", allow_none=True),
                "Finding person by name when it does not exist not returned "
                "None when parameter allow_none=True")

    def test_find_by_name_allow_none_default(self):
        with self.app_context():
            with self.assertRaises(NoResultFound):
                PersonModel.find_by_name("test")
