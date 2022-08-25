from models.notes import NoteModel
from tests.unit.base_unit_database_test import BaseTestUnitDatabase


class TestNoteModel(BaseTestUnitDatabase):

    def setUp(self) -> None:
        self.note_title = "test_title"
        self.note_content = "Some content of the note"
        self.note = NoteModel(
            title=self.note_title,
            content=self.note_content,
        )

    def test_note_model_initialization(self):
        self.assertEqual(self.note.title, self.note_title,
                         "Title of the note is different after init!")
        self.assertEqual(self.note.content, self.note_content,
                         "Content of the note is different after init!")

    def test_note_persons_visibility_empty(self):
        self.assertEqual(self.note.persons_visibility.count(), 0,
                         "Note is visibly to some person after init!")
