from flask import url_for
from marshmallow import EXCLUDE

from models import UserModel
from routes.i_request import RequestData, ResponseData
from routes.settings import ISettingsRouteLogic
from schemas.settings import SettingSchema


settings_schema = SettingSchema()


class SettingsLogic(ISettingsRouteLogic):

    @classmethod
    def render_settings_form(cls, data: RequestData) -> ResponseData:
        user = UserModel.get_requester(data)
        resource = {}
        if user.setting is not None:
            resource = settings_schema.dump(user.setting)
        return ResponseData(
            'settings.html',
            resource=resource,
        )

    @classmethod
    def save_settings(cls, data: RequestData) -> ResponseData:
        user = UserModel.get_requester(data)
        new_settings = settings_schema.load(data.data, unknown=EXCLUDE)
        if user.setting is not None:
            new_settings.id = user.settings.id
            new_settings.merge()
        else:
            new_settings.save_to_db()
            user.setting_id = new_settings.id
            user.merge()
            user.commit()
        return ResponseData(
            resource={'message': "Settings saved."},
            redirect=url_for('home'),
        )