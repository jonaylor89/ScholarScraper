#!/usr/bin/env python

import logging
from datetime import datetime
from typing import List, Dict

from .scholarly import search_author, search_pub_query

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
    filemode="w",  # Change to 'a' in production
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,  # Change to INFO in production
)


def update_citations(pub_id: str, cites: List) -> None:
    """
    Add citations to the Publication-Cites tables
    """
    pass


def parse_article(pub) -> Dict:
    """
    Convert Publication objects to dictionaries for the database
    """
    return {
        "id": pub.id_scholarcitedby,
        "title": pub.bib["title"],
        "author": pub.bib["author"].split("and")[0].strip(),
        "date": datetime.now(),
        "citation_count": pub.citedby,
    }


def update_articles(scholar_id: str, new_articles: List) -> None:
    """
    Add articles to the Publication and Publication-Cites tables
    """

    for article in new_articles:

        # Convert the Publication objects to dictionaries for the db
        new_info = parse_article(article)

        session = Session()

        # Query the old information for that article
        old_info = (
            ScholarSchema(many=True)
            .dump(session.query(Publication).get(str(new_info["id"])))
            .data
        )

        # First a check is done to see if the article existed in the database already
        # and if it didn't then all that must be done is to create a publication object and add it
        # Along with the accompanying citation
        if old_info is None:

            # New publications is added to the database
            publication = Publication(str(new_info["id"]), new_info["title"], "scraper")
            publication_author = PublicationAuthor(
                scholar_id, str(new_info["id"]), "scraper"
            )
            session.add(publication)
            session.add(publication_author)
        else:
            # Scholar has been seen before and just needs updating

            if new_info["citation_count"] == old_info["citation_count"]:
                # Update the date to the current date
                session.query().filter(Scholar.id == new_info["id"]).update(
                    {"date": new_info["date"]}
                )
            else:
                # Update the citation count and date
                session.query().filter(Scholar.id == new_info["id"]).update(
                    {"date": new_info["date"]}
                )
                session.query().filter(
                    TotalCitations.scholar_id == new_info["id"]
                ).update(
                    {
                        "date": new_info["date"],
                        "total_cites": new_info["citation_count"],
                    }
                )

        session.commit()
        session.close()

    for article in new_articles:

        # Update the publications for every author
        update_citations(article.id_scholarcitedby, list(article.citedby()))

    """
    SELECT *
    FROM (
        SELECT publication_id
        FROM PublicationCites
        WHERE 
    ), Publication p
    WHERE p.id IN publication_id
    """


def parse_researcher(author) -> Dict:
    """
    Convert Author objects to dictionaries for the database
    """
    return {
        "id": author.id,
        "full_name": author.name,
        "citation_count": author.citedby,
        "date": datetime.now(),
    }


def update_researchers() -> None:
    """
    Add authors to the Scholar, Total-Citation, and Publication-Author tables
    """

    # Start database session to retrieve which names to parse
    session = Session()

    # Filter the scholars that are meant to be parsed.
    # Generally scholars that are added by the web app are
    # meant to be parsed while scholars added through citations
    # aren't set to be parsed
    scholars = (
        ScholarSchema(many=True)
        .dump(session.query(Scholar).filter(Scholar.to_parse == True))
        .data
    )

    # Close the current session
    session.close()

    for old_info in scholars:

        # Create database session to upload scholar data
        session = Session()

        # Searching for an author returns a generator expression so
        # we make the assumtion that the first search result is the correct one
        author = next(search_author(old_info["full_name"])).fill()
        new_info = parse_researcher(author)

        # First there is a check to make sure citation_count is a key in case this is a new scholar that's never
        # been scaped before. If that works then there is a check to see if the citation count has changed
        # in which case there would need to be a scrape of the publications by the author
        if "citation_count" not in old_info.keys():
            # New scholar is added to the database

            scholar = Scholar(new_info["id"], new_info["full_name"], "scraper")
            total_cite = TotalCitations(
                new_info["id"], new_info["citation_count"], "scraper"
            )

            session.add(scholar)
            session.add(total_cite)
        else:
            # Scholar has been seen before and just needs updating

            if new_info["citation_count"] == old_info["citation_count"]:
                # Update the date to the current date
                session.query().filter.get(new_info["id"]).update(
                    {"date": new_info["date"]}
                )
            else:
                # Update the citation count and date
                session.query().filter.get(new_info["id"]).update(
                    {"date": new_info["date"]}
                )

                # Add new entry to TotalCitations
                total_cite = TotalCitations(
                    new_info["id"], new_info["citation_count"], "scraper"
                )

                session.add(total_cite)

        # Commit new changes to the database
        session.commit()

        # Close the DB connection
        session.close()

    # After updating the author tables, publications must be updated next
    for old_info in scholars:

        # Get the author back
        author = next(search_author(old_info["full_name"])).fill()

        # Update the publications for every author
        update_articles(author.id, list(author.publications))


def main():

    # Begin parsing
    update_researchers()


if __name__ == "__main__":
    main()
