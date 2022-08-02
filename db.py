from flask_sqlalchemy import SQLAlchemy


class BaseModel:

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


db = SQLAlchemy(model_class=BaseModel)
