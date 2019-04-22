#!/usr/bin/env python3

import json
import logging
from time import sleep
from random import randint, shuffle
from datetime import datetime
from typing import List, Dict

from selenium.webdriver import Chrome
from selenium.webdriver import Firefox
from selenium.webdriver import ChromeOptions
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.remote_connection import LOGGER as slog
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# TODO: Make this not shit (i.e. Refactor the hell out of this)

# I could probably break this up into smaller classes like
# one class for researchers, one for articles, one for citations
# because right now this big guy is disgusting.

# I just want it to work right now


class ScholarScraper(object):
    def __init__(self) -> None:
        """
        Initialize logging and set everything up
        """

        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            filename="scraper.log",
            filemode="w",
            format="%(asctime)s %(name)s %(levelname)s %(message)s",
            datefmt="%H:%M:%S",
            level=logging.DEBUG,
        )

        # Silence these guys
        slog.setLevel(logging.ERROR)
        logging.getLogger("requests").setLevel(logging.ERROR)
        logging.getLogger("urllib3").setLevel(logging.ERROR)

        self.cs_researchers: List[str] = [
            "Irfan Ahmed",
            "Tomasz Arodz",
            "Eyuphan Bulut",
            "Alberto Cano",
            "Krzysztof J Cios",
            "Kostadin Damevski",
            "Thang N. Dinh",
            "Carol Fung",
            "preetam ghosh",
            "Vojislav Kecman",
            "Bartosz Krawczyk",
            "Lukasz Kurgan",
            "John D. Leonard II",
            "Changqing Luo",
            "Milos Manic",
            "Bridget T. McInnes",
            "Tamer Nadeem",
            "Tarynn M Witten",
            "Cang Ye",
            "Hong-Sheng Zhou",
        ]

        self.home_url = "https://scholar.google.com"
        self.researcher_dict: Dict = {}

    def __enter__(self) -> Chrome:
        """
        Returns browser on google scholar for Context Manager
        """

        # randomly choose firefox or chrome
        if randint(1, 1):  # Should be randint(0, 1) in prod
            options = ChromeOptions()

            # Show chrome during for debugging
            # options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

            self.browser = Chrome(options=options)

        else:
            options = Options()

            # show firefox during debugging
            # options.add_argument('-headless')

            self.browser = Firefox(options=options)

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
        self.logger.debug("retrieving google scholar website")
        self.browser.get(self.home_url)
        sleep(1)

    def parse_researcher(self, name: str) -> None:
        """
        Parse new researcher
        """

        # Go to google scholar start screen
        self.goto_start()

        # Grab the search bar
        search = self.browser.find_element_by_name("q")

        # Profession error handling that just catches everything
        try:
            # Enter the researcher's name and hit `ENTER/RETURN`
            search.send_keys(name)
            sleep(randint(1, 2))
            search.send_keys(Keys.RETURN)

            # Find the researcher's name out of the search results
            link = self.browser.find_element_by_link_text(name)
            sleep(randint(1, 2))
            link.click()

        except:
            self.logger.error(f"researcher {name} could not be found")
            self.researcher_dict[name] = {}
            return

        sleep(randint(1, 3))

        self.researcher_dict[name] = {}

        try:
            self.logger.warning(f"creating researcher {name} from scratch")
            self.researcher_dict[name]["id"] = self.parse_id()
            self.researcher_dict[name]["date"] = str(datetime.now())
            self.researcher_dict[name]["citation_count"] = self.citation_count()
            self.researcher_dict[name]["articles"] = self.parse_articles()
        except Exception as e:
            self.logger.error(f"could not create researcher {name} from scratch: {e}")
            self.researcher_dict[name] = {}

    def check_researcher(self, name: str, prev: Dict) -> None:
        """
        Used to check if a researcher needs updating and automatically does so if needed
        """

        try:

            self.browser.get(
                f"https://scholar.google.com/citations?user={prev['id']}&hl=en&oi=ao"
            )

        except Exception as e:
            self.logger.error(f"researcher {name} could not be found: {e}")
            self.researcher_dict[name] = prev
            return

        sleep(randint(1, 3))

        cur_citations = self.citation_count()

        self.logger.info(
            f"current citation count is {cur_citations} vs the old of {prev['citation_count']}"
        )

        self.researcher_dict[name] = {}

        try:
            if cur_citations != prev["citation_count"]:
                self.logger.info(
                    f"change in citation count for {name}, updating researcher"
                )
                self.researcher_dict[name]["id"] = prev["id"]
                self.researcher_dict[name]["date"] = str(datetime.now())
                self.researcher_dict[name]["citation_count"] = cur_citations
                self.researcher_dict[name]["articles"] = self.check_articles(
                    prev["articles"]
                )
            else:
                self.logger.info(f"citation count for {name} has remained constant")
                self.researcher_dict[name] = prev
                self.researcher_dict[name]["date"] = str(datetime.now())

        except Exception as e:
            self.logger.error(
                f"couldn't properly check the researcher {name} because: {e}"
            )
            self.researcher_dict[name] = {}

    def parse_articles(self) -> Dict:
        """
        Parse information about a single researcher by their name

        [!!!] Assumed to already be on the researcher's page

        TODO: Just download the html and use scraPY rather than selenium scraping (parallel scraping perhaps?)

        """

        sleep(randint(1, 3))

        # Click the `SHOW MORE` button at the bottom of the page
        show_more = self.browser.find_element_by_id("gsc_bpf_more")

        # Show more until the button is disabled
        count = 0
        while show_more.is_enabled():
            show_more.click()
            count += 1

        sleep(2)  # Sleep to allow everything to load

        # Create article section
        articles_dict: Dict = {}

        # Grab all articles from researcher
        try:
            titles = self.browser.find_elements_by_class_name("gsc_a_at")
            self.logger.debug(f"titles for author: {len(titles)}")
        except:
            self.logger.error("couldn't get title from page")
            return articles_dict

        # Loop through all articles for the researcher
        try:
            for x in range(len(titles)):

                sleep(randint(1, 2))

                title = titles[x]

                # Add the publication as a key to the dictionary
                title_text = (
                    title.text
                )  # Temperary variable so I don't lose the webelement reference

                articles_dict[title_text] = self.parse_article(title, True)

                try:
                    # Click the `SHOW MORE` button at the bottom of the page
                    show_more = self.browser.find_element_by_id("gsc_bpf_more")

                    # Show more until the button is disabled
                    count = 0
                    while show_more.is_enabled():
                        show_more.click()
                        count += 1
                except Exception as e:
                    self.logger.error("error getting more articles")
                    return articles_dict

                try:
                    # Grab all articles from researcher
                    titles = self.browser.find_elements_by_class_name("gsc_a_at")
                    self.logger.debug(f"titles for author: {len(titles)}")

                except:
                    self.logger.error("couldn't get titles from page")
                    return articles_dict

        except Exception as e:
            self.logger.error(f"Something went wrong with parsing the articles: {e}")
            return articles_dict

        # End of publication parsing

        self.logger.info("parsing complete")

        return articles_dict

    def parse_id(self) -> str:
        """
        parse the id for a researcher

        [!!!] Assumed to be on the researcher's page
        """

        parameters = self.get_url_parameters(self.browser.current_url)

        if "user" in parameters:
            scholar_id = parameters[parameters.index("user") + 1]
            self.logger.debug(f"scholar id is {scholar_id}")

            return scholar_id

        else:
            self.logger.error("`user` not in parameters")
            return ""

    def get_url_parameters(self, url: str) -> List[str]:
        """
        parse the keywords in the parameters of the url and put them in a python list
        """
        return url[url.find("?") + 1 :].replace("&", "=").split("=")

    def check_articles(self, prev_articles: Dict) -> Dict:
        """
        Check if an articles citation number has changed and parse it if it has

        [!!!] Assumed to already be on the researcher's page

        TODO: Just download the html and use scraPY rather than selenium scraping (parallel scraping perhaps?)

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

        try:
            # Grab all articles from researcher (map them to their text and not the webelement)
            titles = self.browser.find_elements_by_class_name("gsc_a_at")

            # Grab all citations for the articles (map them to their text and not the webelement)
            citations = self.browser.find_elements_by_class_name("gsc_a_c")[2:]

        except Exception as e:
            self.logger.error(f"trouble grabbing the titles and citations: {e}")
            return prev_articles

        self.logger.info(f"titles for author: {len(titles)}")
        self.logger.info(f"cited titles for author: {len(citations)}")

        # Create article section
        articles_dict: Dict[str, Dict] = {}

        try:
            # Loop through all articles for the researcher
            for x in range(len(titles)):

                title = titles[x]
                citation_link = citations[x]

                # I have to make it weird like this because web attributes changed be changed
                if citation_link.text == "":
                    citation = "0"
                else:
                    citation = citation_link.text

                # Add the publication as a key to the dictionary
                try:
                    if int(citation) == prev_articles[title.text]["Total citations"]:
                        self.logger.debug(
                            f"article `{title.text}` has not changed citation count"
                        )
                        articles_dict[title.text]["Total citations"] = prev_articles[
                            title.text
                        ]["Total citations"]
                    else:
                        self.logger.info(
                            f"citation count for article `{title.text}` has changed {citation} vs {prev_articles[title.text]['Total citations']} before"
                        )
                        articles_dict[title.text] = self.parse_article(title, True)
                except Exception as e:
                    # title wasn't even in the old database
                    self.logger.warning(f"title `{title.text}` is new to the data: {e}")
                    articles_dict[title.text] = self.parse_article(title, True)

                # It has to be done every loop because webelements get lost every citation
                try:
                    # Grab all articles from researcher (map them to their text and not the webelement)
                    titles = self.browser.find_elements_by_class_name("gsc_a_at")

                    # Grab all citations for the articles (map them to their text and not the webelement)
                    citations = self.browser.find_elements_by_class_name("gsc_a_c")[2:]

                except Exception as e:
                    self.logger.error(f"trouble grabbing the titles and citations: {e}")
                    return prev_articles

        except Exception as e:
            self.logger.error(f"problem grabbing the data for articles: {e}")
            return prev_articles

        # End of publication parsing

        self.logger.info("parsing complete for articles")

        return articles_dict

    def parse_article(self, article_link, citations: bool) -> Dict:
        """
        Grab the fields and values from a publication 
        It might be possible to have the html for the article inputed instead of the link
        This would allow things to be parallelized without being kicked out by google
        """

        # Add the publication as a key to the dictionary
        article_dict: Dict = {}

        sleep(randint(2, 4))

        try:
            # Click the title to get the information about the publication
            article_link.click()
            self.logger.debug(f"entering article ({article_link.text})")
        except Exception as e:
            self.logger.error(
                f"article `{article_link.text}` could not be clicked on: {e}"
            )
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

        # Zip fields and values to add them to the dictionary
        for i in range(len(fields) - 1):  # I don't want the last element

            k = fields[i]
            v = values[i]

            try:

                if k.text == "Total citations":

                    # This is hacky parsing, it can be done better for sure
                    article_dict[k.text] = int(v.text.split("\n")[0].split(" ")[2])

                    if citations:  # Some articles we want citations and others we don't
                        # Get href from link
                        article_id_url = v.find_element_by_css_selector(
                            "a"
                        ).get_attribute("href")

                        if article_id_url is not None:
                            article_dict["id"] = self.parse_article_id(article_id_url)
                        else:
                            self.logger.error("couldn't get the url of the article")
                            article_dict["id"] = 0

                        # Click on the link for total citations to parse the citations
                        article_dict["Citation Titles"] = self.parse_citations(
                            article_link.text, v.find_element_by_css_selector("a")
                        )

                    sleep(randint(3, 4))

                    break

                elif k.text == "Publication date":
                    article_dict[k.text] = v.text

            except Exception as e:
                self.logger.error(f"field parsing error on field {k.text}: {e}")
                self.browser.back()
                sleep(1)
                article_dict[k.text] = {}

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
            article_id = article_id_parameters[article_id_parameters.index("cites") + 1]
            self.logger.debug(f"article id is {article_id}")

            return article_id
        else:
            self.logger.error("`cites` not in parameters")
            return ""

    def parse_citations(self, cited_title, citations_link) -> Dict[str, Dict]:
        """
        Grab the titles of citations of a specific article from google scholar
        """

        citations_dict: Dict[str, Dict] = {}

        sleep(randint(1, 3))

        try:
            citations_link.click()

        except:
            self.logger.error("citations could not be clicked")
            return {}

        sleep(randint(1, 3))

        citation_list: List = []
        authors_divs: List = []

        try:
            citation_list = self.browser.execute_script(
                """
                            return [...document.querySelectorAll('.gs_rt')].map(i => i.lastChild.firstChild.data);
                        """
            )[
                1:
            ]  # The first element is the original article so we just need the rest

        except Exception as e:
            self.logger.error(f"couldn't get citation titles: {e}")
            self.browser.back()
            return {}

        try:
            author_divs = self.browser.find_elements_by_class_name("gs_a")

        except:
            self.logger.error("couldn't get citation author")
            self.browser.back()
            return {}

        sleep(1)

        for x in range(len(citation_list)):

            citation = citation_list[x]
            author_div = author_divs[x]

            try:
                author_link = author_div.find_element_by_css_selector("a")
                citations_dict[citation] = self.parse_citation(
                    cited_title, citation, author_link
                )

                try:
                    citation_list = self.browser.execute_script(
                        """
                            return [...document.querySelectorAll('.gs_rt')].map(i => i.lastChild.firstChild.data);
                        """
                    )[
                        1:
                    ]  # The first element is the original article

                except:
                    self.logger.error("couldn't get citation titles again")
                    self.browser.back()
                    return {}

                try:
                    author_divs = self.browser.find_elements_by_class_name("gs_a")

                except:
                    self.logger.error("couldn't get citation author")
                    self.browser.back()
                    return {}

                sleep(1)

            except Exception as e:
                self.logger.warning(
                    f"Author for citation: <{citation}> could not be clicked, skipping..."
                )
                continue

                sleep(randint(1, 2))

        sleep(randint(1, 2))
        self.browser.back()

        return citations_dict

    def parse_citation(self, cited_title, citation, author_link) -> Dict:

        sleep(randint(2, 3))

        citation_dict: Dict = {}

        try:
            self.logger.debug(f"parsing citation author : {author_link.text}")
            author_link.click()

            sleep(randint(1, 2))

            try:
                # Click the `SHOW MORE` button at the bottom of the page
                show_more = self.browser.find_element_by_id("gsc_bpf_more")

                # Show more until the button is disabled
                count = 0
                while show_more.is_enabled():
                    show_more.click()
                    count += 1

            except Exception as e:
                self.logger.error("error getting more articles")
                self.browser.back()
                return citation_dict

            try:
                self.logger.debug(f"attempting to enter citation article: <{citation}>")

                # Grab the article that cited the target article
                citation_article = self.find_article_link(citation)

                if citation_article is None:
                    return citation_dict

                citation_dict = self.parse_article(
                    citation_article, False
                )  # The 'False' means we don't grab its citations

            except Exception as e:
                self.logger.error(f"couldn't get citation article from page: {e}")
                self.browser.back()
                return citation_dict

        except Exception as e:
            self.logger.error(f"{e}")
            return citation_dict

        self.browser.back()
        return citation_dict

    def find_article_link(self, search_title: str):
        """
        [!!!] Assumes the browser is on an author's page
        """

        sleep(randint(1, 2))

        # Grab all articles from researcher
        try:
            titles = self.browser.find_elements_by_class_name("gsc_a_at")
            self.logger.debug(f"titles for author: {len(titles)}")
        except:
            self.logger.error("couldn't get titles from page")
            return None

        # Loop through all articles for the researcher
        try:
            for title in titles:

                if title.text == search_title:
                    return title

            else:
                return None

        except Exception as e:
            self.logger.error(
                f"Something went wrong with parsing the citation author's articles: {e}"
            )
            return None

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

        # Shuffle list to confuse google bot detection
        shuffle(scraper.cs_researchers)

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
                        except KeyError as ke:
                            scraper.logger.warning(
                                f"researcher {name} not in existing data: {ke}"
                            )
                            researcher = {}
                            scraper.parse_researcher(name)
                        except Exception as e:
                            scraper.logger.error(f"error with researcher {name}: {e}")
                            scraper.researcher_dict[name] = {}
                    else:
                        scraper.logger.error(f"database not found parsing {name}")
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
