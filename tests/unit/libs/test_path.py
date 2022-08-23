from libs.path import get_project_directory
from tests.unit.base_unit_test import BaseUnitTest


class TestPathGeneration(BaseUnitTest):

    def test_generating_project_directory_path(self):
        path = get_project_directory()
        self.assertEqual(
            path.name, "NotesCoC",
            "Project directory should be of specific name!"
        )
        self.assertTrue(
            path.joinpath("README.md").exists(),
            "Project directory probably contains README.md file"
        )
