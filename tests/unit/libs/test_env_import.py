import os

import libs.env_import  # Import for loading .env file before tests
from libs.path import get_project_directory
from tests.base_test import BaseTest


class TestEnvImport(BaseTest):

    @classmethod
    def setUpClass(cls) -> None:
        env_list = []
        path = get_project_directory().joinpath(".env.example")
        with open(path, "r", encoding='utf-8') as f:
            for line in f.readlines():
                env_list.append(line.split('=')[0].replace(" ", ""))
        cls.env_list = env_list

    def test_all_env_variables_exist(self):
        for env in self.env_list:
            self.assertIsNotNone(
                os.environ.get(env),
                f"Environment variable '{env}' is not defined!"
            )
