#!/usr/bin/env python3

from time import sleep

from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ChromeOptions

options = ChromeOptions()
# options.add_argument('headless')
browser = Chrome(options=options)
browser.get("http://scholar.google.com")

search = browser.find_element_by_name("q")

search.send_keys("Alberto Cano")
search.send_keys(Keys.RETURN)


# TODO: Go through and print the titles of all of the articles on the page


sleep(5)

browser.quit()
