from models.notes import NoteModel
from models.persons import PersonModel
from tests.unit.base_unit_database_test import BaseTestUnitDatabase


class TestNoteModelPersonsVisibility(BaseTestUnitDatabase):

    def setUp(self) -> None:
        super().setUp()
        self.note_title = "test_title"
        self.note_content = "Some content of the note"
        self.note = NoteModel(
            title=self.note_title,
            content=self.note_content,
        )
        self.persons = {
            PersonModel(name="person1"),
            PersonModel(name="person2"),
            PersonModel(name="person3"),
        }

    def create_note_in_db(self):
        self.note.save_to_db()

    def create_persons_in_db(self):
        for person in self.persons:
            person.save_to_db()

    def test_adding_persons_visibility(self):
        with self.app_context():
            self.create_note_in_db()
            self.create_persons_in_db()

            self.note.add_persons_visibility(self.persons)
            self.assertEqual(self.note.persons_visibility.count(), 3,
                             "Note is not visibly to persons after adding!")

    def test_adding_and_removing_persons_visibility(self):
        with self.app_context():
            self.create_note_in_db()
            self.create_persons_in_db()

            self.note.add_persons_visibility(self.persons)
            self.assertEqual(self.note.persons_visibility.count(), 3,
                             "Note is not visibly to persons after adding!")

            self.note.remove_persons_visibility({self.persons.pop()})
            self.assertEqual(self.note.persons_visibility.count(), 2,
                             "Note should be visibily only to one person "
                             "after removing second!")

    def test_create_with_persons_visible(self):
        with self.app_context():
            self.create_persons_in_db()
            person1 = self.persons.pop()
            person2 = self.persons.pop()
            note1 = NoteModel(
                title="Title",
                content="Some content",
                persons_visibility={person1, person2}
            )
            note2 = NoteModel(
                title="Title",
                content="Some content",
                persons_visibility={person1, }
            )
            note1.save_to_db()
            note2.save_to_db()
            self.assertEqual(len(NoteModel.get_all_visible(person1.name).all()),
                             2,
                             "Person was added to two notes!")
            self.assertEqual(len(NoteModel.get_all_visible(person2.name).all()),
                             1,
                             "Person was added to a single note!")

    def test_checking_if_note_is_visible(self):
        with self.app_context():
            self.create_persons_in_db()
            person1 = self.persons.pop()
            person2 = self.persons.pop()
            note1 = NoteModel(
                title="Title",
                content="Some content",
                persons_visibility={person1, person2}
            )
            note2 = NoteModel(
                title="Title",
                content="Some content",
                persons_visibility={person1, }
            )
            note1.save_to_db()
            note2.save_to_db()

            self.assertTrue(person1.is_note_visible(note2.id),
                            "Person1 should see note 2!")
            self.assertFalse(person2.is_note_visible(note2.id),
                             "Person2 should not see note 2!")
