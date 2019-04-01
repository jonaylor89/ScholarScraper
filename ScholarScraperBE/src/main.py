#!/usr/bin/env python3

import json
import logging
from .scraper import scraper
# from .entities.entity import Session, engine, Base
# from .entities.scholar import Scholar
from flask_cors import CORS
from flask import Flask, redirect, jsonify

app = Flask(__name__)
CORS(app)

# Create all tables
# Base.metadata.create_all(engine)


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
