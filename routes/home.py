from flask import render_template, redirect, url_for, request
from flask_jwt_extended import get_jwt

from libs.jwt_functions import jwt_required_with_redirect
from logic.interfaces.i_home_routes import IHomeRoute
from logic.interfaces.i_request_data import IRequestDataHandler
from models.notes import NoteModel
from models.persons import PersonModel


class HomeRoutes:

    data_handler:  IRequestDataHandler = None
    logic: IHomeRoute = None

    @classmethod
    def config(cls, data: IRequestDataHandler, logic: IHomeRoute):
        cls.data_handler = data
        cls.logic = logic

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
