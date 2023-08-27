import logging
from typing import Type, Union, List

from flask import request, Flask, Response
from wtforms_alchemy import ModelForm

from NotesApp.config import log_access
from NotesApp.forms.subjects import SubjectForm
from libs.factories import name_factory
from libs.jwt_functions import jwt_required_with_redirect
from NotesApp.ma import ma
from database.models import SubjectCategoryModel
from database.models.base_resource import ResourceIdentifier, BaseResourceModel
from database.models.subjects import SubjectModel
from NotesApp.routes.base_resource import BaseResourceRouteForm
from NotesApp.routes.base_route import request_logic
from NotesApp.routes.i_request import IRequestData, RequestData, ResponseData
from NotesApp.schemas.schema_context import SchemaContext


class SubjectRoutes(BaseResourceRouteForm):

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
            form: SubjectForm = None,
            form_template: str = 'form_resource.html',
    ):
        super().__init__(app, data, logic, schema, template,
                         resource_url_name, resources_url_name, identifier, form, form_template)
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
        log_access(logging.WARNING, data, name=name)
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
        log_access(logging.WARNING, data, name=name)
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
                len(resource) > 0 and
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

    def populate_form(
            self,
            form: ModelForm,
            data: RequestData,
            obj: BaseResourceModel,
            **kwargs
    ) -> ModelForm:
        form: SubjectForm = super().populate_form(form, data, obj)
        form.categories.query = SubjectCategoryModel.list(data)
        return form
