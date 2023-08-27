from wtforms_alchemy import ModelForm

from database.models import SubjectCategoryModel


class CategoryForm(ModelForm):

    class Meta:
        model = SubjectCategoryModel
        include = ("name",)
