from datetime import date

from wtforms import StringField, DateField
from wtforms.validators import DataRequired, Length
from wtforms_alchemy import ModelForm

from models import SubjectModel


class SubjectForm(ModelForm):

    class Meta:
        model = SubjectModel
        # include = ('name',)

