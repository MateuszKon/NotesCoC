from flask import Flask

from logic.base_request_data import BaseRequestData
from logic.home import HomeLogic
from logic.notes import NoteLogic
from logic.user_login import UserLoginLogic
from logic.user_register import UserRegisterLogic
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
        SubjectSchema(
            "NoteSchema",
            notes_param={'only': ('id', 'title', 'persons_visibility')}
        ),
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
    # /register/form/<string:registration_hash>
    # /register/new
    # /register/get_all
    UserRegister(
        app,
        BaseRequestData,
        UserRegisterLogic,
    )
    # /login
    # /logout
    UserLogin(
        app,
        BaseRequestData,
        UserLoginLogic,
    )

    app.add_url_rule("/users", view_func=User.get_all)