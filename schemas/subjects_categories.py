from typing import List

from marshmallow import fields, pre_dump
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


    @pre_dump(pass_many=True)
    def filter_empty_category(
            self,
            objs: List[SubjectCategoryModel],
            **kwargs
    ) -> List[SubjectCategoryModel]:
        if self.subjects_schema_name is None:
            return objs
        if self.subjects_schema is None:
            self._init_subjects_schema()
        for obj in objs:
            obj.subjects_ = self.subjects_schema.dump(
                obj.subjects, many=True
            )
        return [obj for obj in objs if len(obj.subjects_) > 0]

    def get_subjects_(self, obj: SubjectCategoryModel):
        if not hasattr(obj, 'subjects_'):
            if self.subjects_schema is None:
                self._init_subjects_schema()
            obj.subjects_ = self.subjects_schema.dump(obj.subjects, many=True)
        return obj.subjects_

    def _init_subjects_schema(self):
        class_ = get_class(self.subjects_schema_name)
        self.subjects_schema = class_(**self.subjects_schema_param)

