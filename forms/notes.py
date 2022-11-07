from datetime import date

from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length
from wtforms_alchemy import QuerySelectMultipleField

from forms.base_form import OrderedForm
from models import NoteModel


class CustomNoteForm(OrderedForm):

    _field_order = ['title', "content", "subjects", "game_creation_date", "game_update_date"]

    title = StringField("Tytuł", validators=[DataRequired(), Length(max=80)])
    content = TextAreaField("Treść", render_kw={"rows": 13})
    subjects = QuerySelectMultipleField("Tematy")

    class Meta:
        model = NoteModel
        field_args = {
            "game_creation_date": {"format": "%Y-%m-%d", "default": date(1920, 1, 1)},
            "game_update_date": {"format": "%Y-%m-%d", "default": date(1920, 1, 1)},
        }

