from typing import Type, Union, List, Tuple

from flask import Flask, Response, request

from libs.factories import name_factory
from libs.jwt_functions import jwt_required_with_redirect
from ma import ma
from models.base_resource import BaseResourceModel, ResourceIdentifier
from routes.base_route import BaseRoute, request_logic
from routes.i_request import IRequestData, ResponseData, RequestData
from schemas.schema_context import SchemaContext


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
            identifier: ResourceIdentifier = None
    ):
        super().__init__(app, data, logic)
        self.template = template
        self.resource_url_name = resource_url_name
        self.resources_url_name = resources_url_name
        self.schema = schema
        self.identifier = identifier

        if self.resource_url_name is not None:
            app.add_url_rule(
                f"/{self.resource_url_name}/{self.identifier.type_str}",
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
            **kwargs,
    ) -> Union[Response, ResponseData]:
        identifier = self.identifier.new_value(kwargs[self.identifier.key])
        if request.method == "PUT":
            obj = self.logic.get_by_identifier(identifier, allow_none=True)
            if obj is not None:
                return self.create_response(
                    data,
                    202,
                    message=f"Resource {identifier.value} updated.",
                    resource=obj.update(data),
                )

        if request.method in ["POST", "PUT"]:
            return self.create_response(
                data,
                201,
                message=f"Resource {identifier.value} created.",
                resource=self.logic.create(
                    identifier,
                    data,
                )
            )

        if request.method == "DELETE":
            return self.create_response(
                data,
                202,
                message=f"Resource {identifier.value} deleted.",
                resource=self.logic.get_by_identifier(identifier).delete(),
            )

        # request.method == "GET"
        return self.create_response(
            data,
            200,
            resource=self.logic.get_by_identifier(identifier).read(),
        )

    @name_factory
    @jwt_required_with_redirect(admin=True)
    @request_logic
    def resources(
            self,
            data: RequestData,
    ) -> Union[Response, ResponseData]:
        return self.create_response(
            data,
            200,
            resource=self.logic.list(),
        )

    def create_response(
            self,
            data: RequestData,
            status_code: int = None,
            message: str = None,
            resource: Union[BaseResourceModel, List[BaseResourceModel]] = None
    ) -> ResponseData:
        resource_dict = self.create_resource_dict(data, resource)
        if message:
            resource_dict['message'] = message
        return ResponseData(
            template=self.template,
            resource=resource_dict,
            status_code=status_code,
        )

    def create_resource_dict(
            self,
            data: RequestData,
            resource: Union[BaseResourceModel, List[BaseResourceModel], None]
    ) -> dict:
        resource_dict = {}
        with SchemaContext(self.schema, data.context):
            if isinstance(resource, BaseResourceModel):
                resource_dict = self.schema.dump(resource)
            if isinstance(resource, list):
                resource_dict['list'] = self.schema.dump(resource, many=True)
            return resource_dict
