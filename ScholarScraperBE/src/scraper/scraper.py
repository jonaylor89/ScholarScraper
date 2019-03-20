#!/usr/bin/env python3

import json
import logging
from time import sleep
from typing import List

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions

# TODO: Make this not shit

CS_DEPARTMENT_RESEARCHERS: List[str] = [
    "Irfan Ahmed",
    "Tomasz Arodz",
    "Caroline Budwell",
    "Eyuphan Bulut",
    "Alberto Cano",
    "Krzysztof Cios",
    "Robert Dahlberg",
    "Kostadin Damevski",
    "Thang Dinh",
    # "Debra Duke",
    "Carol Fung",
    "Preetam Ghosh"
    "Vojislav Kecman",
    "Bartosz Krawczyk",
    "Lukasz Kurgan",
    "John D. Leonard II",
    "Changqing Luo",
    "Milos Manic",
    "Bridget McInnes",
    "Tamer Nadeem",
    # "Zachary Whitten",
    "Tarynn Witten",
    "Cang Ye",
    "Hong-Sheng Zhou",
]


class ScholarScraper(object):
    def __init__(self):
        """
        Initialize logging and start the browser
        """

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        self.temp_dict = {}

    def __enter__(self):
        """
        Returns browser on google scholar for Context Manager
        """

        options = ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.browser = Chrome(options=options)
        self.logger.info("connect to selenium server")


        return self.browser

    def __exit__(self, type, value, tb):
        """
        Used by Context Manager to exit the browser
        """

        self.quit()

    def quit(self):
        """
        Seperate method in case we don't want to use the Context Manager
        """

        self.browser.quit()

    def parse_by_name(self, name: str):
        """
        Parse information about a single researcher by their name
        """
        self.browser.get("https://scholar.google.com")
        self.logger.info("retrieving website")

        self.temp_dict[name] = {}

        # Grab the search bar
        search = self.browser.find_element_by_name("q")

        try:
            # Enter the researcher's nam and hit `ENTER/RETURN`
            search.send_keys(name)
            search.send_keys(Keys.RETURN)

            ############################################################################
            # Error handling here would be awesome
            # If a name can't be found or is formatted differently in the html
            # Then the program shouldn't crash
            ############################################################################

            # Find the researcher's name out of the search results
            link = self.browser.find_element_by_link_text(name)
            link.click()

            # Click the `SHOW MORE` button at the bottom of the page
            show_more = self.browser.find_element_by_id("gsc_bpf_more")
            show_more.click()

            sleep(2)  # Sleep to allow everything to load

            # Grab all articles from researcher
            titles = self.browser.find_elements_by_class_name("gsc_a_at")

            self.logger.info(f"titles for author: {len(titles)}")

            # Loop through all articles for the researcher
            for title in titles:

                # Add the publication as a key to the dictionary
                self.temp_dict[name][title.text] = self.parse_article_and_citations(title)

                # Go back to grab the next article
                self.browser.back()
                sleep(1)

            # End of publication parsing

            self.logger.info("parsing complete")
        except:
            self.logger.error(f"error with researcher {name}")

    def parse_article_and_citations(self, article_link):
        """
        Grab the fields and values from a publication 
        It might be possible to have the html for the article inputed instead of the link
        This would allow things to be parallelized without being kicked out by google
        
        This function differs from `parse_article()` because it does grab citations
        """
        # Add the publication as a key to the dictionary
        article_dict = {}

        # Click the title to get the information about the publication
        article_link.click()

        self.logger.info(f"entering article ({article_link.text})")

        sleep(1)  # Sleep to give google scholar some space to breath

        # Grab all fields about the publication
        fields = self.browser.find_elements_by_class_name("gsc_vcd_field")
        values = self.browser.find_elements_by_class_name("gsc_vcd_value")

        self.logger.info(f"there are {len(fields)} fields to parse")

        # Zip fields and values to add them to the dictionary
        for k, v in zip(fields, values):
            if k.text == "Authors":
                # Serialize string of names to list
                article_dict[k.text] = v.text.split(", ")
            elif k.text == "Total citations":
                # This is hacky parsing, it can be done better for sure
                article_dict[k.text] = int(v.text.split("\n")[0].split(" ")[2])

                # Click on the link for total citations to parse the citations
                article_dict["Citation Titles"] = self.parse_citations()

            else:
                article_dict[k.text] = v.text
            self.logger.info(f"parsed : {k.text} : {v.text}")

        return article_dict

    def parse_citations(self):
        """
        Go through every article on the page and grab the necessary information
        """

        return "Nothing yet"

    def parse_article(self):
        """
        Grab the information about an article but NOT the citations
        """
        pass


if __name__ == "__main__":

    scraper: ScholarScraper = ScholarScraper()
    with scraper:
        """
        Context manager to handle opening and closing of browser
        """

        # I would love to parallelize this but I really don't want google scholar to block me out
        for name in CS_DEPARTMENT_RESEARCHERS:
            scraper.parse_by_name(name)

        with open("data.json", "w") as f:
            f.write(json.dumps(scraper.temp_dict))
