from typing import List, Union

import bcrypt
from flask import url_for
from flask_jwt_extended import create_access_token
from sqlalchemy import String, Integer, Column, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from libs.random import uuid_gen
from models.base_resource import BaseResourceModel


class UserModel(BaseResourceModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String(80), nullable=False, unique=True)
    password = Column(String(60), nullable=False)
    person_name = Column(String(80), ForeignKey('persons.name'))
    setting_id = Column(Integer, ForeignKey('settings.id'))
    admin = Column(Boolean, default=False)

    person = relationship("PersonModel", uselist=False)
    setting = relationship("SettingModel", uselist=False, cascade='delete')

    def __init__(
            self,
            login: str,
            password: str,
            person_name: Union[str, None]
    ):
        self.login = login
        self.person_name = person_name
        self.set_password(password)

    @classmethod
    def get_by_login(cls, username: str) -> "UserModel":
        return cls.query.filter_by(login=username).one_or_none()

    def set_password(self, password: str):
        if isinstance(password, str):
            password = bytes(password, 'utf-8')
        self.password = str(bcrypt.hashpw(password, bcrypt.gensalt()), 'utf8')

    def check_password(self, passwd_to_check: str):
        if isinstance(passwd_to_check, str):
            passwd_to_check = bytes(passwd_to_check, 'utf-8')
        password = bytes(self.password, 'utf8')
        return bcrypt.hashpw(passwd_to_check, password) == password

    @classmethod
    def get_all(cls) -> List["UserModel"]:
        return cls.query.all()

    def create_authorisation_tokens(self) -> str:
        additional_claims = {"scope": self.person_name}
        if self.admin:
            additional_claims["admin"] = True
        access_token = create_access_token(
            identity=self.id,
            additional_claims=additional_claims,
        )
        return access_token

    @classmethod
    def create_single_admin_user(cls, login: str, password: str):
        if cls.query.filter_by(admin=True).one_or_none() is None:
            user = cls(login, password, person_name=None)
            user.admin = True
            user.save_to_db()


class RegisterUserModel(BaseResourceModel):
    __tablename__ = "register_users"

    id = Column(Integer, primary_key=True)
    hash = Column(String(36), unique=True, default=uuid_gen)
    person_name = Column(String(80), ForeignKey("persons.name"))

    @property
    def link(self):
        return url_for(
            'register_user',
            registration_hash=self.hash,
            _external=True,
        )
