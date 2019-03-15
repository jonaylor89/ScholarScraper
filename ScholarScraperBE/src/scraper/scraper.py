#!/usr/bin/env python3

import json
import logging
from time import sleep

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Remote
from selenium.webdriver import ChromeOptions

# TODO: Make scraper a class
# TODO: And not shit

def parse_by_name(professor="Alberto Cano", filename="data.json"):

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    temp_dict = {professor: {}}

    options = ChromeOptions()
    options.add_argument("headless")
    browser = Remote(
        command_executor="http://localhost:4444/wd/hub",
        desired_capabilities=DesiredCapabilities.FIREFOX,
    )

    logger.info("connected to selenium server")

    browser.get("http://scholar.google.com")
    logger.info("retrieving website")

    search = browser.find_element_by_name("q")

    search.send_keys(professor)
    search.send_keys(Keys.RETURN)

    link = browser.find_element_by_link_text(professor)
    link.click()

    show_more = browser.find_element_by_id("gsc_bpf_more")
    show_more.click()

    sleep(3)

    titles = browser.find_elements_by_class_name("gsc_a_at")

    logger.info("titles for author: {0}".format(len(titles)))

    for title in titles:
        temp_dict[professor][title.text] = {}
        title.click()

        logger.info("entering article ({0})".format(title.text))
        print("entering article ({0})".format(title.text))

        sleep(1)

        fields = browser.find_elements_by_class_name("gsc_vcd_field")
        values = browser.find_elements_by_class_name("gsc_vcd_value")

        logger.info("there are {0} fields to parse".format(len(fields)))

        for k, v in zip(fields, values):
            if k.text == "Authors":
                temp_dict[professor][title.text][k.text] = v.text.split(", ")
            elif k.text == "Total citations":
                # This is hacky parsing, it can be done better for sure
                temp_dict[professor][title.text][k.text] = int(
                    v.text.split("\n")[0].split(" ")[2]
                )
            else:
                temp_dict[professor][title.text][k.text] = v.text
            logger.info("parsed : {0} : {1}".format(k.text, v.text))

        browser.back()
        sleep(1)

    with open(filename, "w+") as f:
        f.write(json.dumps(temp_dict))
    sleep(1)

    browser.quit()


if __name__ == "__main__":
    parse_by_name()
