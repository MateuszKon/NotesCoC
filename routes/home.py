from typing import Type

from flask import redirect, url_for, request, Flask

from libs.jwt_functions import jwt_required_with_redirect
from logic.interfaces.i_home_routes import IHomeRoute
from logic.interfaces.i_request_data import IRequestDataHandler


class HomeRoutes:

    data_handler:  Type[IRequestDataHandler] = None
    logic: Type[IHomeRoute] = None

    @classmethod
    def config(
            cls,
            app: Flask,
            data: Type[IRequestDataHandler],
            logic: Type[IHomeRoute],
    ):
        cls.data_handler = data
        cls.logic = logic
        app.add_url_rule("/", view_func=HomeRoutes.index)
        app.add_url_rule(
            "/home",
            view_func=HomeRoutes.home,
            methods=["GET", "POST"],
        )

    @classmethod
    def index(cls):
        return redirect(url_for("home"))

    @classmethod
    @jwt_required_with_redirect()
    def home(cls):
        data = cls.data_handler.get_request_data()

        if request.method == "POST":
            return cls.logic.render_home_page_filtered(data)

        # request.method == "GET"
        return cls.logic.render_home_page(data)
