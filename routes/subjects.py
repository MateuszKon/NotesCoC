from typing import Type, Union, List

from flask import request, Flask, Response

from libs.factories import name_factory
from libs.jwt_functions import jwt_required_with_redirect
from ma import ma
from models.base_resource import ResourceIdentifier, BaseResourceModel
from models.subjects import SubjectModel
from routes.base_resource import BaseResourceRoute
from routes.base_route import request_logic
from routes.i_request import IRequestData, RequestData, ResponseData
from schemas.schema_context import SchemaContext


class SubjectRoutes(BaseResourceRoute):

    logic: Type[SubjectModel]

    def __init__(
            self,
            app: Flask,
            data: Type[IRequestData],
            logic: Type[SubjectModel],
            schema: ma.Schema,
            child_schema: ma.Schema,
            template: str = 'base_resource.html',
            resource_url_name: str = 'subject',
            resources_url_name: str = 'subjects',
            identifier: ResourceIdentifier = None,
    ):
        super().__init__(app, data, logic, schema, template,
                         resource_url_name, resources_url_name, identifier)
        self.child_schema = child_schema
        app.add_url_rule(
            f"/{self.resource_url_name}/<string:name>/category",
            view_func=self.category_of_subject(
                self.resource_url_name + 's_category'
            ),
            methods=["POST", "PUT", "DELETE"],
        )
        app.add_url_rule(
            f"/{self.resource_url_name}/<string:name>/categories",
            view_func=self.categories_of_subject(
                self.resource_url_name + 's_categories'
            ),
            methods=["GET"],
        )

    @name_factory
    @jwt_required_with_redirect(admin=True)
    @request_logic
    def category_of_subject(
        self,
        data: RequestData,
        name: str
    ) -> Union[Response, ResponseData]:
        subject = self.logic.find_by_name(name)
        categories = self.child_schema.load(data.data['subject_categories'], many=True)

        if request.method == "POST":
            subject.remove_categories(subject.categories.all())
            subject.add_categories(categories)
            subject.save_to_db()
            return self.create_response(
                data,
                201,
                message=f"Categories set for subject {name}",
                resource=subject,
            )

        if request.method == "PUT":
            subject.add_categories(categories)
            subject.save_to_db()
            return self.create_response(
                data,
                201,
                message=f"Categories added for subject {name}",
                resource=subject,
            )

        if request.method == "DELETE":
            subject.remove_categories(categories)
            subject.save_to_db()
            return self.create_response(
                data,
                201,
                message=f"Categories deleted from subject {name}",
                resource=subject,
            )

    @name_factory
    @jwt_required_with_redirect(admin=True)
    @request_logic
    def categories_of_subject(
            self,
            data: RequestData,
            name: str
    ) -> Union[Response, ResponseData]:
        subject = SubjectModel.find_by_name(name)
        return self.create_response(
            data,
            200,
            resource=subject.categories.all()
        )

    def create_resource_dict(
            self,
            data: RequestData,
            resource: Union[BaseResourceModel, List[BaseResourceModel], None]
    ) -> dict:
        if isinstance(resource, SubjectModel) or (
                isinstance(resource, list) and
                isinstance(resource[0], SubjectModel)
        ):
            return super().create_resource_dict(data, resource)

        resource_dict = {}
        with SchemaContext(self.child_schema, data.context):
            if isinstance(resource, BaseResourceModel):
                resource_dict = self.child_schema.dump(resource)
            if isinstance(resource, list):
                resource_dict['list'] = self.child_schema.dump(
                    resource,
                    many=True
                )
            return resource_dict