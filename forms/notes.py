from wtforms import StringField
from wtforms.validators import DataRequired, Length
from wtforms_alchemy import ModelForm

from models import NoteModel


class CustomNoteForm(ModelForm):
    title = StringField("Tytuł", validators=[DataRequired(), Length(max=80)])
    content = StringField("Treść", validators=[Length(max=5000)])

    class Meta:
        model = NoteModel
