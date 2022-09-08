from typing import Type, Union

from flask import Flask, Response, request

from libs.factories import name_factory
from libs.jwt_functions import jwt_required_with_redirect
from ma import ma
from models.resource_mixin import BaseResourceModel
from routes.base_route import BaseRoute, request_logic
from routes.i_request import IRequestData, ResponseData, RequestData


class ResourceMixin(BaseRoute):

    logic: Type[BaseResourceModel]

    def __init__(
            self,
            app: Flask,
            data: Type[IRequestData],
            logic: Type[BaseResourceModel],
            schema: ma.Schema,
            resource_url_name: str = None,
            resources_url_name: str = None,
    ):
        super().__init__(app, data, logic)
        self.resource_url_name = resource_url_name
        self.resources_url_name = resources_url_name
        self.schema = schema

        if self.resource_url_name is not None:
            app.add_url_rule(
                f"/{self.resource_url_name}/<string:name>",
                view_func=self.resource(self.resource_url_name),
                methods=["GET", "POST", "PUT", "DELETE"],
            )
        if self.resources_url_name is not None:
            app.add_url_rule(
                f"/{self.resources_url_name}",
                view_func=self.resources(self.resources_url_name),
                # view_func=name_factory(self.resources,
                #                        self.resources_url_name),
                methods=["GET"],
            )

    @name_factory
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

    @name_factory
    @jwt_required_with_redirect(admin=True)
    @request_logic
    def resources(
            self,
            data: RequestData,
    ) -> Union[Response, ResponseData]:

        return ResponseData(
            resource={
                'list': self.schema.dump(self.logic.list(), many=True)
            }
        )
