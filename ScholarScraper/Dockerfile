
FROM python:3.7

# Install python dependencies
RUN pip3 install pipenv

WORKDIR /usr/src/app

COPY Pipfile ./
COPY Pipfile.lock ./

RUN set -ex && pipenv install --deploy --system

COPY . .

# Command to execute scraper
CMD ["python", "src/main.py"]