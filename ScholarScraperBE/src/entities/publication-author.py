
from sqlalchemy import Column, String, Integer
from .entity import Entity, Base


class Publication-Author(Entity, Base):

    __tablename__ = "publication-author"

    def __init__(self, pub_id, scholar_id, created_by):
        Entity.__init__(self, created_by)