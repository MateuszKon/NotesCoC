from datetime import date

from wtforms import StringField, TextAreaField, FieldList
from wtforms.validators import DataRequired, Length
from wtforms_alchemy import QuerySelectMultipleField, ModelFormField

from forms.base_form import OrderedForm
from forms.subjects import SubjectForm
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


class AdminNoteForm(CustomNoteForm):

    _field_order = ['title', "content", "persons_visibility", "subjects", "game_creation_date",
                    "game_update_date", "new_subjects"]

    persons_visibility = QuerySelectMultipleField("Widoczność postaci")
    new_subjects = FieldList(
        ModelFormField(SubjectForm, label="Nowy temat"),
        label="Nowe tematy",
    )

