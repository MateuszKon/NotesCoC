from abc import abstractmethod
from typing import Type, Union

from flask import request, render_template, make_response, redirect, jsonify, \
    url_for, Flask, Response
from flask_jwt_extended import set_access_cookies, get_jwt

from blocklist import add_to_blocklist
from libs.jwt_functions import jwt_required_with_redirect
from models.users import UserModel
from routes.base_route import BaseRoute, request_logic
from routes.i_request import IRequestLogic, IRequestData, RequestData, \
    ResponseData
from schemas.users import UserSchema

INVALID_REGISTRATION_HASH = "Invalid registration hash!"
INVALID_CREDENTIALS = "Invalid username or password!"
USERNAME_EXIST_ERROR = "Username with name {} already exist!"

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
    def list(
            cls,
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
        app.add_url_rule("/register/form/<string:registration_hash>",
                         view_func=self.register_user,
                         methods=["GET", "POST"],
                         )
        app.add_url_rule("/register/new",
                         view_func=self.add_registration_record,
                         methods=["POST"],
                         )
        app.add_url_rule("/register/get_all",
                         view_func=self.get_registration_records,
                         )

    @request_logic
    def register_user(
            self,
            data: RequestData,
            registration_hash: str
    ):
        if request.method == "POST":
            return self.logic.confirm_registration(data, registration_hash)

        # request.method == "GET"
        return self.logic.render_registration_form(data, registration_hash)

    @jwt_required_with_redirect(admin=True)
    @request_logic
    def add_registration_record(
            self,
            data: RequestData,
    ):
        return self.logic.add_registration_record(data)

    @jwt_required_with_redirect(admin=True)
    @request_logic
    def get_registration_records(
            self,
            data: RequestData,
    ):
        return self.logic.list()


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
