from typing import Type, Union, List

from flask import Flask, Response, request

from libs.factories import name_factory
from libs.jwt_functions import jwt_required_with_redirect
from ma import ma
from models.baser_resource import BaseResourceModel
from routes.base_route import BaseRoute, request_logic
from routes.i_request import IRequestData, ResponseData, RequestData


class BaseResourceRoute(BaseRoute):

    logic: Type[BaseResourceModel]

    def __init__(
            self,
            app: Flask,
            data: Type[IRequestData],
            logic: Type[BaseResourceModel],
            schema: ma.Schema,
            template: str = 'base_resource.html',
            resource_url_name: str = None,
            resources_url_name: str = None,
    ):
        super().__init__(app, data, logic)
        self.template = template
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
        if request.method == "PUT":
            obj = self.logic.get_by_name(name, allow_none=True)
            if obj is not None:
                return self._create_response(
                    202,
                    message=f"Resource {name} updated.",
                    resource=obj.update(data),
                )

        if request.method in ["POST", "PUT"]:
            return self._create_response(
                201,
                message=f"Resource {name} created.",
                resource=self.logic.create(data, name),
            )

        if request.method == "DELETE":
            return self._create_response(
                202,
                message=f"Resource {name} deleted.",
                resource=self.logic.get_by_name(name).delete(),
            )

        # request.method == "GET"
        return self._create_response(
            200,
            resource=self.logic.get_by_name(name).read(),
        )

    @name_factory
    @jwt_required_with_redirect(admin=True)
    @request_logic
    def resources(
            self,
            data: RequestData,
    ) -> Union[Response, ResponseData]:
        return self._create_response(
            200,
            resource=self.logic.list()
        )

    def _create_response(
            self,
            status_code: int = None,
            message: str = None,
            resource: Union[BaseResourceModel, List[BaseResourceModel]] = None
    ) -> ResponseData:
        resource_dict = self._create_resource_dict(resource)
        if message:
            resource_dict['message'] = message
        return ResponseData(
            template=self.template,
            resource=resource_dict,
            status_code=status_code,
        )

    def _create_resource_dict(
            self,
            resource: Union[BaseResourceModel, List[BaseResourceModel], None]
    ) -> dict:
        resource_dict = {}
        if isinstance(resource, BaseResourceModel):
            resource_dict = self.schema.dump(resource)
        if isinstance(resource, list):
            resource_dict['list'] = self.schema.dump(resource, many=True)
        return resource_dict
