#!/usr/bin/env python3

import json
import logging
from time import sleep
from random import randint
from typing import Dict

from sqlalchemy import func
from flask_cors import CORS
from flask import Flask, redirect, jsonify, request, render_template

from .entities.entity import Session, engine, Base
from .entities.publication import Publication, PublicationSchema
from .entities.scholar import Scholar, ScholarSchema
from .entities.publicationauthor import PublicationAuthor, PublicationAuthorSchema
from .entities.publicationcites import PublicationCites, PublicationCitesSchema
from .entities.totalcitations import TotalCitations, TotalCitationsSchema

# Create app
app = Flask(__name__)
CORS(app)

# Create all tables
Base.metadata.create_all(engine)


@app.route("/")
def hello():
    """
    Hello message mostly used for development error checking
    """
    return render_template("index.html")


@app.route("/scholar")
def get_scholars():

    # fetching from the database
    session = Session()
    scholar_objects = session.query(Scholar).all()

    # transforming into JSON-serializable objects
    schema = ScholarSchema(many=True)
    scholars = schema.dump(scholar_objects)

    # serializing as JSON
    session.close()

    return jsonify(scholars.data)


@app.route("/scholar", methods=["POST"])
def scholar():
    """
    Parse people
    """
    # mount scholar object
    posted_exam = ScholarSchema().load(request.get_json())

    scholar = Scholar(**posted_exam.data)

    # persist scholar
    session = Session()
    session.add(scholar)
    session.commit()

    # return created scholar
    new_scholar = ScholarSchema().dump(scholar.data)
    session.close()

    return jsonify(new_scholar), 201


@app.route("/publication")
def get_publications():

    # fetching from the database
    session = Session()
    publication_objects = session.query(Publication).all()

    # transforming into JSON-serializable objects
    schema = PublicationSchema(many=True)
    publications = schema.dump(publication_objects)

    # serializing as JSON
    session.close()

    return jsonify(publications.data)


@app.route("/publication", methods=["POST"])
def publication():
    """
    Parse people
    """
    # mount scholar object
    posted_publication = PublicationSchema().load(request.get_json())

    publication = Publication(**posted_publication.data, created_by="HTTP post request")

    # persist scholar
    session = Session()
    session.add(publication)
    session.commit()

    # return created scholar
    new_publication = PublicationSchema().dump(publication.data)
    session.close()

    return jsonify(new_publication), 201


@app.route("/publication-author")
def get_publication_author():

    # fetching from the database
    session = Session()
    publication_author_objects = session.query(PublicationAuthor).all()

    # transforming into JSON-serializable objects
    schema = ScholarSchema(many=True)
    publication_author = schema.dump(publication_author_objects)

    # serializing as JSON
    session.close()

    return jsonify(publication_author.data)


@app.route("/publication_author", methods=["POST"])
def publication_author():
    """
    Parse people
    """
    # mount scholar object
    posted_publication_author = PublicationAuthorSchema().load(request.get_json())

    publication_author = PublicationAuthor(
        **posted_publication_author.data, created_by="HTTP post request"
    )

    # persist scholar
    session = Session()
    session.add(publication_author)
    session.commit()

    # return created scholar
    new_publication_author = PublicationAuthorSchema().dump(publication_author.data)
    session.close()

    return jsonify(new_publication_author), 201


@app.route("/publication-cites")
def get_publication_cites():

    # fetching from the database
    session = Session()
    publication_cites_objects = session.query(PublicationCites).all()

    # transforming into JSON-serializable objects
    schema = ScholarSchema(many=True)
    publication_cites = schema.dump(publication_cites_objects)

    # serializing as JSON
    session.close()

    return jsonify(publication_cites.data)


@app.route("/publication-cites", methods=["POST"])
def publication_cites():
    """
    Parse people
    """
    # mount scholar object
    posted_publication_cites = PublicationCitesSchema().load(request.get_json())

    publication_cites = PublicationCites(
        **posted_publication_cites.data, created_by="HTTP post request"
    )

    # persist scholar
    session = Session()
    session.add(publication_cites)
    session.commit()

    # return created scholar
    new_publication_cites = PublicationCitesSchema().dump(publication_cites.data)
    session.close()

    return jsonify(new_publication_cites), 201


@app.route("/total-citation")
def get_total_citations():

    # fetching from the database
    session = Session()
    total_citations_objects = session.query(TotalCitations).all()

    # transforming into JSON-serializable objects
    schema = TotalCitationsSchema(many=True)
    total_citations = schema.dump(total_citations_objects)

    # serializing as JSON
    session.close()

    return jsonify(total_citations.data)


@app.route("/total-citations", methods=["POST"])
def total_citations():
    """
    Parse people
    """
    # mount scholar object
    posted_total_citations = TotalCitationsSchema().load(request.get_json())

    total_citations = TotalCitations(
        **posted_total_citations.data, created_by="HTTP post request"
    )

    # persist scholar
    session = Session()
    session.add(total_citations)
    session.commit()

    # return created scholar
    new_total_citations = TotalCitationsSchema().dump(total_citations.data)
    session.close()

    return jsonify(new_total_citations), 201


@app.route("/secret")
def secret():
    """
    A secret
    """
    return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")


@app.errorhandler(404)
def not_found(error=None):
    message = {"status": 404, "message": "Not Found: " + request.url}
    resp = jsonify(message)
    resp.status_code = 404

    return resp


def update_scholar(data: Dict):
    """
    Upload scholar to db
    """
    session = Session()

    for name, info in data.items():
        s = session.query(Scholar).get(info["id"])
        s.full_name = name
        print(name)
        session.commit()

    session.close()


def upload_publication(data: Dict):
    """
    Upload publication to db
    """
    session = Session()

    for name, info in data.items():
        for title, article_info in info["articles"].items():
            pub = Publication(
                article_info["id"], title, article_info["publication_date"], "json file"
            )

            new_pub = PublicationSchema().dump(pub).data

            print(json.dumps(new_pub, indent=2))

            session.add(pub)

            session.commit()

    session.close()


def upload_total_citations(data: Dict) -> None:
    """
    Upload total citations to db
    """
    session = Session()

    for name, info in data.items():
        total_cites = TotalCitations(info["id"], info["citation_count"], "json file")

        new_total = TotalCitationsSchema().dump(total_cites).data
        print(json.dumps(new_total, indent=2))

        session.add(total_cites)

        session.commit()

    session.close()
