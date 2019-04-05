import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# These will change depending on the database
db_url = "localhost:3306"
db_name = os.getenv("DB_NAME")
db_user = os.getenv("BD_USERNAME")
db_pass = os.getenv("DB_PASSWORD")

# This will change depending on the database we have
engine = create_engine(f"mysql://{db_user}:{db_pass}@{db_url}/{db_name}")

Session = sessionmaker(bind=engine)
Base = declarative_base()


class Entity(object):

    # id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    last_updated_by = Column(String)

    def __init__(self, created_by):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.last_updated_by = created_by
