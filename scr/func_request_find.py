import sys

import requests

from config import config_env

from lxml import html
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def send_request_get(url):
    return requests.get(url)


def selenium_send_request(url):
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.headless = False
    browser = webdriver.Chrome(executable_path=config_env.PATH_CHROME_DRIVER, options=options)
    browser.implicitly_wait(config_env.IMPLICITLY_WAIT)
    browser.get(url)
    return browser


def html_find_xpath(html, xpath):
    result = html.xpath(xpath)
    return result


def browser_find_xpath(browser, xpath):
    result = browser.find_element(By.XPATH, xpath)
    return result


def browser_finds_xpath(browser, xpath):
    results = browser.find_elements(By.XPATH, xpath)
    return results 


