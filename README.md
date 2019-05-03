-> # ScholarScraper <-
-> 508 Database theory project <-

-------------

# Frontend

**So far the only thing I've done to the frontend is bootstrap the angular app and set the api url to point to the backend**

- Typescript
- Angular

For a front-end I'll let Russia handle that because of her experience with Angular.
It shouldn't be a hard front-end so nothing crazy beautiful. If we do have time and
want to go extra than we can have a page that displays a graph of the names of papers
with citations among them. As well as something to work with backend and front end routes.

-------------

# Backend

**The api package is in the process of setting up and building the database**

- Flask
- SQL Alchemy
- BeautifulSoup4

The api as of now is really just a glorified web scraper than can scrape google scholar for information on reserachers and publications.

--------------

# Execution

## Requirements

**On macOS with Homebrew**
```
~$ brew cask install docker
```

**On Ubuntu**
```
~$ sudo apt install docker
```

**On Arch**
```
~$ sudo pacman -S docker
```

To execute both the frontend and backend on your local machine for development,
just run:

```
~$ docker-compose up
```

To run either the frontend or backend individually
check the *README.md* in their repective directory.

------------------------




