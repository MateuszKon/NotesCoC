from typing import Union, Tuple

from flask import Response, request, jsonify, render_template
from flask_jwt_extended import get_jwt

from models import PersonModel
from routes.i_request import (
    IRequestData,
    RequestPayload,
    ResponseData, ContextData, RequestData,
)


class BaseRequestData(IRequestData):

    @classmethod
    def get_request_data(cls) -> RequestData:
        data = RequestPayload()
        data.update(cls.get_form_data())  # data from form
        data.update(cls.get_json_data())  # data from json body

        context_data = ContextData()
        context_data.update(cls.get_header_data())  # data from header
        context_data.update(cls.get_cookies_data())  # data from cookies
        context_data.update(cls.get_jwt_data())  # data from jwt token
        return RequestData(data, context_data)

    @classmethod
    def serialize_response(
            cls,
            context_data: ContextData,
            response_data: ResponseData,
    ) -> Union[Tuple[Response, int], str]:
        if context_data["accept"] == "application/json":
            return cls.prepare_json_response(response_data)
        print(response_data.resource)
        return cls.prepare_html_response(context_data, response_data)

    @classmethod
    def get_form_data(cls):
        return request.form

    @classmethod
    def get_header_data(cls):
        return {
            "content_type": request.content_type,
            "accept": request.accept_mimetypes.best,
        }

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
    def prepare_common_data(cls, context_data: ContextData):
        common_data = {"csrf_token": context_data.get("jwt_csrf")}
        if context_data.get("jwt_admin"):
            common_data.update(
                {
                    "persons": PersonModel.get_all(),
                    "admin": context_data.get("jwt_admin"),
                }
            )
        return common_data

    @classmethod
    def prepare_json_response(cls, response_data: ResponseData):
        status_code = response_data.status_code or 200
        return jsonify(response_data.resource), status_code

    @classmethod
    def prepare_html_response(
            cls,
            context_data: ContextData,
            response_data: ResponseData
    ) -> str:
        common_data = cls.prepare_common_data(context_data)

        return render_template(
            response_data.template,
            resource=response_data.resource,
            **common_data,
            **response_data.kwargs,
        )
