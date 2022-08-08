from typing import List, Set

from sqlalchemy import Column, Integer, String, text
from sqlalchemy.orm import relationship

from db import db
from models.persons_notes import persons_notes


class NoteModel(db.Model):

    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    title = Column(String(80))
    content = Column(String(1000))
    persons_visibility = relationship(
        "PersonModel",
        secondary=persons_notes,
        back_populates="notes_visible",
        lazy="dynamic",
        collection_class=set,
    )

    def add_persons_visibility(self, persons: Set["PersonModel"]):
        persons = {
            person for person in persons if not person.is_note_visible(self.id)
        }
        self.persons_visibility.extend(persons)

    def remove_persons_visibility(self, persons: Set["PersonModel"]):
        for person in persons:
            self.persons_visibility.remove(person)

    @classmethod
    def find_by_id(cls, note_id: int) -> "NoteModel":
        return cls.query.filter_by(id=note_id).one()

    @classmethod
    def get_all(cls) -> List["NoteModel"]:
        return cls.query.all()

    @classmethod
    def get_all_visible(cls, person_name: str = None) -> List["NoteModel"]:
        if person_name is None:
            return cls.get_all()
        return cls.query.join(NoteModel.persons_visibility).filter_by(
            name=person_name
        ).all()
