from bs4 import BeautifulSoup
import random
import glob
import re
import requests
import json
import cloudscraper
import os
from playwright.sync_api import sync_playwright
from cf_clearance import sync_cf_retry, sync_stealth
import time
import shutil
import tempfile
# import undetected_chromedriver as webdriver


from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from concurrent.futures import ThreadPoolExecutor
import csv


def get_chromedriver():
    options = webdriver.ChromeOptions()

    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--disable-gpu")
    # options.add_experimental_option("excludeSwitches", ['enable-automation'])
    # chrome_options.add_argument('--disable-infobars')
    options.add_argument("--start-maximized")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    # options.add_argument('--disable-extensions') # Отключает использование расширений
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-setuid-sandbox')
    options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')
    service = ChromeService(executable_path='C:\\scrap_tutorial-master\\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        'source': '''
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
      '''
    })
    return driver

def get_selenium():
    url = 'https://dok.ua/ua/catalog/maslo-motornoe'
    name_files_ua = url.split('/')[-1].replace('-', '_')
    name_files_rus = url.split('/')[-1].replace('-', '_')
    driver = get_chromedriver()
    driver.maximize_window()
    driver.get(url)
    time.sleep(5)

    file_name = f"{name_files_ua}.html"
    with open(file_name, "w", encoding='utf-8') as fl:
        fl.write(driver.page_source)
    driver.find_element(By.XPATH, '//div[@class="header__top-block"]//a[@data-language="ru"]').click()
    time.sleep(5)
    file_name = f"{name_files_rus}.html"
    with open(file_name, "w", encoding='utf-8') as fl:
        fl.write(driver.page_source)
def parsing():
    file = f"amazon_ru.html"
    with open(file, encoding="utf-8") as file:
         src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    row_id = 1
    hedler = []
    while True:
        element = soup.find('span', {'data-row-id': str(row_id)})
        if element:
            hedler.append(element.text.strip())
            row_id += 1
        else:
            break
    print(hedler)



if __name__ == '__main__':
    get_selenium()
    # parsing()
