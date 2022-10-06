from datetime import date

from sqlalchemy import Column, Integer, DateTime

from db import db


class SettingModel(db.Model):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True)
    today_game_date = Column(DateTime, default=date(1920, 1, 1))
