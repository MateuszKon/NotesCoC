import logging
from typing import Type, Union, List

from flask import Flask, Response, request, url_for
from wtforms import Form
from wtforms.form import BaseForm
from wtforms_alchemy import ModelForm

from config import log_access
from libs.factories import name_factory
from libs.jwt_functions import jwt_required_with_redirect, \
    access_denied_response
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
    @jwt_required_with_redirect()
    @request_logic
    def resource(
            self,
            data: RequestData,
            **kwargs,
    ) -> Union[Response, ResponseData]:
        identifier = self.identifier.new_value(kwargs[self.identifier.key])
        level = logging.INFO if request.method == "GET" else logging.WARNING
        log_access(level, data, **identifier.dict)
        if request.method in ["PUT", "POST", "DELETE"] \
                and not data.context.admin:
            return access_denied_response()
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
                resource=self.logic.get_by_identifier(identifier).delete(data),
            )

        # request.method == "GET"
        return self.create_response(
            data,
            200,
            resource=self.logic.get_by_identifier(identifier).read(data),
        )

    @name_factory
    @jwt_required_with_redirect()
    @request_logic
    def resources(
            self,
            data: RequestData,
    ) -> Union[Response, ResponseData]:
        log_access(logging.INFO, data)
        return self.create_response(
            data,
            200,
            resource=self.logic.list(data),
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


class BaseResourceRouteForm(BaseResourceRoute):

    def __init__(
            self,
            app: Flask,
            data: Type[IRequestData],
            logic: Type[BaseResourceModel],
            schema: ma.Schema,
            template: str = 'base_resource.html',
            resource_url_name: str = None,
            resources_url_name: str = None,
            identifier: ResourceIdentifier = None,
            form: ModelForm = None,
            form_template: str = 'form_resource.html',
    ):
        super().__init__(
            app,
            data,
            logic,
            schema,
            template,
            resource_url_name,
            resources_url_name,
            identifier,
        )
        self.form = form
        self.form_template = form_template
        if self.form is not None:
            app.add_url_rule(
                f"/form/{self.resource_url_name}",
                view_func=self.form_view(f"{self.resource_url_name}_form"),
                methods=["GET", "POST"],
            )

    @name_factory
    @jwt_required_with_redirect(admin=True)
    @request_logic
    def form_view(
            self,
            data: RequestData,
    ) -> Union[Response, ResponseData]:
        log_access(logging.WARNING, data)
        form: ModelForm = self.form(data.form)
        if data.context.method == "POST" and form.validate():
            return self.save_resource(form)
        return ResponseData(
            self.form_template,
            form=form,
            title=self.resource_url_name,
        )

    def save_resource(self, form: ModelForm) -> ResponseData:
        resource = self.logic()
        form.populate_obj(resource)
        resource.save_to_db()
        return ResponseData(
            redirect=url_for('home'),
            status_code=201,
            resource={"message": f"Zapisano {self.resource_url_name}"}
        )

