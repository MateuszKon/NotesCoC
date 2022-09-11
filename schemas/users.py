from marshmallow import fields

from db import db
from ma import ma
from models.users import UserModel, RegisterUserModel


class RegisterUserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RegisterUserModel
        # load_only = ()
        exclude = ("id",)
        include_fk = True
        load_instance = True

    link = fields.Str(dump_only=True)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        dump_only = ("id",)
        load_only = ("password",)
        exclude = ("admin",)
        include_fk = True
        load_instance = True
        sqla_session = db.session
