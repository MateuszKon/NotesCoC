from datetime import date

from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length
from wtforms_alchemy import ModelForm

from models import NoteModel


class CustomNoteForm(ModelForm):
    title = StringField("Tytuł", validators=[DataRequired(), Length(max=80)])
    content = TextAreaField("Treść", render_kw={"rows": 13})

    class Meta:
        model = NoteModel
        field_args = {
            "game_creation_date": {"format": "%Y-%m-%d", "default": date(1920, 1, 1)},
            "game_update_date": {"format": "%Y-%m-%d", "default": date(1920, 1, 1)},
        }

