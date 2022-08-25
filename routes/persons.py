from flask import request

from libs.jwt_functions import jwt_required_with_redirect
from models.persons import PersonModel
from schemas.persons import PersonSchema


PERSON_ALREADY_EXIST = "Person {} already exist!"
PERSON_ADDED = "Person {} added."
PERSON_EDITED = "Person {} edited."
PERSON_DOESNT_EXIST = "Person {} doesn't exist!"
PERSON_DELETED = "Person {} deleted."


person_schema = PersonSchema()


class PersonRoutes:

    @classmethod
    @jwt_required_with_redirect(admin=True)
    def person(cls, name: str):
        person_ = PersonModel.find_by_name(name, allow_none=True)
        if request.method == "POST":
            if person_:
                return {"message": PERSON_ALREADY_EXIST.format(name)}, 400
            new_person = PersonModel(name=name)
            new_person.save_to_db()
            return {"message": PERSON_ADDED.format(name)}, 201

        if request.method == "PUT":
            new_person = person_schema.load(request.json)
            if person_:
                person_.name = new_person.name
                person_.save_to_db()
                return {"message": PERSON_EDITED.format(name)}, 200
            new_person.save_to_db()
            return {"message": PERSON_ADDED.format(new_person.name)}, 201

        if request.method == "DELETE":
            if person_ is None:
                return {"message": PERSON_DOESNT_EXIST.format(name)}, 400
            person_.delete_from_db()
            return {"message": PERSON_DELETED.format(name)}, 200

        # request.method == "GET"
        if person_ is None:
            return {"message": PERSON_DOESNT_EXIST.format(name)}, 400
        return person_schema.dump(person_), 200

    @classmethod
    @jwt_required_with_redirect(admin=True)
    def persons(cls):
        return {"persons": person_schema.dump(PersonModel.get_all(),
                                              many=True)}, 200
