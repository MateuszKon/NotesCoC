from typing import Union

from flask import Response, url_for

from database.models.base_resource import ResourceIdentifier
from database.models.users import RegisterUserModel, UserModel
from NotesApp.routes.i_request import RequestData, ResponseData
from NotesApp.routes.users import IUserRegisterRouteLogic
from NotesApp.schemas.users import RegisterUserSchema

USERNAME_EXIST_ERROR = "Username with name {} already exist!"

register_user_schema = RegisterUserSchema()


class UserRegisterLogic(IUserRegisterRouteLogic):

    @classmethod
    def confirm_registration(
            cls,
            data: RequestData,
            registration_hash: str
    ) -> Union[Response, ResponseData]:
        identifier = ResourceIdentifier("hash", "string", registration_hash)
        register_user = RegisterUserModel.get_by_identifier(identifier)

        username = data.data.get("username")
        password = data.data.get("new-password")

        if UserModel.get_by_login(username):
            return ResponseData(
                resource={
                    "message": USERNAME_EXIST_ERROR.format(username)
                },
                status_code=400,
                redirect=url_for(
                    'register_user',
                    registration_hash=registration_hash
                ),
            )

        new_user = UserModel(username, password, register_user.person_name)
        new_user.save_to_db()
        register_user.delete_from_db()

        return ResponseData(
            resource={
                "message": "Registration complete!"
            },
            status_code=201,
            redirect=url_for('login_user'),
        )

    @classmethod
    def render_registration_form(
            cls,
            data: RequestData,
            registration_hash: str
    ) -> Union[Response, ResponseData]:
        identifier = ResourceIdentifier("hash", "string", registration_hash)
        register_user = RegisterUserModel.get_by_identifier(identifier)
        return ResponseData(
            template='register.html',
            resource=register_user_schema.dump(register_user)
        )

    @classmethod
    def add_registration_record(
            cls,
            data: RequestData
    ) -> Union[Response, ResponseData]:
        user_register = RegisterUserModel(
            person_name=data.data.get("person_name")
        )
        user_register.save_to_db()
        return ResponseData(
            resource=register_user_schema.dump(user_register),
            status_code=201
        )

    @classmethod
    def list(
            cls,
            data: RequestData,
    ) -> Union[Response, ResponseData]:
        return ResponseData(
            resource={"list": register_user_schema.dump(
                RegisterUserModel.list(data),
                many=True,
            )},
            status_code=200,
        )
