#!/usr/bin/env python3

import logging
from scraper import scraper

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("Initializing logger and parsing")


    scraper.parse_by_name()
