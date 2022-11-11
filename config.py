import datetime
import logging.config
import os

import libs.env_import  # Import for loading .env file before other imports
from libs.path import get_project_directory
from routes.i_request import ContextData, RequestData


def _translate_postgres_driver(database_url: str):
    if database_url and 'postgres' in database_url and 'postgresql' not in database_url:
        return database_url.replace("postgres", "postgresql")
    return database_url


class Config:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = _translate_postgres_driver(
        os.environ.get("DATABASE_URL")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    SECRET_KEY = os.environ["APP_SECRET_KEY"]
    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
    JWT_TOKEN_LOCATION = ["cookies", "headers"]
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=12)
    JWT_COOKIE_SECURE = True
    JWT_CSRF_CHECK_FORM = True
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access",]


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL",
                                             "sqlite:///data.db")
    SQLALCHEMY_ECHO = False


logging.config.fileConfig(os.path.join(get_project_directory(), 'logging.conf'))
logger = logging.getLogger("NotesCoC")


def log_access(level: int, data: RequestData, **kwargs):
    logger.log(
        level,
        f"Url: {data.context.get('url')} [{data.context.get('method')}] "
        f"User sub: {data.context.get('jwt_sub')} Admin: {data.context.admin} Scope: {data.context.get('jwt_scope')} "
        + " ".join([f"{key}: {value}" for key, value in kwargs.items()])
    )
