#!/usr/bin/env python3

import json
import logging

from flask_cors import CORS
from flask import Flask, redirect, jsonify, request, render_template

from .scraper import scraper
from .entities.entity import Session, engine, Base
from .entities.publication import Publication, PublicationSchema
from .entities.scholar import Scholar, ScholarSchema
from .entities.publicationauthor import PublicationAuthor, PublicationAuthorSchema
from .entities.publicationcites import PublicationCites, PublicationCitesSchema
from .entities.totalcitations import TotalCitations, TotalCitationsSchema


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
    scholar_objects = session.query(Scholar).all()

    # transforming into JSON-serializable objects
    schema = ScholarSchema(many=True)
    scholars = schema.dump(scholar_objects)

    # serializing as JSON
    session.close()

    return jsonify(scholars.data)


@app.route("/publication", methods=["POST"])
def publication():
    """
    Parse people
    """
    # mount scholar object
    posted_exam = ScholarSchema().load(request.get_json())

    scholar = Scholar(**posted_exam.data, created_by="HTTP post request")

    # persist scholar
    session = Session()
    session.add(scholar)
    session.commit()

    # return created scholar
    new_exam = ScholarSchema().dump(scholar.data)
    session.close()

    return jsonify(new_exam), 201


@app.route("/publication-author")
def get_publication_author():

    # fetching from the database
    session = Session()
    scholar_objects = session.query(Scholar).all()

    # transforming into JSON-serializable objects
    schema = ScholarSchema(many=True)
    scholars = schema.dump(scholar_objects)

    # serializing as JSON
    session.close()

    return jsonify(scholars.data)


@app.route("/publication_author", methods=["POST"])
def publication_author():
    """
    Parse people
    """
    # mount scholar object
    posted_exam = ScholarSchema().load(request.get_json())

    scholar = Scholar(**posted_exam.data, created_by="HTTP post request")

    # persist scholar
    session = Session()
    session.add(scholar)
    session.commit()

    # return created scholar
    new_exam = ScholarSchema().dump(scholar.data)
    session.close()

    return jsonify(new_exam), 201


@app.route("/publication-cites")
def get_publication_cites():

    # fetching from the database
    session = Session()
    scholar_objects = session.query(Scholar).all()

    # transforming into JSON-serializable objects
    schema = ScholarSchema(many=True)
    scholars = schema.dump(scholar_objects)

    # serializing as JSON
    session.close()

    return jsonify(scholars.data)


@app.route("/publication-cites", methods=["POST"])
def publication_cites():
    """
    Parse people
    """
    # mount scholar object
    posted_exam = ScholarSchema().load(request.get_json())

    scholar = Scholar(**posted_exam.data, created_by="HTTP post request")

    # persist scholar
    session = Session()
    session.add(scholar)
    session.commit()

    # return created scholar
    new_exam = ScholarSchema().dump(scholar.data)
    session.close()

    return jsonify(new_exam), 201


@app.route("/total-citation")
def get_total_citations():

    # fetching from the database
    session = Session()
    scholar_objects = session.query(Scholar).all()

    # transforming into JSON-serializable objects
    schema = ScholarSchema(many=True)
    scholars = schema.dump(scholar_objects)

    # serializing as JSON
    session.close()

    return jsonify(scholars.data)


@app.route("/total-citations", methods=["POST"])
def total_citations():
    """
    Parse people
    """
    # mount scholar object
    posted_exam = ScholarSchema().load(request.get_json())

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
