from sqlalchemy import Table, Column, ForeignKey

from database.db import db


persons_notes = Table(
    "persons_notes",
    db.Model.metadata,
    Column("person_name", ForeignKey("persons.name"), primary_key=True),
    Column("note_id", ForeignKey("notes.id"), primary_key=True),
)
