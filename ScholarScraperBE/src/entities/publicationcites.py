from sqlalchemy import Column, String, Integer, ForeignKey
from marshmallow import Schema, fields

from .entity import Entity, Base


class PublicationCites(Entity, Base):

    __tablename__ = "publication-cites"

    publication_id_1 = Column(String(32), ForeignKey("publication.id"), primary_key=True)
    publication_id_2 = Column(
        String(32), ForeignKey("publication.id"), primary_key=True
    )

    def __init__(self, pub_id_1, pub_id_2, created_by):
        Entity.__init__(self, created_by)

        self.publication_id_1 = pub_id_1
        self.publication_id_2 = pub_id_2

    def __repr__(self):
        return f"<PublicationCites(publication_id_1='{publication_id_1}', publication_id_2='{self.publication_id_2}')>"


class PublicationCitesSchema(Schema):
    publication_id_1 = fields.Str()
    publication_id_2 = fields.Str()
