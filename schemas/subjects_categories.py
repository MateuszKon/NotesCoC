from marshmallow import fields
from marshmallow.class_registry import get_class

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

    subjects = fields.Method("get_subjects_")

    def __init__(
            self,
            subjects_schema: str = None,
            subjects_param: dict = None,
            *args,
            **kwargs
    ):
        if subjects_param is None:
            subjects_param = {}
        self.subjects_schema = None
        self.subjects_schema_name = subjects_schema
        self.subjects_schema_param = subjects_param
        super().__init__(*args, **kwargs)

    def get_subjects_(self, obj: SubjectCategoryModel):
        if self.subjects_schema is None:
            self._init_subjects_schema()
        return self.subjects_schema.dump(obj.subjects_filtered, many=True)

    def _init_subjects_schema(self):
        class_ = get_class(self.subjects_schema_name)
        self.subjects_schema = class_(**self.subjects_schema_param)

