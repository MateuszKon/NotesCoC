import logging
from abc import abstractmethod
from typing import Type, Union

from flask import request, Response, Flask

from config import log_access
from libs.jwt_functions import jwt_required_with_redirect, \
    access_denied_response
from routes.base_route import BaseRoute, request_logic
from routes.i_request import IRequestLogic, ResponseData, \
    IRequestData, RequestData


class INoteRouteLogic(IRequestLogic):

    @classmethod
    @abstractmethod
    def edit_note(
            cls,
            data: RequestData,
            note_id: int = None,
    ) -> ResponseData:
        pass

    @classmethod
    @abstractmethod
    def render_edit_note(
            cls,
            data: RequestData,
            note_id: int = None,
    ) -> ResponseData:
        #  Obsolete
        pass

    @classmethod
    @abstractmethod
    def save_note(
            cls,
            data: RequestData,
            note_id: int = None,
    ) -> Response:
        #  Obsolete
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

    @classmethod
    @abstractmethod
    def custom_note(
            cls,
            data: RequestData,
    ) -> ResponseData:
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
        app.add_url_rule(
            "/custom_note",
            view_func=self.custom_note,
            methods=["GET", "POST"],
        )

    @jwt_required_with_redirect(admin=True)
    @request_logic
    def edit_note(
            self,
            data: RequestData,
            note_id: int = None,
    ) -> Union[Response, ResponseData]:
        level = logging.INFO if request.method == "GET" else logging.WARNING
        log_access(level, data, note_id=note_id)
        if request.method == "POST" and not data.context.admin:
            return access_denied_response()
        return self.logic.edit_note(data, note_id=note_id)

    @jwt_required_with_redirect(admin=True)
    @request_logic
    def delete_note(
            self,
            data: RequestData,
            note_id: int
    ) -> Union[Response, ResponseData]:
        level = logging.INFO if request.method == "GET" else logging.WARNING
        log_access(level, data, note_id=note_id)
        if request.method in ["DELETE", "POST"]:
            return self.logic.delete_note(data, note_id=note_id)

        # request.method == "GET"
        return self.logic.render_delete_note_confirmation(data, note_id=note_id)

    @jwt_required_with_redirect()
    @request_logic
    def custom_note(
            self,
            data: RequestData,
    ) -> Union[Response, ResponseData]:
        return self.logic.custom_note(data)
