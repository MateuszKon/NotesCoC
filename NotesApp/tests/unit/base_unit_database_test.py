import os

from NotesApp.tests.base_test import BaseTest

from NotesApp.app import app
from database.db import db


class BaseTestUnitDatabase(BaseTest):

    @classmethod
    def setUpClass(cls):
        app.config["SQLALCHEMY_DATABASE_URI"] = \
            os.environ.get("TEST_DATABASE_URI", "sqlite://")
        with app.app_context():
            db.init_app(app)

    def setUp(self):
        with app.app_context():
            db.create_all()
        self.app_context = app.app_context

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
