import os

from flask import Flask

from db import db
from routes.home import HomeRoutes
from routes.note import NoteRoutes

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = os.environ.get("APP_SECRET_KEY")


@app.before_first_request
def create_tables():
    db.create_all()


app.add_url_rule("/", view_func=HomeRoutes.index)
app.add_url_rule("/home", view_func=HomeRoutes.home)
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


if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5001, debug=True)
