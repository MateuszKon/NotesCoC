from typing import List

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.notes import NoteModel
from models.persons_notes import persons_notes
from models.base_resource import BaseResourceModel


class PersonModel(BaseResourceModel):
    __tablename__ = "persons"

    name = Column(String(80), primary_key=True)
    notes_visible = relationship(
        "NoteModel",
        secondary=persons_notes,
        back_populates="persons_visibility",
        lazy="dynamic",
        collection_class=set,
    )

    def __str__(self) -> str:
        return f"{self.name}"

    def is_note_visible(self, note_id: int):
        return bool(self.notes_visible.filter(
            NoteModel.id == note_id).one_or_none())

    @classmethod
    def find_by_name(cls, name: str, allow_none=False):
        if allow_none:
            return cls.query.filter_by(name=name).one_or_none()
        return cls.query.filter_by(name=name).one()

    @classmethod
    def get_all(cls) -> List["PersonModel"]:
        return cls.query.all()
