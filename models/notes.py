from typing import List

from db import db


class NoteModel(db.Model):

    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    content = db.Column(db.String(1000))

    @classmethod
    def empty_note(cls):
        return cls(id=None, title="", content="")

    @classmethod
    def find_by_id(cls, note_id: int) -> "NoteModel":
        return cls.query.filter_by(id=note_id).one()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls) -> List["NoteModel"]:
        return cls.query.all()
