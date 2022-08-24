from models.persons import PersonModel
from routes.notes import NoteRoutes
from tests.unit.routes.base_unit_routes_test import BaseTestUnitRoutes


class TestVisibilityNotes(BaseTestUnitRoutes):

    # TODO: something is wrong in test or function
    def test_adding_and_removing_visibility(self):
        persons = [
            PersonModel(name="person1"),
            PersonModel(name="person2"),
            PersonModel(name="person3"),
            PersonModel(name="person4"),
        ]
        state_dictionary = {
            "vis_previous_person1": "False",
            "visibility_person1": "True",
            "vis_previous_person2": "True",
            "visibility_person2": "False",
            "vis_previous_person3": "False",
            "visibility_person3": "False",
            "vis_previous_person4": "True",
            "visibility_person4": "True",
        }
        with self.app_context():
            for person in persons:
                person.save_to_db()
            persons_on, persons_off = NoteRoutes._visibility_changing_list(
                persons,
                state_dictionary,
            )
            print("ON " + " ".join([
                person.name for person in persons_on
            ]))
            print("OFF " " ".join([
                person.name for person in persons_off
            ]))