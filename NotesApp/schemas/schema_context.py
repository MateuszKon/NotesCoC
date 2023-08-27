from marshmallow import Schema

from NotesApp.routes.i_request import ContextData


class SchemaContext(object):

    def __init__(self, schema: Schema, data: ContextData):
        self.schema = schema
        self.data = data

    def __enter__(self):
        self.schema.context["request-context"] = self.data

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.schema.context.pop("request-context")
