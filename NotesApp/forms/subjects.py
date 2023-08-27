from wtforms_alchemy import QuerySelectMultipleField

from NotesApp.forms.base_form import OrderedForm
from database.models import SubjectModel, SubjectCategoryModel


class SubjectForm(OrderedForm):

    _field_order = ['name', 'Kategorie']

    class Meta:
        model = SubjectModel
        include = ('name',)

    categories = QuerySelectMultipleField(
        "Kategorie",
        query_factory=lambda: SubjectCategoryModel.query,
    )
