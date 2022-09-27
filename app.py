import os
import time

from flask import Flask, g
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

import libs.env_import  # Import for loading .env file before other imports
from blocklist import BLOCKLIST
from db import db
from libs.jwt_functions import token_expired_redirection_callback
from ma import ma
from models.users import UserModel
from config_routes import configure_routing


app = Flask(__name__)
app.config.from_object("config.Config")
app.config.from_object(os.environ.get("APPLICATION_SETTINGS"))
app.secret_key = os.environ.get("APP_SECRET_KEY")
jwt = JWTManager(app)
migrate = Migrate(app, db)
db.init_app(app)
ma.init_app(app)


jwt.expired_token_loader(token_expired_redirection_callback)
jwt.revoked_token_loader(token_expired_redirection_callback)


@app.before_first_request
def create_admin_user():
    UserModel.create_single_admin_user(
        os.environ.get("USERADMIN_LOGIN"),
        os.environ.get("USERADMIN_PASSWORD"),
    )


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST


configure_routing(app)


if app.config.get("DEBUG"):
    @app.before_request
    def before_request():
        g.request_start_time = time.time()
        g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)

if __name__ == "__main__":
    app.run(port=5001, debug=True)
