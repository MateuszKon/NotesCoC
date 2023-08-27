from database.db import db
from NotesApp.ma import ma
from database.models import PersonModel


class PersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PersonModel
        # load_only = (,)
        # dump_only = ("id",)
        load_instance = True
        sqla_session = db.session
