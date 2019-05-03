import os
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, DateTime

# These will change depending on the database
db_url = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")

# This will change depending on the database we have
engine = create_engine(f"mysql+pymysql://{db_user}:{db_pass}@{db_url}/{db_name}")

Session = sessionmaker(bind=engine)
Base = declarative_base()


class Entity(object):

    created_at = Column(DateTime)

    def __init__(self, created_by):
        self.created_at = datetime.now()
