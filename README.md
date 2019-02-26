# ScholarScraper
508 Database theory project

For all things database the best library to use would be SqlAlchemy.
It's good stuff so that's the plan. For a front-end I'll let Russia handle that because of her experience with Angular. 
It shouldn't be a hard front-end so nothing crazy beautiful. 

# Execution

- To execute the app for testing and development, use the `run.sh` script

```sh
~$ ./run.sh
```

- To execute on a server or in a production environment, build and run the docker image
```sh
~$ docker build --tag=scholarscraper .
~$ docker run -p 8000:8000 scholarscraper
```

