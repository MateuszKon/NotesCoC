from db import db
from ma import ma
from models.subjects_categories import SubjectCategoryModel


class SubjectCategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SubjectCategoryModel
        # load_only = (,)
        # dump_only = ("id",)
        load_instance = True
        sqla_session = db.session
