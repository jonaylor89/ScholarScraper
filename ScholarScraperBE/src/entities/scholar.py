from sqlalchemy import Column, String, Integer
from marshmallow import Schema, fields

from .entity import Entity, Base


class Scholar(Entity, Base):

    __tablename__ = "scholar"

    id = Column("id", Integer, primary_key=True)
    full_name = Column("full_name", String(64), nullable=True)

    def __init__(self, id, name, created_by):
        Entity.__init__(self, created_by)

        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Scholar(id='{self.id}', full_name='{self.full_name}')>"


class ScholarSchema(Schema):
    id = fields.Number()
    full_name = fields.Str()
