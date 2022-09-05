from typing import Union, Tuple

from flask import Response, request, jsonify, render_template
from flask_jwt_extended import get_jwt

from models import PersonModel
from routes.i_request import (
    IRequestData,
    RequestData,
    ResponseData,
)


class BaseRequestData(IRequestData):

    @classmethod
    def get_request_data(cls) -> RequestData:
        data = RequestData()
        data.update(cls.get_form_data())  # data from form
        data.update(cls.get_header_data())  # data from header
        data.update(cls.get_json_data())  # data from json body
        data.update(cls.get_cookies_data())  # data from cookies
        data.update(cls.get_jwt_data())  # data from jwt token
        return data

    @classmethod
    def serialize_response(
            cls,
            data: RequestData,
            response_data: ResponseData,
    ) -> Union[Tuple[Response, int], str]:
        if data["content_type"] == "application/json":
            return cls.prepare_json_response(response_data)
        return cls.prepare_html_response(data, response_data)

    @classmethod
    def get_form_data(cls):
        return request.form

    @classmethod
    def get_header_data(cls):
        return {"content_type": request.content_type}

    @classmethod
    def get_json_data(cls):
        if request.content_type == "application/json":
            return request.json
        return {}

    @classmethod
    def get_cookies_data(cls):
        return request.cookies

    @classmethod
    def get_jwt_data(cls):
        jwt_data = get_jwt()
        needed_keys = jwt_data.keys() & {'csrf', 'admin', 'scope'}
        return {'jwt_' + key: jwt_data[key] for key in needed_keys}

    @classmethod
    def prepare_common_data(cls, data: RequestData):
        common_data = {"csrf_token": data.get("jwt_csrf")}
        if data.get("jwt_admin"):
            common_data.update(
                {
                    "persons": PersonModel.get_all(),
                    "admin": data.get("jwt_admin"),
                }
            )
        return common_data

    @classmethod
    def prepare_json_response(cls, response_data: ResponseData):
        status_code = response_data.kwargs.get("status_code", 200)
        return jsonify(response_data.resource), status_code

    @classmethod
    def prepare_html_response(
            cls,
            data: RequestData,
            response_data: ResponseData
    ) -> str:
        common_data = cls.prepare_common_data(data)

        return render_template(
            response_data.template,
            resource=jsonify(response_data.resource),
            **common_data,
            **response_data.kwargs,
        )
