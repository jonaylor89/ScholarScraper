#!/usr/bin/env python3

import sys
from time import sleep

from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ChromeOptions

# TODO: Use logging library instead of printing


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

    sleep(3)

    titles = browser.find_elements_by_class_name("gsc_a_at")

    print("[DEBUG] ", len(titles))

    for title in titles:
        title.click()

        print("[INFO] Entering article ({0})".format(title.text))

        sleep(1)
        
        fields = browser.find_elements_by_class_name("gsc_vcd_field")
        values = browser.find_elements_by_class_name("gsc_vcd_value")

        print("[DEBUG] There are {0} fields to parse".format(len(fields)))

        for k, v in zip(fields, values):
            print("[INFO] {0} : {1}".format(k.text, v.text))

        print("-----------------------")
        browser.back()
        sleep(1)

    sleep(1)

    browser.quit()
