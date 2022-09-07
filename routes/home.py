from abc import abstractmethod
from typing import Type, Union

from flask import redirect, url_for, request, Flask, Response

from libs.jwt_functions import jwt_required_with_redirect
from routes.base_route import BaseRoute, request_logic
from routes.i_request import IRequestData, IRequestLogic, RequestPayload, \
    ResponseData


class IHomeRouteLogic(IRequestLogic):

    @classmethod
    @abstractmethod
    def render_home_page(
            cls,
            data: RequestPayload
    ) -> ResponseData:
        pass

    @classmethod
    @abstractmethod
    def render_home_page_filtered(
            cls,
            data: RequestPayload
    ) -> ResponseData:
        pass


class HomeRoutes(BaseRoute):

    logic: Type[IHomeRouteLogic]

    def __init__(
            self,
            app: Flask,
            data: Type[IRequestData],
            logic: Type[IHomeRouteLogic],
    ):
        super().__init__(app, data, logic)
        app.add_url_rule("/", view_func=self.index)
        app.add_url_rule(
            "/home",
            view_func=self.home,
            methods=["GET", "POST"],
        )

    def index(self):
        return redirect(url_for("home"))

    @jwt_required_with_redirect()
    @request_logic
    def home(self, data: RequestPayload) -> Union[Response, ResponseData]:
        if request.method == "POST":
            return self.logic.render_home_page_filtered(data)

        # request.method == "GET"
        return self.logic.render_home_page(data)
