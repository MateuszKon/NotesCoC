from typing import List, Set

from flask import abort
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.notes import NoteModel
from models.notes_subjects import notes_subjects
from models.base_resource import BaseResourceModel
from models.subjects_categories import subjects_categories
from routes.i_request import RequestData


class SubjectModel(BaseResourceModel):
    __tablename__ = "subjects"

    name = Column(String(80), primary_key=True)
    categories = relationship(
        "SubjectCategoryModel",
        secondary=subjects_categories,
        back_populates="subjects",
        lazy="dynamic",
        collection_class=set,
        order_by="SubjectCategoryModel.name",
    )
    notes = relationship(
        "NoteModel",
        secondary=notes_subjects,
        back_populates="subjects",
        lazy="dynamic",
        collection_class=set,
        order_by="NoteModel.real_update_date.desc()"
    )
    _notes_filtered = None

    def read(
            self,
            data: RequestData,
    ) -> 'SubjectModel':
        self.filter_notes(data)
        if not data.context.admin and not self.has_notes:
            abort(404)
        return self

    @classmethod
    def list(
            cls,
            data: RequestData,
    ) -> List['SubjectModel']:
        category = data.data.get('category')
        qs = cls.query
        if category is not None:
            qs = qs.join(cls.categories).filter_by(name=category)
        qs = qs.order_by(cls.name)

        objs = qs.all()
        if data.context.admin and data.context.person_visibility is None:
            return [obj.filter_notes(data) for obj in objs]
        return [obj for obj in objs if obj.filter_notes(data).has_notes]

    @property
    def notes_filtered(self):
        return self._notes_filtered

    @property
    def has_notes(self):
        return len(self.notes_filtered) > 0

    def filter_notes(self, data: RequestData) -> "SubjectModel":
        person = data.context.person_visibility
        self._notes_filtered = NoteModel.filter_notes(self.notes, person)
        return self

    @classmethod
    def find_by_name(cls, name: str, allow_none=False) -> "SubjectModel":
        if allow_none:
            return cls.query.filter_by(name=name).one_or_none()
        return cls.query.filter_by(name=name).one()

    @classmethod
    def get_all(cls) -> List["SubjectModel"]:
        return cls.query.order_by("name").all()

    def add_categories(self, categories: Set["SubjectCategoryModel"]):
        self.categories.extend(categories)

    def remove_categories(self, categories: Set["SubjectCategoryModel"]):
        for category in categories:
            self.categories.remove(category)
