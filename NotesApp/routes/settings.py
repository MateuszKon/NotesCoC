from abc import abstractmethod
from typing import Type

from flask import Flask, request

from libs.jwt_functions import jwt_required_with_redirect
from NotesApp.routes.base_route import BaseRoute, request_logic
from NotesApp.routes.i_request import IRequestData, IRequestLogic, RequestData, \
    ResponseData


class ISettingsRouteLogic(IRequestLogic):

    @classmethod
    @abstractmethod
    def render_settings_form(
            cls,
            data: RequestData,
    ) -> ResponseData:
        pass

    @classmethod
    @abstractmethod
    def save_settings(
            cls,
            data: RequestData,
    ) -> ResponseData:
        pass


class SettingsRoute(BaseRoute):

    logic: Type[ISettingsRouteLogic]

    def __init__(
            self,
            app: Flask,
            data: Type[IRequestData],
            logic: Type[ISettingsRouteLogic],
    ):
        super().__init__(app, data, logic)
        app.add_url_rule(
            "/settings",
            view_func=self.settings,
            methods=["GET", "POST"],
        )

    @jwt_required_with_redirect(admin=True)
    @request_logic
    def settings(
            self,
            data: RequestData,
    ) -> ResponseData:
        if request.method == "POST":
            return self.logic.save_settings(data)
        # request.method == "GET"
        return self.logic.render_settings_form(data)
