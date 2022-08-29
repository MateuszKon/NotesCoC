from typing import List

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from db import db
from models.notes_subjects import notes_subjects
from models.subjects_categories import subjects_categories


class SubjectModel(db.Model):
    __tablename__ = "subjects"

    name = Column(String(80), primary_key=True)
    categories = relationship(
        "SubjectCategoryModel",
        secondary=subjects_categories,
        back_populates="subjects",
        lazy="dynamic",
        collection_class=set,
    )
    notes = relationship(
        "NoteModel",
        secondary=notes_subjects,
        back_populates="subjects",
        lazy="dynamic",
        collection_class=set,
    )

    @classmethod
    def get_all(cls) -> List["SubjectModel"]:
        return cls.query.all()
