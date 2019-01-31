#!/usr/bin/env python3

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

option = Options()
option.headless = True
browser = Firefox(options=option)
browser.get('http://scholar.google.com')

print(browser.title)

browser.quit()
