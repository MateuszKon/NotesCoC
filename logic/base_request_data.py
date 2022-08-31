from typing import Union

from flask import Response, request
from flask_jwt_extended import get_jwt

from logic.interfaces.i_request_data import IRequestDataHandler


class RequestData(IRequestDataHandler):

    @classmethod
    def get_request_data(cls) -> dict:
        data = {'jwt_'+key: data for key, data in get_jwt().items()}
        data.update(request.form)
        if request.content_type == "application/json":
            data.update(request.json)
        data.update(request.cookies)
        return data

    @classmethod
    def prepare_response(
            cls,
            template: str = None,
            **kwargs
    ) -> Union[Response, str]:
        pass