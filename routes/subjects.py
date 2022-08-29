from libs.jwt_functions import jwt_required_with_redirect
from models.subjects import SubjectModel
from schemas.subjects import SubjectSchema

subject_schema = SubjectSchema()


class SubjectRoutes:

    @classmethod
    @jwt_required_with_redirect(admin=True)
    def subjects(cls):
        return {"subjects": subject_schema.dump(SubjectModel.get_all(),
                                                many=True)}, 200
