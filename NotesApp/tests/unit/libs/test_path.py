from pathlib import Path

from libs.path import get_project_directory
from NotesApp.tests.base_test import BaseTest


class TestPathGeneration(BaseTest):

    def test_generating_project_directory_path(self):
        path = Path.cwd()
        self.assertEqual(
            path.name, "NotesCoC",
            "Project directory should be of specific name!"
        )
        self.assertTrue(
            path.joinpath("README.md").exists(),
            "Project directory probably contains README.md file"
        )
