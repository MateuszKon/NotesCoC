import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

import libs.env_import  # Import for loading .env file before other imports
from db import db
from libs.jwt_functions import token_expired_redirection_callback
from ma import ma
from models.users import UserModel
from routes.home import HomeRoutes
from routes.notes import NoteRoutes
from routes.persons import PersonRoutes
from routes.users import UserRegister, UserLogin, User

app = Flask(__name__)
app.config.from_object("config.Config")
app.config.from_object(os.environ.get("APPLICATION_SETTINGS"))
app.secret_key = os.environ.get("APP_SECRET_KEY")
jwt = JWTManager(app)
migrate = Migrate(app, db)
db.init_app(app)


jwt.expired_token_loader(token_expired_redirection_callback)


@app.before_first_request
def create_admin_user():
    UserModel.create_single_admin_user(
        os.environ.get("USERADMIN_LOGIN"),
        os.environ.get("USERADMIN_PASSWORD"),
    )


# Home routes
app.add_url_rule("/", view_func=HomeRoutes.index)
app.add_url_rule("/home",
                 view_func=HomeRoutes.home,
                 methods=["GET", "POST"],
                 )

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

if __name__ == "__main__":
    ma.init_app(app)
    app.run(port=5001, debug=True)
