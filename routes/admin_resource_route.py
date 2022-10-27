import logging
from typing import Union, Type, Callable

from flask import Response, Flask

from config import log_access
from libs.factories import name_factory
from libs.jwt_functions import jwt_required_with_redirect
from ma import ma
from models.base_resource import BaseResourceModel, ResourceIdentifier
from routes.base_resource import BaseResourceRoute
from routes.base_route import request_logic
from routes.i_request import RequestData, ResponseData, IRequestData


class AdminResourceRoute(BaseResourceRoute):

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
        self._super_resource: Callable = super().resource(f'_{resource_url_name}')
        self._super_resources: Callable = super().resources(f'_{resources_url_name}')
        super().__init__(app, data, logic, schema, template, resource_url_name, resources_url_name,
                         identifier)

    @name_factory
    @jwt_required_with_redirect(admin=True)
    @request_logic
    def resource(
            self,
            data: RequestData,
            **kwargs,
    ) -> Union[Response, ResponseData]:
        log_access(logging.WARNING, data)
        return self._super_resource(**kwargs)

    @name_factory
    @jwt_required_with_redirect(admin=True)
    @request_logic
    def resources(
            self,
            data: RequestData,
    ) -> Union[Response, ResponseData]:
        log_access(logging.WARNING, data)
        return self._super_resources()
