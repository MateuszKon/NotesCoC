from functools import wraps
from typing import Type, Union

from flask import Flask, Response

from routes.i_request import IRequestData, IRequestLogic, ResponseData


class BaseRoute:

    data:  Type[IRequestData] = None
    logic: Type[IRequestLogic] = None

    @classmethod
    def config(
            cls,
            app: Flask,
            data: Type[IRequestData],
            logic: Type[IRequestLogic],
    ):
        cls.data = data
        cls.logic = logic


def request_logic(fun):
    @wraps(fun)
    def wrapper(cls: Type[BaseRoute], *args, **kwargs):
        data = cls.data.get_request_data()

        result: Union[Response, ResponseData] = fun(cls, data, *args, **kwargs)

        if isinstance(result, ResponseData):
            return cls.data.serialize_response(data, result)
        return result

    return wrapper
