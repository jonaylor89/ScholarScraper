#!/usr/bin/env bash

# Change directory to backend
cd ScholarScraperBE/

# Build backend image
docker build --tag=scholarscraperbe .

# Create backend container and run in the background on port 8000
docker run -d -p 8000:8000 scholarscraperbe 

# Change directory to the frontend
cd ../ScholarScraperFE

# Build frontend image
docker build --tag=scholarscraperfe .

# Serve dev frontend on port 4200
docker run -d -p 4200:4200 scholarscraperfe

# Change directory back to root of project
cd ..

