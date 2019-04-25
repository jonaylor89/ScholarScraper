#!/usr/bin/env python

import logging

import scholarly
from .entities.entity import Session, engine, Base
from .entities.publication import Publication, PublicationSchema
from .entities.scholar import Scholar, ScholarSchema
from .entities.publicationauthor import PublicationAuthor, PublicationAuthorSchema
from .entities.publicationcites import PublicationCites, PublicationCitesSchema
from .entities.totalcitations import TotalCitations, TotalCitationsSchema

# Create all the tables
Base.metadata.create_all(engine)

logger = logging.getLogger(__name__)

logging.basicConfig(
    filename="scraper.log",
    filemode="w", # Change to 'a' in production
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG, # Change to INFO in production
)

def main():
    pass


if __name__ == "__main__":
    main()
