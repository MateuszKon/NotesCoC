from abc import abstractmethod
from typing import Type, Union

from flask import request, render_template, make_response, redirect, jsonify, \
    url_for, Flask, Response
from flask_jwt_extended import set_access_cookies, get_jwt

from blocklist import add_to_blocklist
from libs.jwt_functions import jwt_required_with_redirect
from models.users import RegisterUserModel, UserModel
from routes.base_route import BaseRoute
from routes.i_request import IRequestLogic, IRequestData, RequestData, \
    ResponseData
from schemas.users import UserSchema, RegisterUserSchema

INVALID_REGISTRATION_HASH = "Invalid registration hash!"
INVALID_CREDENTIALS = "Invalid username or password!"
USERNAME_EXIST_ERROR = "Username with name {} already exist!"

register_user_schema = RegisterUserSchema()
user_schema = UserSchema()


class IUserRegisterRouteLogic(IRequestLogic):

    @classmethod
    @abstractmethod
    def confirm_registration(
            cls,
            data: RequestData,
            registration_hash: str,
    ) -> Union[Response, ResponseData]:
        pass

    @classmethod
    @abstractmethod
    def render_registration_form(
            cls,
            data: RequestData,
            registration_hash: str,
    ) -> Union[Response, ResponseData]:
        pass

    @classmethod
    @abstractmethod
    def add_registration_record(
            cls,
            data: RequestData,
    ) -> Union[Response, ResponseData]:
        pass

    @classmethod
    @abstractmethod
    def get_all(
            cls,
            data: RequestData,
    ) -> Union[Response, ResponseData]:
        pass


class UserRegister(BaseRoute):

    logic: Type[IUserRegisterRouteLogic]

    def __init__(
            self,
            app: Flask,
            data: Type[IRequestData],
            logic: Type[IUserRegisterRouteLogic],
    ):
        super().__init__(app, data, logic)
        app.add_url_rule(
            "/new_note",
            view_func=self.edit_note,
            methods=["GET", "POST"],
        )
        app.add_url_rule(
            "/note/<int:note_id>/edit",
            view_func=self.edit_note,
            methods=["GET", "POST"],
        )
        app.add_url_rule(
            "/note/<int:note_id>/delete",
            view_func=self.delete_note,
            methods=["GET", "POST", "DELETE"],
        )

    @classmethod
    def register_user(cls, registration_hash: str):
        register_user = RegisterUserModel.get_by_hash(registration_hash)
        if register_user is None:
            return {"message": INVALID_REGISTRATION_HASH}, 404
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["new-password"]
            if UserModel.get_by_login(username):
                return {"message": USERNAME_EXIST_ERROR.format(username)}, 400
            new_user = UserModel(username, password, register_user.person_name)
            new_user.save_to_db()
            register_user.delete_from_db()
            return {"message": "Registration complete!"}, 201
        return render_template(
            'register.html',
            person_name=register_user.person_name,
            register_hash=registration_hash,
        )

    @classmethod
    @jwt_required_with_redirect(admin=True)
    def add_registration_record(cls):
        user_register: RegisterUserModel = register_user_schema.load(request.json)
        user_register.save_to_db()
        return register_user_schema.dump(user_register), 201

    @classmethod
    @jwt_required_with_redirect(admin=True)
    def get_registration_records(cls):
        return {"registers": register_user_schema.dump(
            RegisterUserModel.get_all(),
            many=True
        )}, 200


class UserLogin(BaseRoute):

    @classmethod
    def login_user(cls):
        if request.method == "POST":
            content_type = request.headers.get("Content-Type")

            username, password = cls._get_credentials(content_type)

            user_obj = UserModel.get_by_login(username)
            if user_obj and password and user_obj.check_password(password):
                access_token = user_obj.create_authorisation_tokens()
                return cls._prepare_login_response(access_token, content_type)
            return {"message": INVALID_CREDENTIALS}, 404

        return render_template(
            'login.html',
            next=request.args.get('next', None),
        )

    @classmethod
    @jwt_required_with_redirect()
    def logout_user(cls):
        if request.method == "POST":
            jwt_data = get_jwt()
            access_jti = jwt_data["jti"]
            access_exp = jwt_data["exp"]
            add_to_blocklist(access_jti, access_exp)
            return redirect(url_for("login_user"))

    @classmethod
    def _get_credentials(cls, content_type):
        if content_type == "application/json":
            username = request.json["username"]
            password = request.json["current-password"]
        else:
            username = request.form["username"]
            password = request.form["current-password"]
        return username, password

    @classmethod
    def _prepare_login_response(cls, access_token, content_type):
        if content_type == "application/json":
            return jsonify({"access_token": access_token}), 200

        response = make_response(redirect(request.args.get('next', '/home')))
        set_access_cookies(response, access_token)
        return response


class User:

    @classmethod
    @jwt_required_with_redirect(admin=True)
    def get_all(cls):
        return {'users': user_schema.dump(
            UserModel.get_all(),
            many=True
        )}
