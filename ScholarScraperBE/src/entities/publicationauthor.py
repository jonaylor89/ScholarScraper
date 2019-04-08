from sqlalchemy import Column, String, Integer, ForeignKey
from marshmallow import Schema, fields

from .entity import Entity, Base


class PublicationAuthor(Entity, Base):

    __tablename__ = "publication-author"

    publication_id = Column(Integer, ForeignKey("publication.id"), primary_key=True)
    scholar_id = Column(Integer, ForeignKey("scholar.id"), primary_key=True)

    def __init__(self, pub_id, scholar_id, created_by):
        Entity.__init__(self, created_by)
        self.publication_id = pub_id
        self.scholar_id = scholar_id

    def __repr__(self):
        return f"<PublicationAuthor(publication_id='{publication_id}', scholar_id='{self.scholar_id}')>"


class PublicationAuthorSchema(Schema):
    publication_id = fields.Number()
    scholar_id = fields.Number()
