#!/usr/bin/env python3

import json
import logging
from .scraper import scraper
from flask_cors import CORS
from flask import Flask

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "WELCOME TO SCHOLAR SCRAPER!"


@app.route("/name/<name>", methods=["GET"])
def parse_by_name(name: str):

    json_data = ""

    with open("data.json", "r") as f:
        json_data = json.loads(f.read())

    if name not in json_data.keys():
        scraper.parse_by_name(name)

        with open("data.json", "r") as f:
            json_data = json.loads(f.read())

    return json.dumps(json_data[name], indent=2)
