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
    "Preetam Ghosh",
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
        self.logger.setLevel(logging.INFO)

        self.temp_dict = {}

    def __enter__(self):
        """
        Returns browser on google scholar for Context Manager
        """

        options = ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.browser = Chrome(chrome_options=options)
        self.logger.info("connect to selenium server")

        self.browser.get("https://scholar.google.com")
        self.logger.info("retrieving website")

        return self.browser()

    def __exit__(self):
        """
        Used by Context Manager to exit the browser
        """

        self.quit()

    def quit(self):
        """
        Seperate method in case we don't want to use the Context Manager
        """

        self.browser.quit()

    def parse_by_name(self, name):
        """
        Parse information about a single researcher by their name
        """

        self.temp_dict[name] = {}

        search = self.browser.find_element_by_name("q")

        search.send_keys(name)
        search.send_keys(Keys.RETURN)

        link = self.browser.find_element_by_link_text(name)
        link.click()

        show_more = self.browser.find_element_by_id("gsc_bpf_more")
        show_more.click()

        sleep(3)

        titles = self.browser.find_elements_by_class_name("gsc_a_at")

        self.logger.info(f"titles for author: {len(titles)}")

        for title in titles:
            self.temp_dict[name][title.text] = {}
            title.click()

            self.logger.info(f"entering article ({title.text})")

            sleep(1)

            fields = self.browser.find_elements_by_class_name("gsc_vcd_field")
            values = self.rowser.find_elements_by_class_name("gsc_vcd_value")

            self.logger.info(f"there are {len(fields)} fields to parse")

            for k, v in zip(fields, values):
                if k.text == "Authors":
                    self.temp_dict[name][title.text][k.text] = v.text.split(", ")
                elif k.text == "Total citations":
                    # This is hacky parsing, it can be done better for sure
                    self.temp_dict[name][title.text][k.text] = int(
                        v.text.split("\n")[0].split(" ")[2]
                    )
                else:
                    self.temp_dict[name][title.text][k.text] = v.text
                self.logger.info(f"parsed : {k.text} : {v.text}")

            self.browser.back()
            sleep(1)

        self.logger.info("parsing complete")


if __name__ == "__main__":

    scraper: ScholarScraper = ScholarScraper()
    with scraper:
        """
        Context manager to handle opening and closing of browser
        """

        for name in CS_DEPARTMENT_RESEARCHERS:
            scraper.parse_by_name(name)

