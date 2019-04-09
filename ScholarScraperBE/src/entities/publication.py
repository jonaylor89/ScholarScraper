
from sqlalchemy import Column, String, Integer, DateTime
from marshmallow import Schema, fields

from .entity import Entity, Base


class Publication(Entity, Base):

    __tablename__ = "publication"
    id = Column("id", Integer, primary_key=True)
    title = Column("title", String(256), nullable=True)
    date = Column(DateTime)

    def __init__(self, id, name, date, created_by):
        Entity.__init__(self, created_by)
        self.id = id
        self.name = name
        self.date = date

    def __repr__(self):
        return (
            f"<Publication(id='{self.id}', title='{self.title}', date='{self.date}')>"
        )


class PublicationSchema(Schema):
    id = fields.Number()
    title = fields.Str()
    date = fields.DateTime()
