#!/usr/bin/env python3

import json
import logging
from time import sleep
from random import randint
from typing import List, Dict

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions

# TODO: Make this not shit


class ScholarScraper(object):
    def __init__(self) -> None:
        """
        Initialize logging and start the browser
        """

        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            filename="scraper.log",
            filemode="w",
            format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
            datefmt="%H:%M:%S",
            level=logging.INFO,
        )

        self.cs_researchers: List[str] = [
            "Irfan Ahmed",
            "Tomasz Arodz",
            # "Caroline Budwell",
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

        self.home_url = "https://scholar.google.com"
        self.researcher_dict = {}

    def __enter__(self) -> Chrome:
        """
        Returns browser on google scholar for Context Manager
        """

        options = ChromeOptions()

        # Show chrome during for debugging
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.browser = Chrome(options=options)
        self.logger.info("connect to selenium server")

        return self.browser

    def __exit__(self, type, value, tb) -> None:
        """
        Used by Context Manager to exit the browser
        """

        self.quit()

    def quit(self) -> None:
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
        self.browser.get(self.home_url)
        sleep(1)

    def parse_researcher(self, name: str) -> Dict:
        """
        Create new researcher
        """

        # Go to google scholar start screen
        self.goto_start()

        # Grab the search bar
        search = self.browser.find_element_by_name("q")

        # Profession error handling that just catches everything
        try:
            # Enter the researcher's name and hit `ENTER/RETURN`
            search.send_keys(name)
            search.send_keys(Keys.RETURN)

            # Find the researcher's name out of the search results
            link = self.browser.find_element_by_link_text(name)
            link.click()

        except:
            self.logger.error(f"researcher {name} could not be found")
            self.researcher_dict[name] = {}
            return

        sleep(randint(1, 3))

        self.researcher_dict[name] = {}

        try:
            self.logger.info(f"creating researcher {name} from scratch")
            self.researcher_dict[name]["id"] = self.parse_id()
            self.researcher_dict[name]["citation_count"] = self.citation_count()
            self.researcher_dict[name]["articles"] = self.parse_articles()
        except Exception as e:
            self.logger.error(f"could not create researcher {name} from scratch: {e}")
            self.researcher_dict[name] = {}

    def check_researcher(self, name: str, prev: Dict) -> None:
        """
        Used to check if a researcher needs undating and automatically does so if needed
        """
        # Go to google scholar start screen
        self.goto_start()

        # Grab the search bar
        search = self.browser.find_element_by_name("q")

        # Profession error handling that just catches everything
        try:
            # Enter the researcher's name and hit `ENTER/RETURN`
            search.send_keys(name)
            search.send_keys(Keys.RETURN)

            # Find the researcher's name out of the search results
            link = self.browser.find_element_by_link_text(name)
            link.click()

        except:
            self.logger.error(f"researcher {name} could not be found")
            return

        sleep(randint(1, 3))

        cur_citations = self.citation_count()

        self.logger.info(
            f"current citation count is {cur_citations} vs the old of {prev['citation_count']}"
        )

        if cur_citations != prev["citation_count"]:
            self.logger.info(
                f"change in citation count for {name}, updating researcher"
            )
            self.researcher_dict[name]["id"] = prev["id"]
            self.researcher_dict[name]["citations_count"] = cur_citations
            self.researcher_dict[name]["articles"] = self.parse_articles(name)
        else:
            self.logger.info(f"citation count for {name} has remained constant")
            self.researcher_dict[name] = prev

    def parse_articles(self) -> Dict:
        """
        Parse information about a single researcher by their name

        [!!!] Assumed to already be on the researcher's page

        TODO: Just download the html and use scraPY rather than selenium scraping

        """

        sleep(randint(1, 3))

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
        articles_dict = {}

        # Loop through all articles for the researcher
        for title in titles:

            # Add the publication as a key to the dictionary
            articles_dict[title.text] = self.parse_article(title)

        # End of publication parsing

        self.logger.info("parsing complete")

        return articles_dict

    def parse_id(self) -> int:
        """
        parse the id for a researcher

        [!!!] Assumed to be on the researcher's page
        """

        parameters = self.get_url_parameters()

        if "user" in parameters:
            scholar_id = parameters[parameters.index("user") + 1]
            self.logger.debug(f"scholar id is {scholar_id}")

            return scholar_id

        else:
            self.logger.error("`user` not in parameters")
            return ""

    def get_url_parameters(self) -> List[str]:
        """
        parse the keywords in the parameters of the url and put them in a python list
        """
        url = self.browser.current_url
        return url[url.find("?") + 1 :].replace("&", "=").split("=")

    def check_article(self, article_link) -> None:
        """
        Check if an article's citation number has changed and parse it if it has
        """
        pass

    def parse_article(self, article_link) -> Dict:
        """
        Grab the fields and values from a publication 
        It might be possible to have the html for the article inputed instead of the link
        This would allow things to be parallelized without being kicked out by google
        """

        # Add the publication as a key to the dictionary
        article_dict = {}

        sleep(randint(2, 4))

        try:
            # Click the title to get the information about the publication
            article_link.click()
            self.logger.debug(f"entering article ({article_link.text})")
        except Exception as e:
            self.logger.error(f"article `{article_link.text}` could not be clicked on")
            self.browser.back()
            sleep(randint(1, 3))
            return {}

        sleep(randint(1, 3))  # Sleep to give google scholar some space to breath

        try:
            # Grab all fields about the publication
            fields = self.browser.find_elements_by_class_name("gsc_vcd_field")
            values = self.browser.find_elements_by_class_name("gsc_vcd_value")

        except:
            self.logger.error(f"couldn't grab field tags for {article_link.text}")
            self.browser.back()
            sleep(1)
            return {}

        self.logger.debug(f"there are {len(fields)} fields to parse")

        # Zip fields and values to add them to the dictionary
        for k, v in zip(fields, values):
            try:

                if k.text == "Total citations":

                    # Getting the xpath for the cited by link
                    # cited_by_link = self.browser.find_elements_by_xpath(
                    #   "/html/body/div/div[8]/div/div[2]/div/div/div[2]/form/div[2]/div[9]/div[2]"
                    # )

                    # This is hacky parsing, it can be done better for sure
                    article_dict[k.text] = int(v.text.split("\n")[0].split(" ")[2])

                    # Get href from link
                    article_id_url = v.get_attribute("href")

                    article_dict["id"] = self.parse_article_id(article_id_url)

                    # Click on the link for total citations to parse the citations
                    # article_dict["Citation Titles"] = self.parse_citations()

                    sleep(randint(3, 5))

                elif k.text == "Publication date":
                    article_dict[k.text] = v.text

            except:
                self.logger.error(f"field parsing error on {k.text}")
                self.browser.back()
                sleep(1)
                article_dict[k.text] = {}

            self.logger.debug(f"parsed : {k.text} : {v.text}")

        # Go back to grab the next article
        self.browser.back()
        sleep(randint(1, 3))

        return article_dict

    def parse_article_id(self, href: str) -> str:
        """
        Parse the article id from the href url
        """
        article_id_parameters = self.get_url_parameters(href)

        # The id is in the parameters of the link
        if "cites" in article_id_parameters:
            article_id = article_id_parameters[parameters.index("cites") + 1]
            self.logger.debug(f"article id is {article_id}")

            return article_id
        else:
            self.logger.error("`cites` not in parameters")
            return ""

    def parse_citations(self) -> List[str]:
        """
        Grab the titles of citations of a specific article from google scholar
        """

        sleep(randint(1, 3))

        try:
            citation_link = self.browser.find_element_by_xpath(
                "/html/body/div/div[8]/div/div[2]/div/div/div[2]/form/div[2]/div[9]/div[2]/div[1]/a"
            )
        except:
            self.logger.error("couldn't grab citation link")
            return []

        try:
            citation_link.click()

        except:
            self.logger.error("citations could not be clicked")
            return []

        sleep(randint(1, 3))

        try:
            citation_list = self.browser.execute_script(
                """
                            let list= document.getElementsByClassName("gs_rt"); 
                            let arr = [];
                            for (var i = 0; i < list.length; i++) {
                                arr.push(list[i].lastChild.firstChild.data);
                            }   

                            return arr;
                        """
            )
        except:
            self.logger.error("couldn't get citation titles")
            self.browser.back()
            return []

        sleep(1)

        self.browser.back()

        return citation_list

    def citation_count(self) -> int:
        """
        identify how many total citations a researcher has 
        """

        sleep(randint(1, 3))

        citation_data = None
        total_citations = 0

        try:
            # citation_data = self.browser.find_elements_by_xpath("/html/body/div/div[14]/div[2]/div/div[1]/div[1]/table/tbody/tr[1]/td[2]")
            citation_data = self.browser.execute_script(
                """
                                    function getElementByXpath(path) {
                                        return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                                    }

                                    return getElementByXpath("/html/body/div/div[14]/div[2]/div/div[1]/div[1]/table/tbody/tr[1]/td[2]").lastChild.data
                                """
            )

        except:
            self.logger.error("couldn't find cited by table")
            return 0

        total_citations = int(citation_data)
        self.logger.debug(f"{total_citations} citations in total")

        return total_citations


def main() -> None:

    scraper = ScholarScraper()

    with scraper:
        """
        Context manager to handle opening and closing of browser
        """
        researcher_data = None

        with open("data.json") as f:

            try:
                # Get `database`
                researcher_data = json.load(f)
            except Exception as e:
                # Something happened to the `database`
                scraper.logger.error(f"database is missing? {e}")

        # Go through all names
        for name in scraper.cs_researchers:

            # Five attempts to parse the page because it can be janky
            n = 5
            while n > 0:
                n -= 1
                try:

                    if researcher_data is not None:
                        try:
                            researcher = researcher_data[name]
                            scraper.check_researcher(name, researcher)
                        except:
                            researcher = {}
                            scraper.parse_researcher(name)
                    else:
                        scraper.parse_researcher(name)

                    break  # Successful attempt
                except Exception as e:
                    scraper.logger.error(
                        f"failed to parse researcher, {n} attempt(s) left: {e}"
                    )

                sleep(2)

            if n == 0:
                print("scraping failed")
                exit(1)

            sleep(randint(1, 3))

        with open("data.json", "w+") as f:
            f.write(json.dumps(scraper.researcher_dict, indent=2))


if __name__ == "__main__":
    main()
