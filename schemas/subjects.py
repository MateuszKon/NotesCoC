from typing import List

from marshmallow import fields, pre_dump
from marshmallow.class_registry import get_class

from db import db
from ma import ma
from models import NoteModel
from models.subjects import SubjectModel


class SubjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SubjectModel
        # load_only = (,)
        # dump_only = ("id",)
        load_instance = True
        sqla_session = db.session

    notes = fields.Method("get_notes_")

    def __init__(
            self,
            notes_schema: str = None,
            notes_param: dict = None,
            *args,
            **kwargs
    ):
        if notes_param is None:
            notes_param = {}
        self.notes_schema = None
        self.notes_schema_name = notes_schema
        self.notes_schema_param = notes_param
        super().__init__(*args, **kwargs)

    @pre_dump(pass_many=True)
    def filter_empty_subjects(
            self,
            objs: List[SubjectModel],
            **kwargs
    ) -> List[SubjectModel]:
        if self.notes_schema_name is None:
            return objs
        return [obj for obj in objs
                if len(self.get_persons_notes(obj).notes_) > 0]

    def get_persons_notes(self, obj: SubjectModel):
        if self.notes_schema is None:
            self._init_notes_schema()

        person_visibility = self.context["request-context"].person_visibility
        notes = NoteModel.add_filter_persons_visibility_query(
            obj.notes,
            person_visibility,
        )
        obj.notes_ = notes.all()
        return obj

    def get_notes_(self, obj):
        return self.notes_schema.dump(obj.notes_, many=True)

    def _init_notes_schema(self):
        class_ = get_class(self.notes_schema_name)
        self.notes_schema = class_(**self.notes_schema_param)


subject_name_schema = SubjectSchema(only=('name',))
