from functools import wraps
from typing import Type, Union

from flask import Flask, Response

from NotesApp.routes.i_request import IRequestData, IRequestLogic, ResponseData


class BaseRoute:

    def __init__(
            self,
            app: Flask,
            data: Type[IRequestData],
            logic: Type[IRequestLogic],
    ):
        self.data = data
        self.logic = logic


def request_logic(fun):
    @wraps(fun)
    def wrapper(self: BaseRoute, *args, **kwargs):
        data = self.data.get_request_data()

        result: Union[Response, ResponseData] = fun(self, data, *args, **kwargs)

        if isinstance(result, ResponseData):
            return self.data.serialize_response(data.context, result)
        return result

    return wrapper
