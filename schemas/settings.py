from db import db
from ma import ma
from models import SettingModel


class SettingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SettingModel
        exclude = ('id',)
        load_instance = True
        sqla_session = db.session
