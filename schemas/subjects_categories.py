from ma import ma
from models.subjects_categories import SubjectCategoryModel


class SubjectCategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SubjectCategoryModel
        # load_only = (,)
        # dump_only = ("id",)
        load_instance = True
