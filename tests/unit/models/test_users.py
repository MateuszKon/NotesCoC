import os
import unittest
from unittest.mock import patch

from sqlalchemy.exc import IntegrityError

from models.persons import PersonModel
from models.users import UserModel
from tests.unit.models.base_unit_models_test import BaseTestUnitModels, db


class TestUserModel(BaseTestUnitModels):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user_login = "test_user"
        cls.user_password = "test_password"
        cls.users_person_name = "test_person_name"
        cls.user = UserModel(
            cls.user_login,
            cls.user_password,
            cls.users_person_name
        )

    def test_user_initialization(self):
        self.assertEqual(self.user.login, self.user_login,
                         "User login is different than set!")
        self.assertEqual(self.user.person_name, self.users_person_name,
                         "Users person name is different than set!")
        self.assertIsNotNone(self.user.password,
                             "Initialized user has no password!")

    def test_hashing_password(self):
        self.assertNotEqual(self.user.password, self.user_password,
                            "Initialized users password is not hashed!")

    def test_checking_correct_password(self):
        self.assertTrue(
            self.user.check_password(self.user_password),
            "Correct password checking failed!"
        )

    def test_checking_incorrect_password(self):
        self.assertFalse(
            self.user.check_password("Wrong password"),
            "Incorrect password worked as correct!"
        )

    def test_checking_empty_password(self):
        self.assertFalse(
            self.user.check_password(""),
            "Empty password worked as correct!"
        )

    def test_user_saving_when_person_exist(self):
        with self.app_context():
            PersonModel(name=self.users_person_name).save_to_db()
            self.user.save_to_db()

    @unittest.skipIf("sqlite" in os.environ.get("TEST_DATABASE_URI", "sqlite://"),
                     "SQLite doesn't check Foreign Key constraints.")
    @patch("models.users.bcrypt.hashpw")
    def test_user_saving_when_person_not_exist(self, mock_hashing):
        # Mocking for faster testing (password is not needed, but we need
        # fresh user
        mock_hashing.return_value = "aaa".encode("utf8")
        self.user = UserModel(
            self.user_login,
            self.user_password,
            self.users_person_name
        )
        with self.app_context():
            with self.assertRaises(IntegrityError):
                self.user.save_to_db()


