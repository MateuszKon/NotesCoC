from flask import Flask

from logic.base_request_data import BaseRequestData
from logic.home import HomeLogic
from routes.home import HomeRoutes
from routes.notes import NoteRoutes
from routes.persons import PersonRoutes
from routes.subjects import SubjectRoutes
from routes.subjects_categories import SubjectCategoryRoutes, CategoryOfSubject
from routes.users import UserRegister, UserLogin, User


def configure_routing(app: Flask):
    # Configure all classes (inject interfaces implementation

    # NoteRoutes.config()
    # PersonRoutes.config()
    # UserRegister.config()
    # UserLogin.config()
    # SubjectRoutes.config()
    # SubjectCategoryRoutes.config()
    # CategoryOfSubject.config()

    # Home routes:
    # /
    # /home
    HomeRoutes.config(app, BaseRequestData, HomeLogic)



    # Note routes
    app.add_url_rule("/new_note",
                     view_func=NoteRoutes.edit_note,
                     methods=["GET", "POST"],
                     )
    app.add_url_rule("/note/<int:note_id>/edit",
                     view_func=NoteRoutes.edit_note,
                     methods=["GET", "POST"],
                     )

    app.add_url_rule("/note/<int:note_id>/delete",
                     view_func=NoteRoutes.delete_note,
                     methods=["GET", "POST", "DELETE"],
                     )

    # Person routes
    app.add_url_rule("/person/<string:name>",
                     view_func=PersonRoutes.person,
                     methods=["GET", "POST", "PUT", "DELETE"],
                     )
    app.add_url_rule("/persons", view_func=PersonRoutes.persons)

    # User routes
    app.add_url_rule("/users", view_func=User.get_all)
    app.add_url_rule("/register/form/<string:registration_hash>",
                     view_func=UserRegister.register_user,
                     methods=["GET", "POST"],
                     )
    app.add_url_rule("/register/new",
                     view_func=UserRegister.add_registration_record,
                     methods=["POST"],
                     )
    app.add_url_rule("/register/get_all",
                     view_func=UserRegister.get_registration_records,
                     )
    app.add_url_rule("/login",
                     view_func=UserLogin.login_user,
                     methods=["GET", "POST"],
                     )
    app.add_url_rule("/logout",
                     view_func=UserLogin.logout_user,
                     methods=["POST"],
                     )

    # Subjects routes
    app.add_url_rule("/subjects", view_func=SubjectRoutes.subjects)
    app.add_url_rule("/subject/<string:name>",
                     view_func=SubjectRoutes.subject,
                     methods=["GET", "POST", "PUT", "DELETE"],
                     )
    app.add_url_rule("/subject_category/<string:name>",
                     view_func=SubjectCategoryRoutes.subject_category,
                     methods=["GET", "POST", "PUT", "DELETE"],
                     )
    app.add_url_rule("/subject_categories",
                     view_func=SubjectCategoryRoutes.subject_categories)
    app.add_url_rule("/subject/<string:name>/category",
                     view_func=CategoryOfSubject.category_of_subject,
                     methods=["POST", "PUT", "DELETE"],
                     )
    app.add_url_rule("/subject/<string:name>/categories",
                     view_func=CategoryOfSubject.categories_of_subject,
                     )
