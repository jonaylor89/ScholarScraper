
from sqlalchemy import Column, String, Integer
from .entity import Entity, Base


class Publication(Entity, Base):

    __tablename__ = "publication"

    # date is needed in this table as well
    def __init__(self, pub_id, cited_by, created_by):
        Entity.__init__(self, created_by)