from marshmallow import fields

from database.db import db
from NotesApp.ma import ma
from database.models import NoteModel
from NotesApp.schemas.persons import PersonSchema
from NotesApp.schemas.subjects import SubjectSchema
from NotesApp.schemas.subjects_categories import SubjectCategorySchema

DATETIME_STR_FORMAT = '%Y-%m-%d %H:%M:%S'


class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NoteModel
        # load_only = (,)
        # dump_only = (,)
        # include_fk = True

        load_instance = True
        sqla_session = db.session

    real_creation_date = fields.DateTime(DATETIME_STR_FORMAT)
    real_update_date = fields.DateTime(DATETIME_STR_FORMAT)
    persons_visibility = fields.Nested(PersonSchema(many=True, only=('name',)))
    subjects = fields.Nested(SubjectSchema(many=True, only=('name',)))
    categories = fields.Nested(SubjectCategorySchema(many=True, only=('name',)))


note_schema = NoteSchema()
note_schema_without_visibility = NoteSchema(exclude=('persons_visibility',))
