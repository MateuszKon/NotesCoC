from abc import abstractmethod
from typing import Type, Union

from flask import request, Response, Flask

from libs.jwt_functions import jwt_required_with_redirect, \
    access_denied_response
from routes.base_route import BaseRoute, request_logic
from routes.i_request import IRequestLogic, RequestPayload, ResponseData, \
    IRequestData, RequestData


class INoteRouteLogic(IRequestLogic):

    @classmethod
    @abstractmethod
    def render_edit_note(
            cls,
            data: RequestData,
            note_id: int = None,
    ) -> ResponseData:
        pass

    @classmethod
    @abstractmethod
    def save_note(
            cls,
            data: RequestData,
            note_id: int = None,
    ) -> Response:
        pass

    @classmethod
    @abstractmethod
    def render_delete_note_confirmation(
            cls,
            data: RequestData,
            note_id: int,
    ) -> ResponseData:
        pass

    @classmethod
    @abstractmethod
    def delete_note(
            cls,
            data: RequestData,
            note_id: int,
    ) -> Union[ResponseData, Response]:
        pass


class NoteRoutes(BaseRoute):

    logic: Type[INoteRouteLogic]

    def __init__(
            self,
            app: Flask,
            data: Type[IRequestData],
            logic: Type[INoteRouteLogic],
    ):
        super().__init__(app, data, logic)
        app.add_url_rule(
            "/new_note",
            view_func=self.edit_note,
            methods=["GET", "POST"],
        )
        app.add_url_rule(
            "/note/<int:note_id>/view",
            view_func=self.edit_note,
            methods=["GET", "POST"],
        )
        app.add_url_rule(
            "/note/<int:note_id>/delete",
            view_func=self.delete_note,
            methods=["GET", "POST", "DELETE"],
        )

    @jwt_required_with_redirect()
    @request_logic
    def edit_note(
            self,
            data: RequestData,
            note_id: int = None,
    ) -> Union[Response, ResponseData]:
        if request.method == "POST":
            if not data.context.admin:
                return access_denied_response()
            return self.logic.save_note(data, note_id=note_id)

        # request.method == "GET"
        return self.logic.render_edit_note(data, note_id=note_id)

    @jwt_required_with_redirect(admin=True)
    @request_logic
    def delete_note(
            self,
            data: RequestData,
            note_id: int
    ) -> Union[Response, ResponseData]:
        if request.method in ["DELETE", "POST"]:
            return self.logic.delete_note(data, note_id=note_id)

        # request.method == "GET"
        return self.logic.render_delete_note_confirmation(data, note_id=note_id)
