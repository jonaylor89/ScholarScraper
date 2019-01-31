
from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://seleniumhq.org/')

print(browser.title)

browser.quit()
