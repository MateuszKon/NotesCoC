from typing import List, Union

from database.db import db
from NotesApp.routes.i_request import RequestData, IRequestLogic


class ResourceIdentifier(object):

    def __init__(self, key: str, key_type: str, value: Union[str, int] = None):
        self.key = key
        self.key_type = key_type
        self.value = value

    @property
    def type_str(self):
        return f"<{self.key_type}:{self.key}>"

    @property
    def dict(self):
        return {self.key: self.value}

    def new_value(self, value: Union[str, int]):
        return type(self)(self.key, self.key_type, value)


class BaseResourceModel(IRequestLogic, db.Model):
    __abstract__ = True

    @classmethod
    def create(
            cls,
            identifier: ResourceIdentifier,
            data: RequestData,
    ) -> 'BaseResourceModel':
        instance = cls(**identifier.dict, **data.data)
        instance.save_to_db()
        return instance

    def read(
            self,
            data: RequestData,
    ) -> 'BaseResourceModel':
        return self

    def update(
            self,
            data: RequestData,
    ) -> 'BaseResourceModel':
        for key in data.data:
            setattr(self, key, data.data[key])
        self.save_to_db()
        return self

    def delete(
            self,
            data: RequestData,
    ) -> 'BaseResourceModel':
        self.delete_from_db()
        return self

    @classmethod
    def list(
            cls,
            data: RequestData,
    ) -> List['BaseResourceModel']:
        return cls.query.all()

    @classmethod
    def get_by_identifier(
            cls,
            identifier: ResourceIdentifier,
            allow_none=False
    ) -> Union['BaseResourceModel', None]:
        qs = cls.query.filter_by(**identifier.dict)
        if allow_none:
            return qs.one_or_none()
        return qs.first_or_404()
