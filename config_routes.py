from flask import Flask

from forms.categories import CategoryForm
from forms.subjects import SubjectForm
from logic.base_request_data import BaseRequestData
from logic.home import HomeLogic
from logic.notes import NoteLogic
from logic.settings import SettingsLogic
from logic.user_login import UserLoginLogic
from logic.user_register import UserRegisterLogic
from models import PersonModel, SubjectModel, SubjectCategoryModel, UserModel
from models.base_resource import ResourceIdentifier
from routes.admin_resource_route import AdminResourceRoute
from routes.home import HomeRoutes
from routes.notes import NoteRoutes
from routes.base_resource import BaseResourceRoute, BaseResourceRouteForm
from routes.settings import SettingsRoute
from routes.subjects import SubjectRoutes
from routes.users import UserRegister, UserLogin
from schemas.persons import PersonSchema
from schemas.subjects import SubjectSchema
from schemas.subjects_categories import SubjectCategorySchema
from schemas.users import UserSchema


def configure_routing(app: Flask):
    # Configure all classes (inject interfaces implementation)

    # Home routes:
    # /
    # /home
    HomeRoutes(app, BaseRequestData, HomeLogic)

    # Note routes:
    # /new_note
    # /note/<int:note_id>/view
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
    configure_subject_routes(app)

    # Subject Categories routes
    configure_subject_categories_routes(app)

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

    # User routes
    AdminResourceRoute(
        app,
        BaseRequestData,
        UserModel,
        UserSchema(),
        resource_url_name='user',
        resources_url_name='users',
        identifier=ResourceIdentifier("id", "int"),
    )

    # Settings route
    # /settings
    SettingsRoute(
        app,
        BaseRequestData,
        SettingsLogic
    )


def configure_subject_routes(app: Flask):
    if app.config["DEBUG"]:
        notes_param = {'only': ('id', 'title', 'persons_visibility')}
    else:
        notes_param = {'only': ('id', 'title')}

    return SubjectRoutes(
        app,
        BaseRequestData,
        SubjectModel,
        SubjectSchema(
            "NoteSchema",
            notes_param=notes_param
        ),
        SubjectCategorySchema(
            "SubjectSchema",
            subjects_param={'only': ('name',)}
        ),
        template='subjects.html',
        resource_url_name='subject',
        resources_url_name='subjects',
        identifier=ResourceIdentifier("name", "string"),
        form=SubjectForm,
    )


def configure_subject_categories_routes(app: Flask):
    return BaseResourceRouteForm(
        app,
        BaseRequestData,
        SubjectCategoryModel,
        SubjectCategorySchema(
            "SubjectSchema",
            subjects_param={'only': ('name',)}
        ),
        template='categories.html',
        resource_url_name='subject_category',
        resources_url_name='subject_categories',
        identifier=ResourceIdentifier("name", "string"),
        form=CategoryForm,
    )
