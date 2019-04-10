
from sqlalchemy import Column, String, Integer, DateTime
from marshmallow import Schema, fields

from .entity import Entity, Base


class Publication(Entity, Base):

    __tablename__ = "publication"
    id = Column("id", String(32), primary_key=True)
    title = Column("title", String(256), nullable=True)
    cites = Column("cites", Integer, nullable=True)
    date = Column(String)

    def __init__(self, id, title, cites, date, created_by):
        Entity.__init__(self, created_by)
        self.id = id
        self.title = title
        self.cites = cites
        self.date = date

    def __repr__(self):
        return (
            f"<Publication(id='{self.id}', title='{self.title}', cites='{self.cites}', date='{self.date}')>"
        )


class PublicationSchema(Schema):
    id = fields.Str()
    title = fields.Str()
    cites = fields.Number()
    date = fields.Str()
