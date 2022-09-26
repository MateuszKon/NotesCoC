from abc import abstractmethod
from typing import Type, Union

from flask import request, Flask, Response

from libs.jwt_functions import jwt_required_with_redirect
from models.users import UserModel
from routes.base_route import BaseRoute, request_logic
from routes.i_request import IRequestLogic, IRequestData, RequestData, \
    ResponseData
from schemas.users import UserSchema

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
        return self.logic.list(data)


class IUserLoginRouteLogic(IRequestLogic):

    @classmethod
    @abstractmethod
    def render_login(
            cls,
            data: RequestData,
    ) -> Union[Response, ResponseData]:
        pass

    @classmethod
    @abstractmethod
    def login_user(
            cls,
            data: RequestData,
    ) -> Union[Response, ResponseData]:
        pass

    @classmethod
    @abstractmethod
    def logout_user(
            cls,
            data: RequestData,
    ) -> Union[Response, ResponseData]:
        pass


class UserLogin(BaseRoute):
    logic: Type[IUserLoginRouteLogic]

    def __init__(
            self,
            app: Flask,
            data: Type[IRequestData],
            logic: Type[IUserLoginRouteLogic],
    ):
        super().__init__(app, data, logic)
        app.add_url_rule("/login",
                         view_func=self.login_user,
                         methods=["GET", "POST"],
                         )
        app.add_url_rule("/logout",
                         view_func=self.logout_user,
                         methods=["POST"],
                         )

    @request_logic
    def login_user(
            self,
            data: RequestData,
    ):
        if request.method == "POST":
            return self.logic.login_user(data)
        return self.logic.render_login(data)

    @jwt_required_with_redirect()
    @request_logic
    def logout_user(
            self,
            data: RequestData,
    ):
        return self.logic.logout_user(data)


class User:

    @classmethod
    @jwt_required_with_redirect(admin=True)
    def get_all(cls):
        return {'users': user_schema.dump(
            UserModel.get_all(),
            many=True
        )}
