from sqlalchemy import Column, String, Integer, DateTime
from marshmallow import Schema, fields

from .entity import Entity, Base


class Publication(Entity, Base):

    __tablename__ = "publication"
    id = Column("id", String(32), primary_key=True)
    title = Column("title", String(256), nullable=True)
    citation_count = Column("citation_count", Integer, nullable=True)
    date = Column(String)

    def __init__(self, id, title, citation_count, date, created_by):
        Entity.__init__(self, created_by)
        self.id = id
        self.title = title
        self.citation_count = citation_count
        self.date = date

    def __repr__(self):
        return f"<Publication(id='{self.id}', title='{self.title}', citation count='{self.citation_count}', date='{self.date}')>"


class PublicationSchema(Schema):
    id = fields.Str()
    title = fields.Str()
    citation_count = fields.Number()
    date = fields.Str()

