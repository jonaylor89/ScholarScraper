#!/usr/bin/env python3

import json
import logging

from flask_cors import CORS
from flask import Flask, redirect, jsonify, request

from .scraper import scraper
from .entities.entity import Session, engine, Base
from .entities.publication import Publication, PublicationSchema
from .entities.scholar import Scholar, ScholarSchema
from .entities.publication_author import PublicationAuthor, PublicationAuthorSchema
from .entities.publication_cites import PublicationCites, PublicationCitesSchema
from .entities.total_citations import TotalCitations, TotalCitationsSchema


app = Flask(__name__)
CORS(app)

# Create all tables
Base.metadata.create_all(engine)


@app.route("/")
def hello():
    """
    Hello message mostly used for development error checking
    """
    return "<h1>WELCOME TO SCHOLAR SCRAPER!</h1>"


@app.route("/scholar")
def get_schiolars():

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
def parse_by_name():
    """
    Parse people
    """
    # mount scholar object
    posted_exam = ScholarSchema() \
            .load(request.get_json())

    scholar = Scholar(**posted_exam.data, created_by="HTTP post request")

    # persist scholar
    session = Session()
    session.add(scholar)
    session.commit()

    # return created scholar
    new_exam = ScholarSchema().dump(scholar.data)
    session.close()

    return jsonify(new_exam), 201


@app.route("/secret")
def secret():
    """
    A secret
    """
    return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
