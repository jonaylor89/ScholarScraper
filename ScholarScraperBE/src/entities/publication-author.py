
from sqlalchemy import Column, String, Integer
from .entity import Entity, Base


class Publication-Author(Entity, Base):

    __tablename__ = "publication-author"

    publication_id = Column(Integer, primary_key=True)
    scholar_id = Column(Integer, primary_key=True)

    def __init__(self, pub_id, scholar_id, created_by):
        Entity.__init__(self, created_by)