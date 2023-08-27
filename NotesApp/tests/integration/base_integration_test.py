import os
from math import floor
from unittest.mock import patch

from NotesApp.app import app
from database.db import db
from database.models import PersonModel, SubjectCategoryModel, SubjectModel, NoteModel, UserModel
from NotesApp.tests.base_test import BaseTest


class BaseIntegrationTest(BaseTest):

    @classmethod
    def setUpClass(cls):
        app.config["SQLALCHEMY_DATABASE_URI"] = \
            os.environ.get("TEST_DATABASE_URI", "sqlite://")
        with app.app_context():
            db.init_app(app)

    def setUp(self):
        with app.app_context():
            db.create_all()

            # Creating models
            with patch("models.users.bcrypt.hashpw") as mock_hashing:
                mock_hashing.return_value = "aaa".encode("utf8")
                self.user = UserModel(login="mym", password='mym', person_name=None)
            self.person_logged = PersonModel(name='logged')
            self.persons_others = [
                PersonModel(name=f'other{i}') for i in range(0, 2)
            ]
            self.categories_visible = [
                SubjectCategoryModel(name=f'cat_visible{i}') for i in range(0, 3)
            ]
            self.categories_invisible = [
                SubjectCategoryModel(name=f'cat_invisible{i}') for i in range(0, 3)
            ]
            self.subjects_visible = [
                SubjectModel(name=f'subj_visible{i}') for i in range(0, 3)
            ]
            self.subjects_invisible = [
                SubjectModel(name=f'subj_invisible{i}') for i in range(0, 3)
            ]
            self.notes_visible = [
                NoteModel(title=f"note visible{i}", content=f"vis_mym {i}") for i in range(0, 5)
            ]
            self.notes_invisible = [
                NoteModel(title=f"note invisible{i}", content=f"invis_mym {i}") for i in range(0, 10)
            ]
            self.visible_titles = [note.title for note in self.notes_visible]
            self.visible_subjects_names = [subject.name for subject in self.subjects_visible]
            self.visible_categories_names = [category.name for category in self.categories_visible]

            # Adding categories to subjects
            self.subjects_visible[0].add_categories(set(self.categories_visible[0:1]))
            self.subjects_visible[1].add_categories(set(self.categories_visible[0:2]))
            self.subjects_visible[2].add_categories(set(self.categories_visible[0:3]))
            self.subjects_invisible[0].add_categories(set(self.categories_invisible[0:1]))
            self.subjects_invisible[1].add_categories(set(self.categories_invisible[0:2] +
                                                          self.categories_visible[0:1]))
            self.subjects_invisible[2].add_categories(set(self.categories_invisible[0:3] +
                                                          self.categories_visible[0:2]))

            # Adding visible notes to person and subjects
            for i, note in enumerate(self.notes_visible):
                note.persons_visibility.extend({self.person_logged})
                note.add_subjects(
                    set(self.subjects_visible[0:min(i + 1, len(self.subjects_visible))])
                )

            # Adding invisible notes to other persons and subjects
            note_two_third_count = floor(len(self.notes_invisible) * 2 / 3)
            note_half_count = floor(len(self.notes_invisible) / 2)
            for i, note in enumerate(self.notes_invisible):
                j = i - note_half_count
                if i < note_half_count:
                    note.persons_visibility.extend({self.persons_others[0]})
                    j = i
                elif i < note_two_third_count:
                    note.persons_visibility.extend(set(self.persons_others))

                note.add_subjects(
                    set(self.subjects_invisible[0:min(j + 1, len(self.subjects_invisible))])
                )
                if i >= note_half_count:
                    note.add_subjects(
                        set(self.subjects_visible[0:min(j + 1, len(self.subjects_visible))])
                    )

            # Adding models to session and commit
            db.session().expire_on_commit = False
            for models_list in [
                [self.user],
                [self.person_logged],
                self.persons_others,
                self.categories_visible,
                self.categories_invisible,
                self.subjects_visible,
                self.subjects_invisible,
                self.notes_visible,
                self.notes_invisible,
            ]:
                for model in models_list:
                    db.session.add(model)
            db.session.commit()
        self.app_context = app.app_context

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
