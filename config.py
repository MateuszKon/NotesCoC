import datetime
import os


def _translate_postgres_driver(database_url: str):
    if 'postgres' in database_url and 'postgresql' not in database_url:
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
