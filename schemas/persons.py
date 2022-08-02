from ma import ma
from models.persons import PersonModel


class PersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PersonModel
        # load_only = (,)
        dump_only = ("id",)
        load_instance = True
