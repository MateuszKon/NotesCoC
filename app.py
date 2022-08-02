import os

from flask import Flask

from db import db
from ma import ma
from routes.home import HomeRoutes
from routes.notes import NoteRoutes
from routes.persons import PersonRoutes


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = os.environ.get("APP_SECRET_KEY")


@app.before_first_request
def create_tables():
    db.create_all()


# Home routes
app.add_url_rule("/", view_func=HomeRoutes.index)
app.add_url_rule("/home", view_func=HomeRoutes.home)

# Note routes
app.add_url_rule("/new_note",
                 view_func=NoteRoutes.new_note,
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


if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5001, debug=True)
