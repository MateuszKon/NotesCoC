from database.db import db
from NotesApp.ma import ma
from database.models import SettingModel


class SettingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SettingModel
        exclude = ('id',)
        load_instance = True
        sqla_session = db.session
