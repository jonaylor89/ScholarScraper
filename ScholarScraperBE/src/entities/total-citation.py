
from sqlalchemy import Column, String, Integer
from .entity import Entity, Base


class Total-Citations(Entity, Base):

    __tablename__ = "total-citation"

    # The date is in this table as well
    def __init__(self, scholar_id, total_cites, cited_by, created_by):
        Entity.__init__(self, created_by)