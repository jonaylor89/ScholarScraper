
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime

from .entity import Entity, Base

class Total-Citations(Entity, Base):

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
        return f"<Total-Citations(scholar_id='{self.scholar_id}', date='{self.date}', total_cites='{self.total_cites}')>"