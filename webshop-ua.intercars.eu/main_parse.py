import glob
import re
from random import randint
import time
import psutil
import requests
import undetected_chromedriver
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
# Для работы webdriver____________________________________________________
# Для работы с драйвером селениум по Хром необходимо эти две строчки
from selenium.webdriver.support.wait import WebDriverWait

import csv

# Нажатие клавиш

useragent = UserAgent()

# Данные для прокси
PROXY_HOST = 'IP'
PROXY_PORT = 'PORT'  # Без кавычек
PROXY_USER = 'LOGIN'
PROXY_PASS = 'PASS'

# Настройка для requests чтобы использовать прокси
proxies = {'http': f'http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}/'}

manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"76.0.0"
}
"""

background_js = """
let config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };
chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}
chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)


# def get_chromedriver(use_proxy=True, user_agent=None):
#     chrome_options = webdriver.ChromeOptions()
#
#     if use_proxy:
#         plugin_file = 'proxy_auth_plugin.zip'
#
#         with zipfile.ZipFile(plugin_file, 'w') as zp:
#             zp.writestr('manifest.json', manifest_json)
#             zp.writestr('background.js', background_js)
#
#         chrome_options.add_extension(plugin_file)
#
#     if user_agent:
#         chrome_options.add_argument(f'--user-agent={user_agent}')
#
#     s = Service(
#         executable_path="C:\\scrap_tutorial-master\\chromedriver.exe"
#     )
#     driver = webdriver.Chrome(
#         service=s,
#         options=chrome_options
#     )
#
#     return driver
def get_undetected_chromedriver(use_proxy=False, user_agent=None):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    driver = undetected_chromedriver.Chrome()
    # s = Service(
    #     executable_path="C:\\scrap_tutorial-master\\chromedriver.exe"
    # )
    # driver = webdriver.Chrome(
    #     service=s,
    #     options=chrome_options
    # )

    return driver


def save_link_all_product(url):
    with open(f'C:\\scrap_tutorial-master\\webshop-ua.intercars.eu\\csv\\output.csv', newline='',
              encoding='utf-8') as files:
        csv_reader = list(csv.reader(files, delimiter=' ', quotechar='|'))
        count_url = 0
        bad_product = []
        counter = 0
        for row in csv_reader[1:2]:
            counter += 1
            name_product = (','.join(row))
            name_product_find = name_product.replace(",", " ")
            name_file = name_product.replace(",", "_")
            driver = get_undetected_chromedriver()
            driver.get(url=url)
            driver.maximize_window()
            try:
                find_product_wait = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//input[@class="ui-autocomplete-input"]')))
                find_product = driver.find_element(By.XPATH, '//input[@class="ui-autocomplete-input"]')
                find_product.send_keys(name_product_find)
                find_product.send_keys(Keys.RETURN)
                time.sleep(1)
                try:
                    dont_find_wait = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Немає результатів")]')))
                    driver.close()
                    driver.quit()
                except:
                    button_img_wain = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//div[@class="art-images margincenter"]')))
                    button_img = driver.find_element(By.XPATH, '//div[@class="art-images margincenter"]').click()
                    wait_img_full = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//div[@class="swal2-container"]')))
                    with open(f"c:\\intercars_html\\{name_file}.html", "w",
                              encoding='utf-8') as file:
                        file.write(driver.page_source)
                    driver.close()
                    driver.quit()
            except:
                bad_product.append(name_product_find)
                with open(f'C:\\scrap_tutorial-master\\webshop-ua.intercars.eu\\csv\\bad_product.csv', 'a', newline='',
                          encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter='\n', quotechar='|')
                    writer.writerow(bad_product)
                driver.close()
                driver.quit()
            print(counter)



def parsing_product():
    targetPattern = r"c:\intercars_html\*.html"
    files_html = glob.glob(targetPattern)
    # data = []
    for item in files_html[:5]:
        with open(f"{item}", encoding="utf-8") as file:
            src = file.read()
        driver = get_undetected_chromedriver()
        driver.get(item)
        driver.maximize_window()
        soup = BeautifulSoup(src, 'lxml')
        sku = driver.find_element(By.XPATH, '//span[@id="index_30"]').text
        name_product = soup.find('p', attrs={'id': 'description_30'}).text.strip()
        try:
            if driver.find_element(By.XPATH, '//div[contains(text(), "Штрих-код")]'):
                bray = driver.find_element(By.XPATH, '//div[contains(text(), "Штрих-код")]')
                br = bray.find_element(By.XPATH, './..')
            else:
                continue
        except:
            continue
        with open(f"C:\\scrap_tutorial-master\\webshop-ua.intercars.eu\\data.csv", "a", errors='ignore') as file:
            writer = csv.writer(file, delimiter=";", lineterminator="\r")
            writer.writerow(
                (
                    sku, name_product, br.text.replace("\n", "").replace("Штрих-код:", "")

                )
            )




        #
        #
        # name_product = soup.find('span', attrs={'class': 'active_filters_span'}).text.strip()
        # try:
        #     script_div = soup.find('a', attrs={'data-gc-onclick': 'dyn-gallery'})['data-dyngalposstring']
        # except:
        #     script_div = 'Пусто'
        # pattern = re.compile(r"'src': '(.+?)',")
        # result = pattern.findall(script_div)
        # counter = 0
        # for img in result:
        #     counter += 1
        #     img_data = requests.get(img)
        #     with open(f"c:\\intercars_img\\{name_product}_0{counter}.jpg", 'wb') as file_img:
        #         file_img.write(img_data.content)
        #     if counter == 4:
        #         break


if __name__ == '__main__':
    # # Собираем все ссылки на категории товаров
    # url = "https://webshop-ua.intercars.eu/zapchasti/"
    # save_link_all_product(url)
    # Парсим все товары из файлов с
    parsing_product()
