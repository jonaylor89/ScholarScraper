#!/usr/bin/env python3

##############################################
## THIS IS JUST A BUNCH OF SCRIPTS I'M
## USING TO UPLOAD AND UPDATE THINGS IN
## THE DATABASE BECAUSE I WAS STUPID AND PUT
## EVERYTHING IN A JSON FILE.
##############################################

import json

from entities.entity import Session, Base, engine
from entities.scholar import Scholar, ScholarSchema
from entities.publication import Publication, PublicationSchema
from entities.publicationauthor import PublicationAuthor, PublicationAuthorSchema
from entities.totalcitations import TotalCitations, TotalCitationsSchema
from entities.publicationcites import PublicationCites, PublicationCitesSchema

data = None

with open("scraper/data.json") as f:
    data = json.load(f)


def upload_scholar():

    session = Session()

    for name, info in data.items():

        scholar = Scholar(info["id"], name, "json file")

        new_scholar = ScholarSchema().dump(scholar).data

        print(json.dumps(new_scholar, indent=2))

        session.add(scholar)

        session.commit()

    session.close()


def update_scholar():
    """
    Because I messed up the first time
    """
    session = Session()

    for name, info in data.items():
        s = session.query(Scholar).get(info["id"])
        s.full_name = name
        print(name)
        session.commit()

    session.close()


def upload_publication_author():

    for name, info in data.items():
        session = Session()

        for title, article_info in info["articles"].items():
            try:
                pub_auth = PublicationAuthor(
                    str(article_info["id"]), info["id"], "json file"
                )

                new_pub_auth = PublicationAuthorSchema().dump(pub_auth).data

                print(json.dumps(new_pub_auth, indent=2))

                session.add(pub_auth)

                session.commit()

            except Exception as e:
                print(f"bad things {e}")
                break

        session.close()


def upload_publication():

    for name, info in data.items():
        session = Session()

        for title, article_info in info["articles"].items():
            try:
                pub = Publication(
                    str(article_info["id"]),
                    title,
                    article_info["Total citations"],
                    article_info["Publication date"],
                    "json file",
                )

                new_pub = PublicationSchema().dump(pub).data

                print(json.dumps(new_pub, indent=2))

                session.add(pub)

                session.commit()
            except KeyError:
                print("nein")
                continue

            except Exception as e:
                print(f"bad things: {e}")
                break

        session.close()


def upload_total_citations():
    session = Session()

    for name, info in data.items():
        total_cites = TotalCitations(info["id"], info["citation_count"], "json file")

        new_total = TotalCitationsSchema().dump(total_cites).data
        print(json.dumps(new_total, indent=2))

        session.add(total_cites)

        session.commit()

    session.close()


def upload_publication_citations():
    session = Session()

    for name, info in data.items():

        for title, article_info in info["articles"].items():
            try:

                for cite_title, cite_info in article_info["Citation Titles"].items():
                    try:
                        pub = Publication(
                            str(cite_info["id"]),
                            cite_title,
                            cite_info["Total citations"],
                            cite_info["Publication date"],
                            "json file",
                        )

                        new_pub = PublicationSchema().dump(pub).data

                        print(json.dumps(new_pub, indent=2))

                        session.add(pub)

                        session.commit()
                    except KeyError:
                        print("cite nein")
                        continue

                    except Exception as e:
                        print(f"cite bad things: {e}")
                        break

            except KeyError:
                print("nein")
                continue

            except Exception as e:
                print(f"bad things: {e}")
                break

    session.close()


def upload_publication_cites():
    session = Session()

    for name, info in data.items():

        for title, article_info in info["articles"].items():
            try:

                for cite_title, cite_info in article_info["Citation Titles"].items():
                    try:
                        pub_cites = PublicationCites(
                            str(article_info["id"]), str(cite_info["id"]), "json file"
                        )

                        new_pub_cites = PublicationCitesSchema().dump(pub_cites).data

                        print(json.dumps(new_pub_cites, indent=2))

                        session.add(pub_cites)

                        session.commit()
                    except KeyError:
                        print("cite nein")
                        continue

                    except Exception as e:
                        print(f"cite bad things: {e}")
                        break

            except KeyError:
                print("nein")
                continue

            except Exception as e:
                print(f"bad things: {e}")
                break

    session.close()


if __name__ == "__main__":
    #########################
    ##  script to execute  ##
    #########################
    upload_publication_cites()
