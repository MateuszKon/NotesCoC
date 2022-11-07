from datetime import date

from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length
from wtforms_alchemy import ModelForm

from models import SubjectCategoryModel


class CategoryForm(ModelForm):

    class Meta:
        model = SubjectCategoryModel
        include = ("name",)
