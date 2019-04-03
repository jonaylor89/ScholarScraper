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

## CRON job

Our script for scraping google scholar is set up as a CRON job to run at noon everyday.

To edit CRON jobs
```sh
~$ crontab -e
```

CRON is formatted like so
```
 +---------------- minute (0 - 59)
 |  +------------- hour (0 - 23)
 |  |  +---------- day of month (1 - 31)
 |  |  |  +------- month (1 - 12)
 |  |  |  |  +---- day of week (0 - 6) (Sunday=0 or 7)
 |  |  |  |  |
 *  *  *  *  *  command to be executed
 ```

 Our CRON job to run at 1pm everyday is:
 ```
0 13 * * * /usr/local/bin/python3.7 /usr/src/app/src/scraper/scraper.py
 ```

 ---------------------------



