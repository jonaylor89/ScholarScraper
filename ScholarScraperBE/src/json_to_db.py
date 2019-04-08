#!/usr/bin/env python3

##############################################
## THIS IS JUST A BUNCH OF SCRIPTS I'M 
## USING TO UPLOAD AND UPDATE THINGS IN
## THE DATABASE BECAUSE I WAS STUPID AND PUT
## EVERYTHING IN A JSON FILE. 
##############################################

from entities.entity import Session, Base, engine
from entities.scholar import Scholar, ScholarSchema
from entities.publication import Publication, PublicationSchema
from entities.totalcitations import TotalCitations, TotalCitationsSchema

import json

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


def upload_publication():
    session = Session()

    for name, info in data.items():
        for title, article_info in info["articles"].items():
            pub = Publication(article_info["id"], title, article_info["publication_date"], "json file")

            new_pub = PublicationSchema().dump(pub).data

            print(json.dumps(new_pub, indent=2))

            session.add(pub)

            session.commit()


    session.close()



def upload_total_citations():
    session = Session()

    for name, info in data.items():
        try:
            total_cites = TotalCitations(info["id"], info["citation_count"], "json file")
        except KeyError:
            total_cites = TotalCitations(info["id"], info["citations_count"], "json file")


        new_total = TotalCitationsSchema().dump(total_cites).data
        print(json.dumps(new_total, indent=2))

        session.add(total_cites)

        session.commit()

    session.close()

if __name__ == "__main__":
    #########################
    ##  script to execute  ##
    #########################

    pass