#!/usr/bin/env python3

import json
import logging
from .scraper import scraper
from .entities.entity import Session, engine, Base
from .entities.scholar import Scholar
from flask_cors import CORS
from flask import Flask, redirect

app = Flask(__name__)
CORS(app)

Base.metadaa.create_all(engine)


@app.route("/")
def hello():
    """
    Hello message mostly used for development error checking
    """
    return "WELCOME TO SCHOLAR SCRAPER!"


@app.route("/name/<name>", methods=["GET"])
def show_by_name(name: str):
    """
    The main meat and potatoes right now
    """

    json_data = ""

    with open("data.json", "r") as f:
        json_data = json.loads(f.read())

    if name not in json_data.keys():
        scraper.parse_by_name(name)

        with open("data.json", "r") as f:
            json_data = json.loads(f.read())

    return json.dumps(json_data[name], indent=2)


@app.route("/parse/<name>", methods=["GET", "POST"])
def parse_by_name(name: str):
    """
    Parse people
    """

    scraper.parse_by_name(name)

    return redirect(f"/name/{name}")


@app.route("/secret", methods=["GET", "POST"])
def secret():
    """
    A secret
    """
    return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
