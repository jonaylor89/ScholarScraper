
# Change directory to backend
cd ScholarScraperBE/

# Build backend image
docker build --tag=scholarscraperbe .

# Create backend container and run in the background on port 8000
docker run -p 8000:8000 scholarscraperbe -b

# Change directory to the frontend
cd ../ScholarScraperFE

# Build frontend
ng build

# Serve dev frontend on port 4200
ng serve

