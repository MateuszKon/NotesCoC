from typing import List

import bcrypt
from flask import url_for
from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship

from db import db
from libs.random import uuid_gen


class UserModel(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String(80), nullable=False, unique=True)
    password = Column(String(60), nullable=False)
    person_name = Column(String(80), ForeignKey('persons.name'))

    person = relationship("PersonModel", uselist=False)

    def __init__(self, login: str, password: str, person_name: str):
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


class RegisterUserModel(db.Model):
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

    @classmethod
    def get_all(cls) -> List["RegisterUserModel"]:
        return cls.query.all()

    @classmethod
    def get_by_hash(cls, register_hash: str) -> "RegisterUserModel":
        return cls.query.filter_by(hash=register_hash).one_or_none()
