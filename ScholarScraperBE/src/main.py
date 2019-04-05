#!/usr/bin/env python3

import json
import logging

from flask_cors import CORS
from flask import Flask, redirect, jsonify

from .scraper import scraper
from .entities.entity import Session, engine, Base
from .entities.publication_author import PublicationAuthor, PublicationAuthorSchema
from .entities.publication_cites import PublicationCites, PublicationCitesSchema
from .entities.publication import Publication, PublicationSchema
from .entities.scholar import Scholar, ScholarSchema
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


@app.route("/names/<name>", methods=["GET"])
def show_by_name(name: str):
    """
    The main meat and potatoes right now
    In construction!!!
    """
    json_data = {}

    with open("src/scraper/data.json", "r") as f:
        json_data = json.load(f)

    return jsonify(json_data[name])


@app.route("/parse/<name>", methods=["GET", "POST"])
def parse_by_name(name: str):
    """
    Parse people
    """

    # scraper.check_researcher(name)

    return redirect(f"/name/{name}")


@app.route("/secret", methods=["GET", "POST"])
def secret():
    """
    A secret
    """
    return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
