from db import db
from routes.i_request import ResponseData, RequestData, IRequestLogic


class BaseResourceModel(IRequestLogic, db.Model):
    __abstract__ = True

    @classmethod
    def create(
            cls,
            data: RequestData,
            name: str,
    ) -> ResponseData:
        instance = cls(name=name, **data.data)
        instance.save_to_db()

    def read(
            self,
    ) -> ResponseData:
        return self

    def update(
            self,
            data: RequestData,
    ) -> ResponseData:
        for key in data.data:
            setattr(self, key, data.data[key])
        self.save_to_db()

    def delete(
            self,
    ) -> ResponseData:
        self.delete_from_db()

    @classmethod
    def list(
            cls,
    ) -> ResponseData:
        return cls.query.all()

    @classmethod
    def get_by_name(cls, name: str, allow_none=False):
        if allow_none:
            return cls.query.filter_by(name=name).one_or_none()
        return cls.query.filter_by(name=name).first_or_404()
