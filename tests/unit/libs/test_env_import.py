import os

from libs.path import get_project_directory
from tests.unit.base_unit_test import BaseUnitTest


class TestEnvImport(BaseUnitTest):

    @classmethod
    def setUpClass(cls) -> None:
        env_list = list()
        path = get_project_directory().joinpath(".env.example")
        with open(path, "r") as f:
            for line in f.readlines():
                env_list.append(line.split('=')[0].replace(" ", ""))
        cls.env_list = env_list

    def test_all_env_variables_exist(self):
        import libs.env_import
        for env in self.env_list:
            self.assertIsNotNone(
                os.environ.get(env),
                f"Environment variable '{env}' is not defined!"
            )
