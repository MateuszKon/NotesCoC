from flask import request

from libs.jwt_functions import jwt_required_with_redirect
from models.subjects import SubjectModel
from schemas.subjects import SubjectSchema

subject_schema = SubjectSchema()

SUBJECT_ALREADY_EXIST = "Subject {} already exist!"
SUBJECT_ADDED = "Subject {} added."
SUBJECT_EDITED = "Subject {} edited."
SUBJECT_DOESNT_EXIST = "Subject {} doesn't exist!"
SUBJECT_DELETED = "Subject {} deleted."


class SubjectRoutes:

    @classmethod
    @jwt_required_with_redirect(admin=True)
    def subject(cls, name: str):
        subject_ = SubjectModel.find_by_name(name, allow_none=True)
        if request.method == "POST":
            if subject_:
                return {"message": SUBJECT_ALREADY_EXIST.format(name)}, 400
            new_subject = SubjectModel(name=name)
            new_subject.save_to_db()
            return {"message": SUBJECT_ADDED.format(name)}, 201

        if request.method == "PUT":
            new_subject = subject_schema.load(request.json)
            if subject_:
                subject_.name = new_subject.name
                subject_.save_to_db()
                return {"message": SUBJECT_EDITED.format(name)}, 200
            new_subject.save_to_db()
            return {"message": SUBJECT_ADDED.format(new_subject.name)}, 201

        if request.method == "DELETE":
            if subject_ is None:
                return {"message": SUBJECT_DOESNT_EXIST.format(name)}, 400
            subject_.delete_from_db()
            return {"message": SUBJECT_DELETED.format(name)}, 200

        # request.method == "GET"
        if subject_ is None:
            return {"message": SUBJECT_DOESNT_EXIST.format(name)}, 400
        return subject_schema.dump(subject_), 200

    @classmethod
    @jwt_required_with_redirect(admin=True)
    def subjects(cls):
        return {"subjects": subject_schema.dump(SubjectModel.get_all(),
                                                many=True)}, 200
