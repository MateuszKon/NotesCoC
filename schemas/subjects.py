from db import db
from ma import ma
from models.subjects import SubjectModel


class SubjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SubjectModel
        # load_only = (,)
        # dump_only = ("id",)
        load_instance = True
        sqla_session = db.session


subject_schema = SubjectSchema()
subject_name_schema = SubjectSchema(only=('name',))
