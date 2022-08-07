from marshmallow import fields

from ma import ma
from models.users import RegisterUser


class RegisterUserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RegisterUser
        # load_only = ()
        dump_only = ("id",)
        exclude = ("hash",)
        include_fk = True
        load_instance = True

    link = fields.Str(dump_only=True)
