#!/usr/bin/env python3

import json
from time import sleep

from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ChromeOptions

# TODO: Use logging library instead of printing

def parse_by_name(professor="Alberto Cano", filename="data.json"):

    temp_dict = {professor : {}}

    options = ChromeOptions()
    # options.add_argument('headless')
    browser = Chrome(options=options)
    browser.get("http://scholar.google.com")

    search = browser.find_element_by_name("q")

    search.send_keys(professor)
    search.send_keys(Keys.RETURN)

    link = browser.find_element_by_link_text(professor)
    link.click()

    show_more = browser.find_element_by_id("gsc_bpf_more")
    show_more.click()

    sleep(3)

    titles = browser.find_elements_by_class_name("gsc_a_at")

    print("[DEBUG] ", len(titles))

    for title in titles:
        temp_dict[professor][title.text] = {}
        title.click()

        print("[INFO] Entering article ({0})".format(title.text))

        sleep(1)
        
        fields = browser.find_elements_by_class_name("gsc_vcd_field")
        values = browser.find_elements_by_class_name("gsc_vcd_value")

        print("[DEBUG] There are {0} fields to parse".format(len(fields)))

        for k, v in zip(fields, values):
            if k.text == "Authors":
                temp_dict[professor][title.text][k.text] = v.text.split(', ')
            elif k.text == "Total citations":
                temp_dict[professor][title.text][k.text] = int(v.text.split('\n')[0].split(' ')[2])
            else:
                temp_dict[professor][title.text][k.text] = v.text
            print("[INFO] parsed : {0} : {1}".format(k.text, v.text))

        print("-----------------------")
        browser.back()
        sleep(1)

    
    with open(filename, "w+") as f:
        f.write(json.dumps(temp_dict))
    sleep(1)

    browser.quit()
