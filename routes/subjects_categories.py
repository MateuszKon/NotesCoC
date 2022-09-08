from flask import request
from sqlalchemy.exc import NoResultFound

from libs.jwt_functions import jwt_required_with_redirect
from models import SubjectModel
from models.subjects_categories import SubjectCategoryModel
from schemas.subjects_categories import SubjectCategorySchema

SUBJECT_DOESNT_EXIST = "Subject {} doesn't exist!"
SUBJECT_CATEGORY_ALREADY_EXIST = "Subject category {} already exist!"
SUBJECT_CATEGORY_ADDED = "Subject category {} added."
SUBJECT_CATEGORY_EDITED = "Subject category {} edited."
SUBJECT_CATEGORY_DOESNT_EXIST = "Subject category {} doesn't exist!"
SUBJECT_CATEGORY_DELETED = "Subject category {} deleted."

subject_category_schema = SubjectCategorySchema()


class SubjectCategoryRoutes:

    @classmethod
    @jwt_required_with_redirect(admin=True)
    def subject_category(cls, name: str):
        subject_category_ = SubjectCategoryModel.find_by_name(name,
                                                              allow_none=True)
        if request.method == "POST":
            if subject_category_:
                return {"message": SUBJECT_CATEGORY_ALREADY_EXIST.format(
                    name)}, 400
            new_category = SubjectCategoryModel(name=name)
            new_category.save_to_db()
            return {"message": SUBJECT_CATEGORY_ADDED.format(name)}, 201

        if request.method == "PUT":
            new_category = subject_category_schema.load(request.json)
            if subject_category_:
                subject_category_.name = new_category.name
                subject_category_.save_to_db()
                return {"message": SUBJECT_CATEGORY_EDITED.format(name)}, 200
            new_category.save_to_db()
            return {"message": SUBJECT_CATEGORY_ADDED.format(
                new_category.name)}, 201

        if request.method == "DELETE":
            if subject_category_ is None:
                return {"message": SUBJECT_CATEGORY_DOESNT_EXIST.format(name)},\
                       400
            subject_category_.delete_from_db()
            return {"message": SUBJECT_CATEGORY_DELETED.format(name)}, 200

        # request.method == "GET"
        if subject_category_ is None:
            return {"message": SUBJECT_CATEGORY_DOESNT_EXIST.format(name)}, 400
        return subject_category_schema.dump(subject_category_), 200

    @classmethod
    @jwt_required_with_redirect(admin=True)
    def subject_categories(cls):
        return {"subject_categories": subject_category_schema.dump(
            SubjectCategoryModel.get_all(), many=True)}, 200


