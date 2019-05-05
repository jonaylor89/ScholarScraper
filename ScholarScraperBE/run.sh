#!/usr/bin/env bash

# Install dependencies
pipenv install

# Reminder
printf "+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+\n"
printf "+= MAKE SURE THE ENVIRONMENT VARIABLES ARE SET =+\n"
printf "+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+\n"

# Serve API
pipenv run gunicorn -b0.0.0.0:8000 src.main:app
