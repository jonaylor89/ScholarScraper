#!/usr/bin/env python3

import json
import logging
from .scraper import scraper
from flask import Flask

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route("/")
def hello():
    return "WELCOME TO SCHOLAR SCRAPER!"


@app.route("/<name>", methods=["GET"])
def parse_by_name(name: str):

    # scraper.parse_by_name(name)

    json_data = ""

    with open("data.json", "r") as f:
        json_data = json.loads(f.read())

    return json.dumps(json_data[name], indent=2)
