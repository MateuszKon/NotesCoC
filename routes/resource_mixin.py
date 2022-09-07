from typing import Type, Union

from flask import Flask, Response, request

from db import db
from libs.jwt_functions import jwt_required_with_redirect
from ma import ma
from models.resource_mixin import ResourceMixinLogic
from routes.base_route import BaseRoute, request_logic
from routes.i_request import IRequestData, RequestPayload, ResponseData, \
    RequestData


class ResourceMixin(BaseRoute):

    logic: Type[ResourceMixinLogic]

    resource_url_name: str = None
    resources_url_name: str = None

    def __init__(
            self,
            app: Flask,
            data: Type[IRequestData],
            logic: Type[ResourceMixinLogic],
    ):
        super().__init__(app, data, logic)
        app.add_url_rule(
            f"/{self.resource_url_name}/<string:name>",
            view_func=self.resource,
            methods=["GET", "POST", "PUT", "DELETE"],
        )
        app.add_url_rule(
            f"/{self.resources_url_name}",
            view_func=self.resources,
            methods=["GET"],
        )

    @jwt_required_with_redirect(admin=True)
    @request_logic
    def resource(
            self,
            data: RequestData,
            name: str,
    ) -> Union[Response, ResponseData]:
        if request.method == "POST":
            return self.logic.create(data, name)
        if request.method == "PUT":
            obj = self.logic.get_by_name(name, allow_none=True)
            if obj is None:
                obj = self.logic(name=name)
            return obj.update(data)
        if request.method == "DELETE":
            obj = self.logic.get_by_name(name, allow_none=False)
            return obj.delete()
        # request.method == "GET"
        obj = self.logic.get_by_name(name, allow_none=False)
        return obj.read()

    @jwt_required_with_redirect(admin=True)
    @request_logic
    def resources(
            self,
            data: RequestData,
    ) -> Union[Response, ResponseData]:
        return self.logic.list()
