#!/usr/bin/env python3

from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

option = Options()
option.headless = True
browser = Firefox(options=option)
browser.get("http://scholar.google.com")

search = browser.find_element_by_name("q")

search.send_keys("Alberto Cano")
search.send_keys(Keys.RETURN)


# TODO: Go through and print the titles of all of the articles on the page

print(browser.page_source)

browser.quit()
