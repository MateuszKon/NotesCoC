from models.persons import PersonModel
from logic.notes import NoteLogic
from routes.i_request import RequestPayload
from tests.unit.base_unit_database_test import BaseTestUnitDatabase


class TestVisibilityNotes(BaseTestUnitDatabase):

    def test_adding_and_removing_visibility(self):
        persons = [
            PersonModel(name="person1"),
            PersonModel(name="person2"),
            PersonModel(name="person3"),
            PersonModel(name="person4"),
        ]
        state_dictionary = RequestPayload({
            "vis_previous_person1": "False",
            "visibility_person1": "True",
            "vis_previous_person2": "True",
            # "visibility_person2": "False",
            "vis_previous_person3": "False",
            # "visibility_person3": "False",
            "vis_previous_person4": "True",
            "visibility_person4": "True",
        })
        with self.app_context():
            for person in persons:
                person.save_to_db()
            persons_on, persons_off = NoteLogic._visibility_changing_list(
                persons,
                state_dictionary,
            )
            self.assertIn(persons[0], persons_on,
                          "First person was switched to visible!")
            self.assertEqual(len(persons_on), 1,
                             "Only one person is switched to on!")
            self.assertIn(persons[1], persons_off,
                          "Second person was switched to invisible!")
            self.assertEqual(len(persons_off), 1,
                             "Only one person is switched to off!")

    def test_visibility_from_form_send_with_false_value_previous_true(self):
        persons = [
            PersonModel(name="person1"),
        ]
        state_dictionary = RequestPayload({
            "vis_previous_person1": "True",
            "visibility_person1": "False",
        })
        with self.app_context():
            for person in persons:
                person.save_to_db()
            with self.assertRaises(ValueError):
                NoteLogic._visibility_changing_list(
                    persons,
                    state_dictionary,
                )

    def test_visibility_from_form_send_with_false_value_previous_false(self):
        persons = [
            PersonModel(name="person1"),
        ]
        state_dictionary = RequestPayload({
            "vis_previous_person1": "False",
            "visibility_person1": "False",
        })
        with self.app_context():
            for person in persons:
                person.save_to_db()
            with self.assertRaises(ValueError):
                NoteLogic._visibility_changing_list(
                    persons,
                    state_dictionary,
                )