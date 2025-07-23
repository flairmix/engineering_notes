from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import re
from bs4 import BeautifulSoup


def start_browser(headless_on:bool):
    options = webdriver.ChromeOptions()
    if headless_on:
        options.add_argument('headless')
    options.page_load_strategy = 'normal'
    return webdriver.Chrome('/Applications/Google Chrome', chrome_options=options)
    

def click_button_by_xpath(browser, xpath):
    try:
        time.sleep(0.1)
        elem = browser.find_element(By.XPATH, xpath)
        elem.click()
    except:
        print(f"fail with button {xpath}")


def write_field_by_class_name(browser, class_name:str, input:str):
    try:
        browser.find_element(By.CLASS_NAME, class_name).clear()
        browser.find_element(By.CLASS_NAME, class_name).send_keys(input)
    except:
        print(f"fail input {input} in {class_name} ")


def get_bs4_page(browser, parser='html.parser'):
    return BeautifulSoup(browser.page_source, parser)
    