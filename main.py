#!/usr/bin/env python3

from time import sleep

from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ChromeOptions

PROFESSOR = "Alberto Cano"

options = ChromeOptions()
# options.add_argument('headless')
browser = Chrome(options=options)
browser.get("http://scholar.google.com")

search = browser.find_element_by_name("q")

search.send_keys(PROFESSOR)
search.send_keys(Keys.RETURN)


# TODO: Go through and print the titles of all of the articles on the page

link = browser.find_element_by_link_text(PROFESSOR)
link.click()

titles = browser.find_elements_by_class_name("gsc_a_at")

for title in titles:
    print("Article:", title.text)
    print()


sleep(2)

browser.quit()
