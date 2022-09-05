from abc import abstractmethod
from typing import Type

from flask import redirect, url_for, request, Flask

from libs.jwt_functions import jwt_required_with_redirect
from routes.base_route import BaseRoute, request_logic
from routes.i_request import IRequestData, IRequestLogic, RequestData


class IHomeRouteLogic(IRequestLogic):

    @classmethod
    @abstractmethod
    def render_home_page(
            cls,
            data: RequestData
    ) -> RequestData:
        pass

    @classmethod
    @abstractmethod
    def render_home_page_filtered(
            cls,
            data: RequestData
    ) -> RequestData:
        pass


class HomeRoutes(BaseRoute):

    logic: Type[IHomeRouteLogic]

    @classmethod
    def config(
            cls,
            app: Flask,
            data: Type[IRequestData],
            logic: Type[IHomeRouteLogic],
    ):
        super().config(app, data, logic)
        app.add_url_rule("/", view_func=cls.index)
        app.add_url_rule(
            "/home",
            view_func=cls.home,
            methods=["GET", "POST"],
        )

    @classmethod
    def index(cls):
        return redirect(url_for("home"))

    @classmethod
    @jwt_required_with_redirect()
    @request_logic
    def home(cls, data):
        if request.method == "POST":
            return cls.logic.render_home_page_filtered(data)

        # request.method == "GET"
        return cls.logic.render_home_page(data)
