#!/usr/bin/env bash

pipenv run gunicorn -b0.0.0.0:8000 src.main:app
