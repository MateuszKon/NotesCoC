import os

from flask import Flask
from flask_migrate import Migrate

import a_env_import  # forces using load_dotenv before project imports
from db import db
from ma import ma
from routes.home import HomeRoutes
from routes.notes import NoteRoutes
from routes.persons import PersonRoutes
from routes.users import UserRegister

app = Flask(__name__)
app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")
app.secret_key = os.environ.get("APP_SECRET_KEY")

migrate = Migrate(app, db)
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


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

# User routes
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

if __name__ == "__main__":
    ma.init_app(app)
    app.run(port=5001, debug=True)
