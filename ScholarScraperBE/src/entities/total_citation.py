from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime
from marshmallow import Schema, fields

from .entity import Entity, Base


class TotalCitations(Entity, Base):

    __tablename__ = "total-citation"

    scholar_id = Column(Integer, primary_key=True)
    date = Column(DateTime, primary_key=True)
    total_cites = Column(Integer)

    def __init__(self, scholar_id, total_cites, cited_by, created_by):
        Entity.__init__(self, created_by)
        self.scholar_id = scholar_id
        self.total_cites = total_cites
        self.date = datetime.now()

    def __repr__(self):
        return f"<TotalCitations(scholar_id='{self.scholar_id}', date='{self.date}', total_cites='{self.total_cites}')>"


class TotalCitationsSchema(Schema):
    scholar_id = fields.Number()
    date = fields.DateTime()
    total_cites = fields.Number()
