
from sqlalchemy import Column, String, Integer
from .entity import Entity, Base

class Scholar(Entity, Base):

    __tablename__ = "scholar"

    def __init__(self, title, description, created_by):
        pass

