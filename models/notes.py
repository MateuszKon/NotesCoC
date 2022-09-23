from datetime import datetime, date
from typing import List, Set

from sqlalchemy import Column, Integer, String, Date, DateTime, or_
from sqlalchemy.orm import relationship

from db import db
# from models.subjects import SubjectModel
from models.subjects_categories import SubjectCategoryModel
from models.notes_subjects import notes_subjects
from models.persons_notes import persons_notes


class NoteModel(db.Model):

    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    title = Column(String(80))
    content = Column(String(1000))
    game_creation_date = Column(Date, default=date(1920, 1, 1))
    game_update_date = Column(Date, default=date(1920, 1, 1))
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
        secondary="subjects",
        primaryjoin="notes_subjects",
        secondaryjoin="subjects_categories",
        viewonly=True,
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
        return cls.query.all()

    @classmethod
    def get_all_visible(cls, person_name: str = None) -> List["NoteModel"]:
        if person_name is None:
            return cls.get_all()
        return cls.add_filter_persons_visibility_query(cls.query, person_name).\
            all()

    def get_subjects_and_categories_words(self) -> Set[str]:
        subjects = self.subjects.all()
        categories = set()
        for subject in subjects:
            categories.update(set(subject.categories.all()))
        words = {
            category.name for category in categories
        }
        words.update(
            {subject.name for subject in subjects}
        )
        return words

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
        filter_list = [NoteModel.title.contains(x) for x in search_words] + \
                      [NoteModel.content.contains(x) for x in search_words]
        return qs.filter(or_(*filter_list))

    @classmethod
    def category_filtering_qs(cls, qs, category):
        pass
        return qs.join(cls.categories).filter(
            name=category
        )

    @classmethod
    def subject_filtering_qs(cls, qs, subject):
        return qs.join(cls.subjects).filter_by(name=subject)