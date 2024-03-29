from datetime import datetime, date
from typing import List, Set

from sqlalchemy import Column, Integer, String, Date, DateTime, or_, func
from sqlalchemy.orm import relationship
from wtforms.validators import DataRequired, Length

from db import db
from models.notes_subjects import notes_subjects
from models.persons_notes import persons_notes


class NoteModel(db.Model):

    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    title = Column(String(80))
    content = Column(String(5000))
    game_creation_date = Column(
        Date,
        default=date(1920, 1, 1),
        info={"label": "Data gry powstania notatki"}
    )
    game_update_date = Column(
        Date,
        default=date(1920, 1, 1),
        info={"label": "Data gry aktualizacji notatki"}
    )
    real_creation_date = Column(DateTime, default=datetime.now)
    real_update_date = Column(DateTime, default=datetime.now)
    persons_visibility = relationship(
        "PersonModel",
        secondary=persons_notes,
        back_populates="notes_visible",
        lazy="dynamic",
        collection_class=set,
    )
    subjects = relationship(
        "SubjectModel",
        secondary=notes_subjects,
        back_populates="notes",
        lazy="dynamic",
        collection_class=set,
    )
    categories = relationship(
        "SubjectCategoryModel",
        secondary="notes_subjects."
                  "join(subjects_categories, notes_subjects.columns.subject_name == "
                  "subjects_categories.columns.subject_name)",
        viewonly=True,
        lazy="dynamic",
        collection_class=set,
    )

    def save_to_db(self):
        self.real_update_date = datetime.now()
        super().save_to_db()

    def add_persons_visibility(self, persons: Set["PersonModel"]):
        persons = {
            person for person in persons if not person.is_note_visible(self.id)
        }
        self.persons_visibility.extend(persons)

    def remove_persons_visibility(self, persons: Set["PersonModel"]):
        for person in persons:
            self.persons_visibility.remove(person)

    def add_subjects(self, subjects: Set["SubjectModel"]):
        self.subjects.extend(subjects)

    def remove_subjects(self, subjects: Set["SubjectModel"]):
        for subject in subjects:
            self.subjects.remove(subject)

    @classmethod
    def find_by_id(cls, note_id: int) -> "NoteModel":
        return cls.query.filter_by(id=note_id).first_or_404()

    @classmethod
    def find_by_id_with_scope(cls, note_id: int, person: str) -> "NoteModel":
        if person is None:
            return cls.find_by_id(note_id)
        return cls.query.filter_by(id=note_id)\
            .join(cls.persons_visibility)\
            .filter_by(name=person)\
            .first_or_404()

    @classmethod
    def get_all(cls) -> List["NoteModel"]:
        return cls.query

    @classmethod
    def get_all_visible(cls, person_name: str = None) -> List["NoteModel"]:
        if person_name is None:
            qs = cls.get_all()
        else:
            qs = cls.add_filter_persons_visibility_query(cls.query, person_name)
        return qs.order_by(cls.game_update_date.desc(),
            cls.real_update_date.desc())

    @classmethod
    def filter_notes(cls, qs, person: str) -> List["NoteModel"]:
        return cls.add_filter_persons_visibility_query(
            qs,
            person,
        ).all()

    @classmethod
    def add_filter_persons_visibility_query(cls, qs, person_name: str = None):
        if person_name is not None:
            qs = qs.join(cls.persons_visibility).filter_by(name=person_name)
        return qs

    @classmethod
    def words_filtering_qs(cls, qs, search_words):
        filter_list = [func.lower(NoteModel.title).contains(x) for x in search_words] + \
                      [func.lower(NoteModel.content).contains(x) for x in search_words]
        return qs.filter(or_(*filter_list))

    @classmethod
    def category_filtering_qs(cls, qs, category):
        return qs.join(cls.categories).filter_by(
            name=category
        )

    @classmethod
    def subject_filtering_qs(cls, qs, subject):
        return qs.join(cls.subjects).filter_by(name=subject)
