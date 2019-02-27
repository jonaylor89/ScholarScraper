
# Backend

The backend is a flask application that, as of now, just runs a web scraper for google scholar.
For all things database the best library to use would be SqlAlchemy. It's good stuff.
The plan is to add some more routes with extra features and functionality once more detail
has been given about the project.


## Environment

I use `pipenv` to store the python dependencies.It works like npm to manage dependencies and installing.
Install pipenv and run:
```
~$ pipenv install
```

## Execution

To execute the app for testing and development, use the `run.sh` script

```sh
~$ ./run.sh
```
This will just run flask in the virtual environment, starting the server on port 8000


To execute on a server or in a production environment, build and run the docker image.

 *This requires docker obviously*

```sh
~$ docker build --tag=scholarscraper . 
~$ docker run -p 8000:8000 scholarscraper
```


