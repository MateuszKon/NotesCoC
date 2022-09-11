from typing import List

from sqlalchemy import Table, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from db import db
from models.base_resource import BaseResourceModel

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

    @classmethod
    def get_all(cls) -> List["SubjectCategoryModel"]:
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name: str, allow_none=False):
        if allow_none:
            return cls.query.filter_by(name=name).one_or_none()
        return cls.query.filter_by(name=name).one()
