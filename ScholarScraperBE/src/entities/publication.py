
from sqlalchemy import Column, String, Integer, DateTime

from .entity import Entity, Base

class Publication(Entity, Base):

    __tablename__ = "publication"
    publication_id = Column(Integer, primary_key=True)
    date = Column(DateTime)

    def __init__(self, pub_id, date, created_by):
        Entity.__init__(self, created_by)
        self.publication_id = pub_id 
        self.date = date

    def __repr__(self):
        return f"<Publication(publication_id='{publication_id}', date='{self.date}')>"
