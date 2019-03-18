from sqlalchemy import Column, String, Integer
from .entity import Entity, Base


class Scholar(Entity, Base):

    __tablename__ = "scholar"

    scholarid = Column(Integer)
    name = Column(String)
    cited_by = Column(String)

    def __init__(self, scholarid, name, cited_by, created_by):
        Entity.__init__(self, created_by)
        self.scholarid = scholarid
        self.name = name
        self.cited_by = cited_by
