from typing import List

from sqlalchemy import Table, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from db import db
from models.base_resource import BaseResourceModel
from routes.i_request import RequestData

subjects_categories = Table(
    "subjects_categories",
    db.Model.metadata,
    Column("subject_name", ForeignKey("subjects.name"), primary_key=True),
    Column("subject_categories_name", ForeignKey("subject_categories.name"),
           primary_key=True),
)


class SubjectCategoryModel(BaseResourceModel):
    __tablename__ = "subject_categories"

    name = Column(String(80), primary_key=True)
    subjects = relationship(
        "SubjectModel",
        secondary=subjects_categories,
        back_populates="categories",
        lazy="dynamic",
        collection_class=set,
    )
    _subjects_filtered = None

    def read(
            self,
            data: RequestData,
    ) -> 'SubjectCategoryModel':
        return self.filter_subjects(data)

    @classmethod
    def list(
            cls,
            data: RequestData,
    ) -> List['SubjectCategoryModel']:
        objs = super().list(data)
        if data.context.admin and data.context.person_visibility is None:
            return [obj.read(data) for obj in objs]
        return [obj for obj in objs if obj.read(data).has_subjects]

    @property
    def has_subjects(self):
        return len(self.subjects_filtered) > 0

    @property
    def subjects_filtered(self):
        return self._subjects_filtered

    def filter_subjects(
            self,
            data: RequestData,
    ) -> 'SubjectCategoryModel':
        if data.context.admin and data.context.person_visibility is None:
            filtered = [subject.read(data) for subject in self.subjects]
        else:
            filtered = [
                subject for subject in self.subjects
                if subject.filter_notes(data).has_notes
            ]
        self._subjects_filtered = filtered
        return self

    @classmethod
    def get_all(cls) -> List["SubjectCategoryModel"]:
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name: str, allow_none=False):
        if allow_none:
            return cls.query.filter_by(name=name).one_or_none()
        return cls.query.filter_by(name=name).one()
