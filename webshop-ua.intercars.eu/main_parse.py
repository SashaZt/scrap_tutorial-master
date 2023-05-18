import glob
import traceback
import re
import time
import os
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


def get_undetected_chromedriver(use_proxy=False, user_agent=None):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument('--headless')
    """Проба"""
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-setuid-sandbox")

    driver = undetected_chromedriver.Chrome()
    return driver


def save_link_all_product(url):
    with open(f'C:\\scrap_tutorial-master\\webshop-ua.intercars.eu\\csv\\output.csv', newline='',
              encoding='utf-8') as files:
        csv_reader = list(csv.reader(files, delimiter=' ', quotechar='|'))
        count_url = 0
        bad_product = []
        counter = 274870
        for row in csv_reader[274870:]:
            counter += 1
            print(counter)
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
                    driver.find_element(By.XPATH, '//div[contains(text(), "Немає результатів")]')
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
                    time.sleep(5)
                    driver.close()
                    driver.quit()
            except Exception as e:
                bad_product.append(name_product_find)
                with open(f'C:\\scrap_tutorial-master\\webshop-ua.intercars.eu\\csv\\bad_product.csv', 'a', newline='',
                          encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter='\n', quotechar='|')
                    writer.writerow(bad_product)
                traceback.print_exc()
                driver.close()
                driver.quit()


def parsing_product():
    targetPattern = r"c:\intercars_html\*.html"
    files_html = glob.glob(targetPattern)
    # data = []
    # with open("output.csv", "w", newline="", encoding='utf-8') as csvfile:
    #     writer = csv.writer(csvfile)
    for item in files_html:
        # print(item)
        filename_csv = os.path.basename(item)  # Получаем только имя файла из пути
        filename_csv = os.path.splitext(filename_csv)[0].replace("_", " ")  # Удаляем расширение файла
        # writer.writerow([filename_csv])
        with open(f"{item}", encoding="utf-8") as file:
            src = file.read()
        soup = BeautifulSoup(src, 'lxml')

        try:
            name_product = soup.find('span', attrs={'class': 'active_filters_span'}).text.strip()
        except:
            name_product = filename_csv
        try:
            script_div = soup.find('a', attrs={'data-gc-onclick': 'dyn-gallery'})['data-dyngalposstring']
        except:
            script_div = 'Пусто'
        pattern = re.compile(r"'src': '(.+?)',")
        result = pattern.findall(script_div)
        counter = 1
        filenames = []
        for img in result:

            """Выкачка фото"""
            img_dir = "c:\\intercars_img"
            if len(result) < 4:
                while counter <= len(result):
                    filename = f"{name_product}_0{counter}.jpg"
                    file_path = os.path.join(img_dir, filename)

                    if os.path.exists(file_path):
                        # Файл уже существует, пропускаем его
                        # print(f"Файл {filename} уже существует, пропускаем его")
                        counter += 1
                        continue

                    img_data = requests.get(img)
                    with open(file_path, 'wb') as file_img:
                        file_img.write(img_data.content)

                    counter += 1
                filenames.append(filename)
            elif len(result) > 4:
                while counter <= 4:
                    filename = f"{name_product}_0{counter}.jpg"
                    file_path = os.path.join(img_dir, filename)

                    if os.path.exists(file_path):
                        # Файл уже существует, пропускаем его
                        # print(f"Файл {filename} уже существует, пропускаем его")
                        counter += 1
                        continue

                    img_data = requests.get(img)
                    with open(file_path, 'wb') as file_img:
                        file_img.write(img_data.content)

                    counter += 1
                filenames.append(filename)
            # print(filenames)
            """Получение данных"""
            try:
                full_name = soup.find('div', class_="col-xs-12 p-l-2 p-r-2 f-12 text-center").text
            except:
                full_name = ""
            details_card_div = soup.find("div", {"id": "details_card"})
            try:
                divs = details_card_div.find_all("div", class_="clearfix flexcard p-l-2 p-r-2")
            except:
                continue
            pattern = re.compile(r"Штрих-ко.*?(\d{13})")
            barcode = ''
            for div in divs:
                match = pattern.search(div.text)
                if match:
                    barcode = match.group(1)
                    barcode = re.sub(r"\D", "", barcode)  # Удаляем все символы, кроме цифр
                    break
            # print(details_card_div)
            manufacture = soup.find('span', attrs = {'id': 'manufacture_30'}).text
            manufacture_code = soup.find('a', class_="article_index_link").text
            manufacture_name = soup.find('span', attrs = {'id': 'name_30'}).text
            with open("data.csv", "a", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow([full_name, manufacture, manufacture_code, manufacture_name, barcode] + filenames)
            # print(f"{full_name} | {manufacture} | {manufacture_code} | {manufacture_name} | {barcode}")
if __name__ == '__main__':
    # # Собираем все ссылки на категории товаров
    # url = "https://webshop-ua.intercars.eu/zapchasti/"
    # save_link_all_product(url)
    # Парсим все товары из файлов с
    parsing_product()
