
from sqlalchemy import Column, String, Integer
from .entity import Entity, Base


class Publication-Cites(Entity, Base):

    __tablename__ = "publication-cites"
    
    publcation_id_1 = Column(Integer, primary_key=True)
    publication_id_2 = Column(Integer, primary_key=True)

    def __init__(self, pub_id_1, pub_id_2, created_by):
        Entity.__init__(self, created_by)   

        self.publication_id_1 = pub_id_1
        self.publication_id_2 = pub_id_2

    def __repr__(self):
        return f"<Publication-Cites(publication_id_1='{publication_id_1}', publication_id_2='{self.publication_id_2}')>"