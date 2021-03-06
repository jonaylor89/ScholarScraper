#!/usr/bin/env python

import time
import logging
import traceback
import schedule
from random import shuffle, randint
from time import sleep
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


def update_citations(pub_id: str, cites) -> None:
    """
    Add citations to the Publication-Cites tables
    """

    logger.info(f"Updating citations for publication id '{pub_id}''")

    for cite in cites:
        logger.debug("opening session")
        session = Session()
        try:

            cite.fill()

            # Convert Publication object tot dict
            try:
                new_info = parse_article(cite)
            except Exception as e:
                logger.error(f"article parsing error: {e}")
                traceback.print_exc()
                continue

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
                session.add(publication)

                session.commit()  # Commiting so I don't get integrity errors

                publication_cites = PublicationCites(
                    pub_id, str(new_info["id"]), "scraper"
                )
                session.add(publication_cites)

                session.commit()  # Commit to prevent integrity errors

                # Searching for an author returns a generator expression so
                # we make the assumption that the first search result is the correct one
                author = next(search_author(new_info["author"])).fill()
                author_info = parse_researcher(author)

                # Filter the scholars that are meant to be parsed.
                # Generally scholars that are added by the web app are
                # meant to be parsed while scholars added through citations
                # aren't set to be parsed
                authors = (
                    ScholarSchema(many=True)
                    .dump(
                        session.query(Scholar).filter(Scholar.id == author_info["id"])
                    )
                    .data
                )

                if not authors:
                    # Check if author is already in the database and if they aren't create a new entry
                    # The new entry will not have a parse flag
                    scholar = Scholar(
                        author_info["id"], author_info["full_name"], False, "citation"
                    )
                    session.add(scholar)

                    session.commit()  # Commit to prevent integrity errors

                # Create entry for author citing publication
                publication_author = PublicationAuthor(
                    new_info["id"], author_info["id"], "citation"
                )
                session.add(publication_author)

            else:
                # Citation has been seen before
                # Because citaiton count changes so frequently,
                # it has to be checked and updated even for citations
                if new_info["citation_count"] == old_info["citation_count"]:
                    continue

                else:
                    # Update the citation count
                    session.query(Publication).filter(
                        Publication.id == new_info["id"]
                    ).update({"cites": new_info["citation_count"]})

            session.commit()
            logger.debug("closing session")
            session.close()

            # Sleep to prevent detection
            sleep(randint(1, 10))

        except Exception as e:
            logger.error(f"error parsing citation: '{e}''")
            traceback.print_exc()
            continue

    logger.info("end parsing of citations")


def parse_article(pub) -> Dict:
    """
    Convert Publication objects to dictionaries for the database
    """
    logger.info(f"parsing article '{pub.bib['title']}'")

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

    logger.info(f"updating articles for scholar id '{scholar_id}''")

    for article in new_articles:

        try:

            # Fill the object to have all necessary fields
            # Convert the Publication objects to dictionaries for the db
            try:
                new_info = parse_article(article.fill())
            except Exception as e:
                logger.error(f"article parsing error: {e}")
                traceback.print_exc()
                continue

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
                session.commit()  # Commiting so I don't get integrity errors

                session.add(publication_author)
            else:
                # Scholar has been seen before and just needs updating

                if new_info["citation_count"] == old_info["citation_count"]:
                    continue

                else:
                    # Update the citation count
                    session.query(Publication).filter(
                        Publication.id == new_info["id"]
                    ).update({"citation_count": new_info["citation_count"]})
        except Exception as e:
            logger.error(f"error parsing article: '{article.bib['title']}': {e}")
            traceback.print_exc()
            continue

        session.commit()

        logger.debug("closing session")
        session.close()

        # Give it some time to not get detected
        sleep(randint(1, 10))

        # TODO: Ideally citations should only be updated for new articles and articles with
        #       changes in their citation count be for debugging I still updated citations for every articles.
        #       After debugging and finalizing this code then it will be moved for efficiency.

        # Update citations for the article
        update_citations(article.id_scholarcitedby, article.get_citedby())

    logger.info("end parsing of articles")


def parse_researcher(author) -> Dict:
    """
    Convert Author objects to dictionaries for the database
    """

    logger.info(f"parsing researcher '{author.name}'")

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
            # we make the assumption that the first search result is the correct one
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

                    # Update the publications for every author
                    update_articles(author.id, list(author.publications))

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

                    # Get the author back
                    author = next(search_author(old_info["full_name"])).fill()

                    # Update the publications for every author
                    update_articles(author.id, list(author.publications))

            # Commit new changes to the database
            session.commit()

            # Close the DB connection
            logger.debug("closing session")
            session.close()

            # Give it some time to not get detected
            sleep(randint(1, 3))

        except Exception as e:
            logger.error(f"issue parsing researcher '{old_info['full_name']}': {e}")
            traceback.print_exc()
            continue

    logger.info("end parsing of researchers")


def execute_scrape():
    logger.info("begin scrape")
    n0 = time.time()

    # Begin parsing
    update_researchers()

    n_delta = time.time() - n0
    logger.info(f"end scrape (time elapsed = {n_delta})")


def main():
    # Every day at 12pm, there is a scrape
    schedule.every().day.at("12:00").do(execute_scrape)

    # Loop so that the scheduling task
    # keeps on running all time.
    while True:

        # Checks whether scheduled task
        # is pending to run or not
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
