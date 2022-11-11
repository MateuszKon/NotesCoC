from wtforms_alchemy import QuerySelectMultipleField

from forms.base_form import OrderedForm
from models import SubjectModel, SubjectCategoryModel


class SubjectForm(OrderedForm):

    _field_order = ['name', 'Kategorie']

    class Meta:
        model = SubjectModel
        include = ('name',)

    categories = QuerySelectMultipleField(
        "Kategorie",
        query_factory=lambda: SubjectCategoryModel.query,
    )
