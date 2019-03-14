#!/usr/bin/env bash

# Install dependencies
npm install

# Build angular project
ng build

# Serve site
ng serve --host=0.0.0.0
