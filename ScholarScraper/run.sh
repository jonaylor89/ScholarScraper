#!/usr/bin/env bash

# Reminder
printf "+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\n"
printf "+= MAKE SURE THE ENVIRONMENT VARIABLE DB_PASSWORD IS SET =+\n"
printf "+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\n"

pipenv install

pipenv run python src/main.py
