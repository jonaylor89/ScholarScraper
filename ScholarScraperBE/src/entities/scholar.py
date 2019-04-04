
from sqlalchemy import Column, String, Integer
from marshmallow import Schema, fields

from .entity import Entity, Base


class Scholar(Entity, Base):

    __tablename__ = "scholar"

    scholar_id = Column(Integer, primary_key=True)
    name = Clumn(String)

    def __init__(self, scholar_id, name, created_by):
        Entity.__init__(self, created_by)

        self.scholar_id = scholar_id
        self.name = name

    def __repr__(self):
        return f"<Scholar(scholar_id='{self.scholar_id}', name='{self.name}')>"

class ScholarSchema(Schema):
    scholar_id = fields.Number()
    name = fields.String()