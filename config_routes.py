from flask import Flask

from logic.base_request_data import BaseRequestData
from logic.home import HomeLogic
from logic.notes import NoteLogic
from models import PersonModel, SubjectModel, SubjectCategoryModel
from models.base_resource import ResourceIdentifier
from routes.home import HomeRoutes
from routes.notes import NoteRoutes
from routes.base_resource import BaseResourceRoute
from routes.subjects import SubjectRoutes
from routes.users import UserRegister, UserLogin, User
from schemas.persons import PersonSchema
from schemas.subjects import SubjectSchema
from schemas.subjects_categories import SubjectCategorySchema


def configure_routing(app: Flask):
    # Configure all classes (inject interfaces implementation)

    # Home routes:
    # /
    # /home
    HomeRoutes(app, BaseRequestData, HomeLogic)

    # Note routes:
    # /new_note
    # /note/<int:note_id>/edit
    # /note/<int:note_id>/delete
    NoteRoutes(app, BaseRequestData, NoteLogic)

    # Person routes
    BaseResourceRoute(
        app,
        BaseRequestData,
        PersonModel,
        PersonSchema(),
        resource_url_name='person',
        resources_url_name='persons',
        identifier=ResourceIdentifier("name", "string"),
    )

    # Subjects routes
    SubjectRoutes(
        app,
        BaseRequestData,
        SubjectModel,
        SubjectSchema(),
        SubjectCategorySchema(),
        resource_url_name='subject',
        resources_url_name='subjects',
        identifier=ResourceIdentifier("name", "string"),
    )

    # Subject Categories routes
    BaseResourceRoute(
        app,
        BaseRequestData,
        SubjectCategoryModel,
        SubjectCategorySchema(),
        resource_url_name='subject_category',
        resources_url_name='subject_categories',
        identifier=ResourceIdentifier("name", "string"),
    )

    # User routes
    app.add_url_rule("/users", view_func=User.get_all)
    # app.add_url_rule("/register/form/<string:registration_hash>",
    #                  view_func=UserRegister.register_user,
    #                  methods=["GET", "POST"],
    #                  )
    # app.add_url_rule("/register/new",
    #                  view_func=UserRegister.add_registration_record,
    #                  methods=["POST"],
    #                  )
    # app.add_url_rule("/register/get_all",
    #                  view_func=UserRegister.get_registration_records,
    #                  )
    app.add_url_rule("/login",
                     view_func=UserLogin.login_user,
                     methods=["GET", "POST"],
                     )
    app.add_url_rule("/logout",
                     view_func=UserLogin.logout_user,
                     methods=["POST"],
                     )
