
from sqlalchemy import Column, String, Integer
from .entity import Entity, Base


class Scholar(Entity, Base):

    __tablename__ = "scholar"

    def __init__(self, scholar_id, name, created_by):
        Entity.__init__(self, created_by)
