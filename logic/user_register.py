from typing import Union

from flask import Response

from routes.i_request import RequestData, ResponseData
from routes.users import IUserRegisterRouteLogic


class UserRegisterLogic(IUserRegisterRouteLogic):

    @classmethod
    def confirm_registration(cls, data: RequestData, registration_hash: str) -> \
    Union[Response, ResponseData]:
        pass

    @classmethod
    def render_registration_form(cls, data: RequestData,
                                 registration_hash: str) -> Union[
        Response, ResponseData]:
        pass

    @classmethod
    def add_registration_record(cls, data: RequestData) -> Union[
        Response, ResponseData]:
        pass

    @classmethod
    def get_all(cls, data: RequestData) -> Union[Response, ResponseData]:
        pass

