#!/usr/bin/env python3

import json
import logging
from time import sleep
from typing import List, Dict
from random import randint

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions

# TODO: Make this not shit

HOME_URL = "https://scholar.google.com"

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
        logging.basicConfig(filename='scraper.log',
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)

        self.researcher_dict = {}

    def __enter__(self):
        """
        Returns browser on google scholar for Context Manager
        """

        options = ChromeOptions()
        
        # Show chrome during for debugging
        # options.add_argument("--headless")
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

    def goto_start(self) -> None:
        """
        Go to the google scholar home page
        """

        sleep(1)
        self.logger.info("retrieving google scholar website")
        self.browser.get(HOME_URL)
        sleep(1)


    def parse_researcher(self, name: str) -> Dict:
        """
        Parse information about a single researcher by their name
        """

        # Go to google scholar start screen
        self.goto_start()

        temp_dict = {}

        # Grab the search bar
        search = self.browser.find_element_by_name("q")

        # Profession error handling that just catches everything
        try:
            # Enter the researcher's nam and hit `ENTER/RETURN`
            search.send_keys(name)
            search.send_keys(Keys.RETURN)

            # Find the researcher's name out of the search results
            link = self.browser.find_element_by_link_text(name)
            link.click()

        except:
            self.logger.error("researcher could not be found")
            return {}

        sleep(randint(1, 3))

        # Get the total number of citations for a researcher
        cit_count = self.citation_count()
        temp_dict["citation count"] = cit_count

        # Click the `SHOW MORE` button at the bottom of the page
        show_more = self.browser.find_element_by_id("gsc_bpf_more")
        
        # Show more until the button is disabled
        count = 0
        while show_more.is_enabled():
            show_more.click()
            count += 1

        self.logger.debug(f"show more was pressed {count} times")

        sleep(2)  # Sleep to allow everything to load

        # Grab all articles from researcher
        titles = self.browser.find_elements_by_class_name("gsc_a_at")

        self.logger.debug(f"titles for author: {len(titles)}")

        # Create article section
        temp_dict["articles"] = {}

        # Loop through all articles for the researcher
        for title in titles:

            # Add the publication as a key to the dictionary
            temp_dict["articles"][title.text] = self.parse_article(title)


        # End of publication parsing

        self.logger.info("parsing complete")

        return temp_dict

    def parse_article(self, article_link) -> Dict:
        """
        Grab the fields and values from a publication 
        It might be possible to have the html for the article inputed instead of the link
        This would allow things to be parallelized without being kicked out by google
        """

        # Add the publication as a key to the dictionary
        article_dict = {}

        try:
            # Click the title to get the information about the publication
            article_link.click()
            self.logger.info(f"entering article ({article_link.text})")
        except:
            self.logger.error(f"article `{article_link.text}` could not be clicked on")
            return {}

        sleep(1 + randint(1, 3))  # Sleep to give google scholar some space to breath

        try:
            # Grab all fields about the publication
            fields = self.browser.find_elements_by_class_name("gsc_vcd_field")
            values = self.browser.find_elements_by_class_name("gsc_vcd_value")

        except:
            self.logger.error(f"couldn't grab field tags for {article_link.text}")
            return {}

        self.logger.debug(f"there are {len(fields)} fields to parse")

        # Zip fields and values to add them to the dictionary
        for k, v in zip(fields, values):
            try:

                if k.text == "Authors":
                    # Serialize string of names to list
                    article_dict[k.text] = v.text.split(", ")
                elif k.text == "Total citations":

                    cited_by_link = self.browser.find_elements_by_xpath("/html/body/div/div[8]/div/div[2]/div/div/div[2]/form/div[2]/div[9]/div[2]")

                    # This is hacky parsing, it can be done better for sure
                    article_dict[k.text] = int(v.text.split("\n")[0].split(" ")[2])

                    # Click on the link for total citations to parse the citations
                    # article_dict["Citation Titles"] = self.parse_citations()

                else:
                    article_dict[k.text] = v.text

            except:
                self.logger.error(f"field parsing error on {k.text}")
                article_dict[k.text] = {}

            self.logger.debug(f"parsed : {k.text} : {v.text}")

        # Go back to grab the next article
        self.browser.back()
        sleep(randint(1, 3))

        return article_dict

    def parse_citations(self, citation_link):

        sleep(1)

        try:
            citation_link.click()
            # self.browser.back()
        except:
            self.logger.error("citations could not be clicked")

        return []

    def citation_count(self) -> int:
        """
        identify how many total citations a researcher has 
        """
        citation_data = None
        total_citations = 0

        try:
            # citation_data = self.browser.find_elements_by_xpath("/html/body/div/div[14]/div[2]/div/div[1]/div[1]/table/tbody/tr[1]/td[2]")
            citation_data = self.browser.execute_script("""
                                    function getElementByXpath(path) {
                                        return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                                    }

                                    return getElementByXpath("/html/body/div/div[14]/div[2]/div/div[1]/div[1]/table/tbody/tr[1]/td[2]").lastChild.data
                                """)

        except:
            self.logger.error("couldn't find cited by table")
            return 0


        total_citations = int(citation_data)
        self.logger.debug(f"{total_citations} citations in total")

        return total_citations

if __name__ == "__main__":

    scraper: ScholarScraper = ScholarScraper()
    with scraper:
        """
        Context manager to handle opening and closing of browser
        """

        # Five attempts to parse the page because it can be janky
        n = 5
        while n > 0:
            n -= 1
            try:
                scraper.researcher_dict["Bartosz Krawczyk"] = scraper.parse_researcher("Bartosz Krawczyk")
                break
            except Exception as e:
                print(e)
                print(f"Failed to parse researcher, {n} attempt(s) left")

            sleep(2)

        if n == 0:
            print("scraping failed") 
            exit(1)
        
        """
        # I would love to parallelize this but I really don't want google scholar to block me out
        for name in CS_DEPARTMENT_RESEARCHERS:
            scraper.researcher_dict[name] = scraper.parse_researcher(name)
            sleep(2 + randint(-1, 3))
        """

        with open("data.json", "w+") as f:
            f.write(json.dumps(scraper.researcher_dict, indent=2))
