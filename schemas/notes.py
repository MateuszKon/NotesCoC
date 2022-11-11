from marshmallow import fields

from db import db
from ma import ma
from models.notes import NoteModel
from schemas.persons import PersonSchema
from schemas.subjects import SubjectSchema
from schemas.subjects_categories import SubjectCategorySchema

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
