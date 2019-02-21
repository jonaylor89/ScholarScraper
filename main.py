#!/usr/bin/env python3

import sys
from time import sleep

from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ChromeOptions


PROFESSOR = "Alberto Cano"


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        PROFESSOR = ' '.join(sys.argv[1:])

    options = ChromeOptions()
    # options.add_argument('headless')
    browser = Chrome(options=options)
    browser.get("http://scholar.google.com")

    search = browser.find_element_by_name("q")

    search.send_keys(PROFESSOR)
    search.send_keys(Keys.RETURN)

    link = browser.find_element_by_link_text(PROFESSOR)
    link.click()

    show_more = browser.find_element_by_id("gsc_bpf_more")
    show_more.click()

    sleep(5)

    titles = browser.find_elements_by_class_name("gsc_a_at")
    authors = browser.find_elements_by_class_name("gs_grey")
    cited_by = browser.find_elements_by_class_name("gsc_a_ac gs_ibl")

    for title, author, cited in zip(titles, authors, cited_by):
        print("Article:", title.text)
        print("Author(s):", author)
        print("Cited By:", cited)
        print()


    # TODO: Click on the links and print Author, Date, Journal, Decriptions, and Total Citations

    sleep(1)

    browser.quit()
