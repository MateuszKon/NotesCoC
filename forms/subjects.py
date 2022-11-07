from wtforms_alchemy import ModelForm, QuerySelectMultipleField

from models import SubjectModel


class SubjectForm(ModelForm):

    class Meta:
        model = SubjectModel
        include = ('name',)

    categories = QuerySelectMultipleField("Kategorie")
