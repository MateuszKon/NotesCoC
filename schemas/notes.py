from marshmallow import fields

from db import db
from ma import ma
from models.notes import NoteModel
from schemas.persons import PersonSchema
from schemas.subjects import SubjectSchema


class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NoteModel
        # load_only = (,)
        # dump_only = (,)
        # include_fk = True
        load_instance = True
        sqla_session = db.session

    persons_visibility = fields.Nested(PersonSchema(many=True, only=('name',)))
    subjects = fields.Nested(SubjectSchema(many=True, only=('name',)))


note_schema = NoteSchema()
note_schema_without_visibility = NoteSchema(exclude=('persons_visibility',))
