#!/usr/bin/env python

import logging
import traceback
from random import shuffle
from datetime import datetime
from typing import List, Dict
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from scraper.scholarly import search_author, search_pubs_query

from entities.entity import Session, engine, Base
from entities.publication import Publication, PublicationSchema
from entities.scholar import Scholar, ScholarSchema
from entities.publicationauthor import PublicationAuthor, PublicationAuthorSchema
from entities.publicationcites import PublicationCites, PublicationCitesSchema
from entities.totalcitations import TotalCitations, TotalCitationsSchema


# Create all the tables
Base.metadata.create_all(engine)

logger = logging.getLogger(__name__)

logging.basicConfig(
    filename="scraper.log",
    filemode="w",  # TODO: Change to `a` for production
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,  
)

logging.getLogger("urllib3").setLevel(logging.WARNING)


def update_citations(pub_id: str, cites: List) -> None:
    """
    Add citations to the Publication-Cites tables
    """

    logger.debug(f"Updating citations for publication id {pub_id}")

    for cite in cites:
        logger.debug("opening session")
        session = Session()
        try:

            cite.fill()

            # Convert Publication object tot dict
            new_info = parse_article(cite)

            # Grab old value for that publication
            old_info = (
                PublicationSchema(many=False)
                .dump(session.query(Publication).get(str(new_info["id"])))
                .data
            )

            # First a check is done to see if the article existed in the database already
            # and if it didn't then all that must be done is to create a publication object and add it
            # along with the citation reference
            if not old_info:

                # New publications is added to the database
                publication = Publication(
                    str(new_info["id"]),
                    new_info["title"],
                    new_info["citation_count"],
                    new_info["date"],
                    "scraper",
                )
                publication_cites = PublicationCites(pub_id, str(new_info["id"]), "scraper")

                session.add(publication)
                session.commit() # Commiting so I don't get integrety errors

                session.add(publication_cites)
            else:
                # Citation has been seen before
                # Because citaiton count changes so frequently,
                # it has to be checked and updated even for citations
                if new_info["citation_count"] == old_info["cites"]:
                    continue

                else:
                    # Update the citation count
                    session.query(Publication).filter(Publication.id == new_info["id"]).update(
                        {"cites": new_info["citation_count"]}
                    )

        except Exception as e:
            logger.error(f"error parsing citation: {e}")
            traceback.print_exc()
            continue

        session.commit()

        logger.debug("closing dession")
        session.close()


def parse_article(pub) -> Dict:
    """
    Convert Publication objects to dictionaries for the database
    """
    logger.info(f"parsing article {pub.bib['title']}")

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

    logger.info(f"updating articles for scholar id {scholar_id}")

    for article in new_articles:

        try:

            # Fill the object to have all necessary fields
            # Convert the Publication objects to dictionaries for the db
            new_info = parse_article(article.fill())

            logger.debug("opening session")
            session = Session()

            # Query the old information for that article
            old_info = (
                PublicationSchema(many=False)
                .dump(session.query(Publication).get(str(new_info["id"])))
                .data
            )

            # First a check is done to see if the article existed in the database already
            # and if it didn't then all that must be done is to create a publication object and add it
            # Along with the accompanying citation
            if not old_info:

                # New publications is added to the database
                publication = Publication(
                    str(new_info["id"]),
                    new_info["title"],
                    new_info["citation_count"],
                    new_info["date"],
                    "scraper",
                )

                publication_author = PublicationAuthor(
                    str(new_info["id"]), scholar_id, "scraper"
                )

                session.add(publication)
                session.commit() # Commiting so I don't get integrity errors

                session.add(publication_author)
            else:
                # Scholar has been seen before and just needs updating

                if new_info["citation_count"] == old_info["cites"]:
                    continue

                else:
                    # Update the citation count
                    session.query(Publication).filter(Publication.id == new_info["id"]).update(
                        {"cites": new_info["citation_count"]}
                    )
        except Exception as e:
            logger.error(f"error parsing article: {article.bib['title']}: {e}")
            traceback.print_exc()
            continue

        session.commit()
        
        logger.debug("closing session")
        session.close()

        # Update the citations for article
        update_citations(article.id_scholarcitedby, list(article.get_citedby()))


def parse_researcher(author) -> Dict:
    """
    Convert Author objects to dictionaries for the database
    """

    logger.info(f"parsing researcher {author.name}")

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

    logger.info("updating researchers")

    # Start database session to retrieve which names to parse
    logger.debug("opening session")
    session = Session()

    # Filter the scholars that are meant to be parsed.
    # Generally scholars that are added by the web app are
    # meant to be parsed while scholars added through citations
    # aren't set to be parsed
    scholars = (
        ScholarSchema(many=True)
        .dump(session.query(Scholar).filter(Scholar.parse == True))
        .data
    )

    # Close the current session
    logger.debug("closing session")
    session.close()

    shuffle(scholars)

    for old_info in scholars:
        try:
            # Create database session to upload scholar data
            logger.debug("opening session")
            session = Session()

            total_citations = (
                TotalCitationsSchema(many=False)
                .dump(
                    session.query(TotalCitations)
                    .filter(TotalCitations.scholar_id == old_info["id"])
                    .group_by(TotalCitations.scholar_id)
                    .having(func.max(TotalCitations.date))
                    .first()
                )
                .data
            )

            if total_citations != []:
                old_info = {**old_info, **(total_citations)}

            # Searching for an author returns a generator expression so
            # we make the assumtion that the first search result is the correct one
            author = next(search_author(old_info["full_name"])).fill()
            new_info = parse_researcher(author)

            # First there is a check if citation_count is not a key in case this is a new scholar that's never
            # been scaped before. If that works then there is a check to see if the citation count has changed
            # in which case there would need to be a scrape of the publications by the author
            if "citation_count" not in old_info.keys():
                # New scholar is added to the database

                try:
                    # scholar = Scholar(new_info["id"], new_info["full_name"], True,"scraper")
                    total_cite = TotalCitations(
                        new_info["id"], new_info["citation_count"], "scraper"
                    )

                    # session.add(scholar)
                    session.add(total_cite)
                except IntegrityError as e:
                    logger.error(f"Database error: {e}")
            else:
                # Scholar has been seen before and just needs updating

                if new_info["citation_count"] == old_info["citation_count"]:
                    # Citation count is the same so nothing to do
                    continue
                else:
                    # Add new entry to TotalCitations because of the change
                    total_cite = TotalCitations(
                        new_info["id"], new_info["citation_count"], "scraper"
                    )

                    session.add(total_cite)

            # Commit new changes to the database
            session.commit()

            # Close the DB connection
            logger.debug("closing session")
            session.close()

            # Get the author back
            author = next(search_author(old_info["full_name"])).fill()

            # Update the publications for every author
            update_articles(author.id, list(author.publications))

        except Exception as e:
            logger.error(f"issue parsing researcher {old_info['full_name']}: {e}")
            traceback.print_exc()
            continue


def main():

    # Begin parsing
    update_researchers()


if __name__ == "__main__":
    main()
