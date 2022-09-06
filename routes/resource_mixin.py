from typing import Type, Union

from flask import Flask, Response, request

from db import db
from libs.jwt_functions import jwt_required_with_redirect
from ma import ma
from models.resource_mixin import ResourceMixinLogic
from routes.base_route import BaseRoute, request_logic
from routes.i_request import IRequestData, RequestPayload, ResponseData


class ResourceMixin(BaseRoute):

    logic: Type[ResourceMixinLogic]

    resource_url_name: str = None
    resources_url_name: str = None

    @classmethod
    def config(
            cls,
            app: Flask,
            data: Type[IRequestData],
            logic: Type[ResourceMixinLogic],
    ):
        super().config(app, data, logic)
        app.add_url_rule(
            f"/{cls.resource_url_name}/<string:name>",
            view_func=cls.resource,
            methods=["GET", "POST", "PUT", "DELETE"],
        )
        app.add_url_rule(
            f"/{cls.resources_url_name}",
            view_func=cls.resources,
            methods=["GET"],
        )

    @classmethod
    @jwt_required_with_redirect(admin=True)
    @request_logic
    def resource(
            cls,
            data: RequestPayload,
            name: str,
    ) -> Union[Response, ResponseData]:
        if request.method == "POST":
            return cls.logic.create(data, name)
        if request.method == "PUT":
            obj = cls.logic.get_by_name(name, allow_none=True)
            if obj is None:
                obj = cls.logic(name=name)
            return obj.update(data)
        if request.method == "DELETE":
            obj = cls.logic.get_by_name(name, allow_none=False)
            return obj.delete()
        # request.method == "GET"
        obj = cls.logic.get_by_name(name, allow_none=False)
        return obj.read()

    @classmethod
    @jwt_required_with_redirect(admin=True)
    @request_logic
    def resources(
            cls,
            data: RequestPayload,
    ) -> Union[Response, ResponseData]:
        return cls.logic.list()
