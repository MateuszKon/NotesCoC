from typing import List, Union

from db import db
from routes.i_request import ResponseData, RequestData, IRequestLogic


class BaseResourceModel(IRequestLogic, db.Model):
    __abstract__ = True

    @classmethod
    def create(
            cls,
            data: RequestData,
            name: str,
    ) -> 'BaseResourceModel':
        instance = cls(name=name, **data.data)
        instance.save_to_db()
        return instance

    def read(
            self,
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
    ) -> 'BaseResourceModel':
        self.delete_from_db()
        return self

    @classmethod
    def list(
            cls,
    ) -> List['BaseResourceModel']:
        return cls.query.all()

    @classmethod
    def get_by_name(
            cls,
            name: str,
            allow_none=False
    ) -> Union['BaseResourceModel', None]:
        if allow_none:
            return cls.query.filter_by(name=name).one_or_none()
        return cls.query.filter_by(name=name).first_or_404()
