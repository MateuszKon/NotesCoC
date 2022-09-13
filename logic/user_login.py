from typing import Union

from flask import Response, url_for
from flask_jwt_extended import set_access_cookies

from blocklist import add_to_blocklist
from models import UserModel
from models.base_resource import ResourceIdentifier
from routes.i_request import RequestData, ResponseData, Cookie
from routes.users import IUserLoginRouteLogic


class AccessCookie(Cookie):

    def set_cookie(self, response: Response) -> Response:
        set_access_cookies(response, self.value)
        return response


class UserLoginLogic(IUserLoginRouteLogic):

    @classmethod
    def render_login(cls, data: RequestData) -> Union[Response, ResponseData]:
        return ResponseData(
            template='login.html',
            next=data.data.get('next', None)
        )

    @classmethod
    def login_user(cls, data: RequestData) -> Union[Response, ResponseData]:
        username = data.data['username']
        password = data.data['current-password']

        user_obj = UserModel.get_by_identifier(
            ResourceIdentifier('login', 'string', username)
        )
        if user_obj and password and user_obj.check_password(password):
            access_token = user_obj.create_authorisation_tokens()
            return ResponseData(
                resource={
                    'access_token': access_token,
                    'message': "User logged in."
                },
                redirect=data.context['args'].get('next', url_for('home')),
                cookies=[AccessCookie('access_token', access_token)]
            )

    @classmethod
    def logout_user(cls, data: RequestData) -> Union[Response, ResponseData]:
        access_jti = data.context["jwt_jti"]
        access_exp = data.context["jwt_exp"]
        add_to_blocklist(access_jti, access_exp)
        return ResponseData(
            resource={'message': "User logged out"},
            redirect=url_for('login_user'),
        )