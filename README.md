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
- SQL
- Selenium

The api as of now is really just a glorified web scraper than can scrape google scholar for information on reserachers and publications.
Storing results, serializing and deserializing, fancy routing is still in the process of being developed. Slowly but surely.
I've been carried away with making deployment beautiful. (It is for anyone asking)

The web scraper is on and off. Because of the importance of the reliability of this component of the application, I'll be doing
major restructuring and refactoring to make it cleaning and then improve the reliability of it all.

--------------

# Execution

## Requirements

On macOS with Homebrew
```
~$ brew cask install docker
```

On Ubuntu
```
~$ sudo apt install docker
```

On Arch
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

--------------

# TODO

1. Count and log the number of citations and by which publications to a specific publication.
2. Reorganize the database to be more accurate and correct. (ASAP)
3. Make the web scraping a CRON job on the CMSC 508 server. (ASAP)
4. Design upgraded web scraper




