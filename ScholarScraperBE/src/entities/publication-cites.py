
from sqlalchemy import Column, String, Integer
from .entity import Entity, Base


class Publication-Cites(Entity, Base):

    __tablename__ = "publication-cites"

    def __init__(self, pub_id_1, pub_id_2, cited_by, created_by):
        Entity.__init__(self, created_by)