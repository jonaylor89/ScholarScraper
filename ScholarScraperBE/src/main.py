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


@app.route("/scholar")
def get_scholars():
    """
    Serve all scholars in db
    """

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
    Add scholar to the db
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
    """
    Serve all publications in the db
    """

    # fetching from the database
    session = Session()
    publication_objects = session.query(Publication).all()

    # transforming into JSON-serializable objects
    schema = PublicationSchema(many=True)
    publications = schema.dump(publication_objects)

    # serializing as JSON
    session.close()

    return jsonify(publications.data)


@app.route("/publication-author")
def get_publication_author():
    """
    Serve all publications with their associated author in the db
    """

    # fetching from the database
    session = Session()
    publication_author_objects = session.query(PublicationAuthor).all()

    # transforming into JSON-serializable objects
    schema = ScholarSchema(many=True)
    publication_author = schema.dump(publication_author_objects)

    # serializing as JSON
    session.close()

    return jsonify(publication_author.data)


@app.route("/publication-cites")
def get_publication_cites():
    """
    Serve all publication and the publications that cite them in the db
    """

    # fetching from the database
    session = Session()
    publication_cites_objects = session.query(PublicationCites).all()

    # transforming into JSON-serializable objects
    schema = ScholarSchema(many=True)
    publication_cites = schema.dump(publication_cites_objects)

    # serializing as JSON
    session.close()

    return jsonify(publication_cites.data)


@app.route("/total-citation")
def get_total_citations():
    """
    Serve the total citation count for every scholar in the db
    """

    # fetching from the database
    session = Session()
    total_citations_objects = session.query(TotalCitations).all()

    # transforming into JSON-serializable objects
    schema = TotalCitationsSchema(many=True)
    total_citations = schema.dump(total_citations_objects)

    # serializing as JSON
    session.close()

    return jsonify(total_citations.data)


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
