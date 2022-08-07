from flask import request

from models.users import RegisterUser
from schemas.users import RegisterUserSchema

register_user_schema = RegisterUserSchema()
register_user_schemas = RegisterUserSchema(many=True)


class UserRegister:

    @classmethod
    def register_user(cls, registration_hash: str):
        pass

    @classmethod
    def add_registration_record(cls):
        print(request.json)
        user_register: RegisterUser = register_user_schema.load(request.json)
        user_register.save_to_db()
        print(user_register)
        return register_user_schema.dump(user_register), 200
        # return {"message": "OK"}, 201

    @classmethod
    def get_registration_records(cls):
        return {"registers": register_user_schema.dump(
            RegisterUser.get_all(),
            many=True
        )}, 200

