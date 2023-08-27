from sqlalchemy import Table, Column, ForeignKey

from database.db import db


notes_subjects = Table(
    "notes_subjects",
    db.Model.metadata,
    Column("note_id", ForeignKey("notes.id"), primary_key=True),
    Column("subject_name", ForeignKey("subjects.name"), primary_key=True),
)
