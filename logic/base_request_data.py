from typing import Union, Tuple

from flask import Response, redirect, request, jsonify, render_template, \
    make_response, flash
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
        data.update(cls.get_args_data())  # data from args (url)
        data.update(cls.get_form_data())  # data from form
        data.update(cls.get_json_data())  # data from json body

        context_data = ContextData()
        context_data.update(cls.get_header_data())  # data from header
        context_data.update(cls.get_cookies_data())  # data from cookies
        context_data.update(cls.get_jwt_data())  # data from jwt token
        return RequestData(data, context_data, cls.get_form_data())

    @classmethod
    def serialize_response(
            cls,
            context_data: ContextData,
            response_data: ResponseData,
    ) -> Union[Tuple[Response, int], str, Response]:
        if context_data["accept"] == "application/json":
            return cls.prepare_json_response(response_data)
        if isinstance(response_data.resource, dict) \
                and response_data.resource.get('message'):
            message = response_data.resource.pop('message')
            flash(message)
        if response_data.is_redirect:
            return cls.prepare_redirect_response(context_data, response_data)
        return cls.prepare_html_response(context_data, response_data)

    @classmethod
    def get_args_data(cls):
        return request.args

    @classmethod
    def get_form_data(cls):
        return request.form

    @classmethod
    def get_header_data(cls):
        return {
            "content_type": request.content_type,
            "accept": request.accept_mimetypes.best,
            "args": request.args,
            "method": request.method,
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
        try:
            jwt_data = get_jwt()
        except RuntimeError:
            jwt_data = {}
        needed_keys = jwt_data.keys() & {'csrf', 'admin', 'scope', 'jti',
                                         'exp', 'sub'}
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
    ) -> Response:
        common_data = cls.prepare_common_data(context_data)
        response = make_response(render_template(
            response_data.template,
            resource=response_data.resource,
            **common_data,
            **response_data.kwargs,
        ))
        response = cls._set_cookies(response, response_data)
        return response

    @classmethod
    def prepare_redirect_response(
            cls,
            context_data,
            response_data
    ) -> Response:
        response = make_response(redirect(
            response_data.kwargs['redirect']
        ))
        response = cls._set_cookies(response, response_data)
        return response

    @classmethod
    def _set_cookies(
            cls,
            response: Response,
            response_data: ResponseData) -> Response:
        for cookie in response_data.cookies:
            response = cookie.set_cookie(response)
        return response
