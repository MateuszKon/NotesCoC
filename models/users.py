from typing import List

import bcrypt
from flask import url_for
from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship

from db import db
from libs.random import uuid_gen


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String(80), nullable=False, unique=True)
    password = Column(String(60), nullable=False)
    person_name = Column(String(80), ForeignKey('persons.name'))

    person = relationship("PersonModel", uselist=False)

    def set_password(self, password: str):
        if isinstance(password, str):
            password = bytes(password, 'utf-8')
        self.password = str(bcrypt.hashpw(password, bcrypt.gensalt()), 'utf8')

    def check_password(self, passwd_to_check: str):
        if isinstance(passwd_to_check, str):
            passwd_to_check = bytes(passwd_to_check, 'utf-8')
        password = bytes(self.password, 'utf8')
        return bcrypt.hashpw(passwd_to_check, password) == password


class RegisterUser(db.Model):
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
    def get_all(cls) -> List["RegisterUser"]:
        return cls.query.all()
