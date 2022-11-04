from datetime import date

from wtforms import StringField, DateField
from wtforms.validators import DataRequired, Length
from wtforms_alchemy import ModelForm

from models import NoteModel


class CustomNoteForm(ModelForm):

    class Meta:
        model = NoteModel
        field_args = {
            "title": {"validators": [DataRequired(), Length(max=80)]},
            "game_creation_date": {"format": "%Y-%m-%d", "default": date(1920, 1, 1)},
            "game_update_date": {"format": "%Y-%m-%d", "default": date(1920, 1, 1)},
        }

