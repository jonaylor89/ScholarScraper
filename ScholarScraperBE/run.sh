#!/usr/bin/env bash

# Install dependencies
pipenv install

# Serve API
pipenv run gunicorn -b0.0.0.0:8000 src.main:app
