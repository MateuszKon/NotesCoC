from typing import Union, Tuple

from flask import Response, request, jsonify, render_template
from flask_jwt_extended import get_jwt

from routes.i_request import (
    IRequestData,
    RequestData,
    ResponseData,
    RequestHiddenData,
)


class BaseRequestData(IRequestData):

    @classmethod
    def get_request_data(cls) -> Tuple[RequestData, RequestHiddenData]:
        request_data = RequestData(
            {'jwt_' + key: data for key, data in get_jwt().items()}
        )
        request_data.update(request.form)
        request_data["content_type"] = request.content_type
        if request_data["content_type"] == "application/json":
            request_data.update(request.json)
        request_data.update(request.cookies)
        print(request_data)
        # hidden_data =

        return request_data

    @classmethod
    def serialize_response(
            cls,
            data: RequestData,
            response_data: ResponseData,
    ) -> Union[Tuple[Response, int], str]:
        status_code = response_data.kwargs.get("status_code", 200)
        if data["content_type"] == "application/json":
            return jsonify(response_data.requested_data), status_code
        return render_template(
            response_data.template,
            **response_data.requested_data,
            **response_data.kwargs,
        )
