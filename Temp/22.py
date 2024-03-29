import csv
import json
import math
from datetime import datetime
import os
import re
import pandas as pd
import mysql.connector
from concurrent.futures import ProcessPoolExecutor
import time
import threading
from urllib.parse import urlparse, parse_qs
import glob
import requests
from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import random
from selenium.webdriver.common.by import By


"""Настройка browsermob-proxy"""
server_options = {
    'log_path': 'NUL'
}

server = Server(r"c:\Program Files (x86)\browsermob-proxy\bin\browsermob-proxy", options=server_options)
server.start()
proxy = server.create_proxy()


"""Настройка для Selenium"""
def get_chromedriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(
        f'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument('--auto-open-devtools-for-tabs=devtools://devtools/bundled/inspector.html')

    s = Service(executable_path="C:\\scrap_tutorial-master\\chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=chrome_options)

    return driver


"""Получаем curl с помощью Selenium и browsermob-proxy"""
def selenium_get_curl(url):
    proxy.new_har("copart.com", options={'captureHeaders': True, 'captureContent': True})
    """Ссылка куда переходим"""
    driver = get_chromedriver()
    driver.get(url)
    time.sleep(5)

    driver.execute_script('''
        var elements = document.querySelectorAll('[aria-label="Network panel"]');
        for (var i = 0; i < elements.length; i++) {
            var element = elements[i];
            if (element.offsetWidth > 0 && element.offsetHeight > 0) {
                element.click();
                break;
            }
        }
    ''')
    time.sleep(5)
    # получить все запросы из Network panel
    requests = driver.execute_script('''
        var performanceEntries = performance.getEntriesByType("resource");
        var fetchRequests = [];
        for (var i = 0; i < performanceEntries.length; i++) {
            var entry = performanceEntries[i];
            fetchRequests.push(entry);
        }
        return fetchRequests;
    ''')

    curl_command = "curl "
    entries = proxy.har['log']['entries']
    for entry in entries:
        # print(entry)
        """Указываем тут url который нужно отслеживать"""
        if entry['request']['url'].startswith('https://www.copart.com/public/lots/vehicle-finder-search-results'):
            # Method (GET, POST, etc.)
            curl_command += "-X {} ".format(entry['request']['method'])

            # URL
            curl_command += "'{}' \\\n".format(entry['request']['url'])

            # Headers
            for header in entry['request']['headers']:
                header_name = header['name']
                header_value = header['value']
                curl_command += "  -H '{}: {}' \\\n".format(header_name, header_value)

            if entry['request']['method'] == 'POST' and 'postData' in entry['request']:
                if 'text' in entry['request']['postData']:
                    curl_command += "  --data '{}'".format(entry['request']['postData']['text'])

            break

    # Extracting cookies
    cookies_match = re.search(r"Cookie:\s(.*?)'", curl_command)
    if cookies_match:
        cookies_str = cookies_match.group(1)
        cookies_list = cookies_str.split('; ')
        cookies = {cookie.split('=')[0]: cookie.split('=')[1] for cookie in cookies_list}

    # Extracting headers
    headers_match = re.findall(r"-H '(.*?)'", curl_command)
    headers = {header.split(': ')[0]: header.split(': ')[1] for header in headers_match}
    return curl_command

"""curl разбираем на cookies и headers"""
def get_cookie_header(curl_command):
    cookies = {}
    headers = {}
    params = {}
    method = "GET"  # по умолчанию

    url_match = re.search(r"'(.*?)'", curl_command)
    if url_match:
        url = url_match.group(1)
        parsed_url = urlparse(url)
        params = parse_qs(parsed_url.query)

    method_match = re.search(r"-X (\w+)", curl_command)
    if method_match:
        method = method_match.group(1)

    cookies_match = re.search(r"Cookie:\s(.*?)'", curl_command)
    if cookies_match:
        cookies_str = cookies_match.group(1)
        cookies_list = cookies_str.split("; ")
        cookies = {cookie.split("=")[0]: cookie.split("=")[1] for cookie in cookies_list}

    headers_match = re.findall(r"-H '(.*?)'", curl_command)
    headers = {header.split(": ")[0]: header.split(": ")[1] for header in headers_match}
    url_match = re.search(r"'(.*?)'", curl_command)
    url = None
    if url_match:
        url = url_match.group(1)

    return url, params, cookies, headers
# def save_to_file(url, params, cookies, headers):
#     with open("headers_cookies.py", "w") as f:
#         f.write("url = '{}'\n\n".format(url))
#
#         f.write("params = {\n")
#         for key, value in params.items():
#             f.write("    '{}': {},\n".format(key, value))
#         f.write("}\n\n")
#
#         f.write("cookies = {\n")
#         for key, value in cookies.items():
#             f.write("    '{}': '{}',\n".format(key, value))
#         f.write("}\n\n")
#
#         f.write("headers = {\n")
#         for key, value in headers.items():
#             f.write("    '{}': '{}',\n".format(key, value))
#         f.write("}\n")

"""Получаем общее количество объявлений"""
def get_totalElements():
    """Используем каждый фильтр со своими данными"""
    # json_data = {
    #     'query': [
    #         '*',
    #     ],
    #     'filter': {
    #         'NLTS': [
    #             'expected_sale_assigned_ts_utc:[NOW/DAY-1DAY TO NOW/DAY]',
    #         ],
    #     },
    #     'sort': None,
    #     'page': 0,
    #     'size': 100,
    #     'start': 0,
    #     'watchListOnly': False,
    #     'freeFormSearch': False,
    #     'hideImages': False,
    #     'defaultSort': False,
    #     'specificRowProvided': False,
    #     'displayName': '',
    #     'searchName': '',
    #     'backUrl': '',
    #     'includeTagByField': {},
    #     'rawParams': {},
    # }
    json_data = {
        'query': [
            '*',
        ],
        'filter': {},
        'sort': None,
        'page': 0,
        'size': 100,
        'start': 0,
        'watchListOnly': False,
        'freeFormSearch': False,
        'hideImages': False,
        'defaultSort': False,
        'specificRowProvided': False,
        'displayName': '',
        'searchName': '',
        'backUrl': '',
        'includeTagByField': {},
        'rawParams': {},
    }
    response = requests.post('https://www.copart.com/public/lots/search-results', cookies=cookies,
                             headers=headers, json=json_data)

    data_json = response.json()
    totalElements = data_json['data']['results']['totalElements']
    print(f'Всего {totalElements}')
    return totalElements


"""Получаем все объявления"""
def get_request_thread(start_page, end_page):
    for page in range(start_page, end_page):
        start = page * 100
        filename = f"c:\\DATA\\copart\\list\\data_{page}.json"
        if not os.path.exists(filename):
            json_data = {
                'query': [
                    '*',
                ],
                'filter': {},
                'sort': None,
                'page': page,
                'size': 100,
                'start': start,
                'watchListOnly': False,
                'freeFormSearch': False,
                'hideImages': False,
                'defaultSort': False,
                'specificRowProvided': False,
                'displayName': '',
                'searchName': '',
                'backUrl': '',
                'includeTagByField': {},
                'rawParams': {},
            }

            try:
                response = requests.post('https://www.copart.com/public/lots/search-results', cookies=cookies, headers=headers, json=json_data)
                data = response.json()
                time.sleep(1)
                with open(filename, 'w') as f:
                    json.dump(data, f)
            except:
                pass

def multi_threaded_get_request(totalElements, thread_count):
    ad = totalElements
    page_ad = ad // 100

    pages_per_thread = (page_ad + 1) // thread_count
    threads = []

    for i in range(thread_count):
        start_page = i * pages_per_thread
        end_page = (i + 1) * pages_per_thread if i != thread_count - 1 else page_ad + 1
        t = threading.Thread(target=get_request_thread, args=(start_page, end_page))
        threads.append(t)
        t.start()

    # Дождитесь завершения выполнения всех потоков
    for t in threads:
        t.join()

    now = datetime.now()
    print(f'Все {page_ad} страницы скачаны в {now}')
def get_id_ad_and_url():
    folders_html = r"c:\DATA\copart\list\*.json"
    files_html = glob.glob(folders_html)
    file_csv = f"url.csv"
    with open(file_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for i in files_html:
            with open(i, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            content = json_data['data']['results']['content']
            for c in content:
                url_ad = f'https://www.copart.com/public/data/lotdetails/solr/lotImages/{c["ln"]}/USA'
                writer.writerow([url_ad])
    now = datetime.now()
    print(f'Получили список всех url в {now}')
"""Следующие 3 функции для работы с Selenium"""
def split_urls(urls, n):
    """Делит список URL-адресов на n равных частей."""
    avg = len(urls) // n
    urls_split = [urls[i:i + avg] for i in range(0, len(urls), avg)]
    return urls_split



def worker(sub_urls, start_counter):
    driver = get_chromedriver()
    for counter, url in enumerate(sub_urls, start=start_counter):
        try:
            filename = f"c:\\DATA\\copart\\product\\data_{counter}.json"
            if not os.path.exists(filename):
                driver.get(url[0])
                time.sleep(1)
                json_content = driver.page_source
                json_content = json_content.replace(
                    '<html><head><meta name="color-scheme" content="light dark"><meta charset="utf-8"></head><body style="margin: 0"><div></div><pre>',
                    '')
                json_content = json_content.replace('</pre></body></html>', '')
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(json_content)

        except Exception as e:
            print(f"Error processing URL {url[0]}: {e}")
    driver.quit()


def get_product_s():
    with open("url.csv", newline='', encoding='utf-8') as files:
        urls = list(csv.reader(files, delimiter=' ', quotechar='|'))
        max_workers = 10
        splitted_urls = split_urls(urls, max_workers)
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            for idx, sub_urls in enumerate(splitted_urls):
                executor.submit(worker, sub_urls, idx * len(sub_urls))
"""Следующие 3 функции для работы с Selenium"""
def parsin():
    print('Передаем данные в Mysql')
    cnx = mysql.connector.connect(
        # host="localhost",  # ваш хост, например "localhost"
        host="vpromo2.mysql.tools",  # ваш хост, например "localhost"
        user="vpromo2_usa",  # ваше имя пользователя
        password="^~Hzd78vG4",  # ваш пароль
        database="vpromo2_usa"  # имя вашей базы данных
    )

    # Создаем объект курсора, чтобы выполнять SQL-запросы
    cursor = cnx.cursor()
    folders_html = r"c:\DATA\copart\product\*.json"
    files_html = glob.glob(folders_html)
    for i in files_html:
        with open(i, 'r') as f:
            # Загрузить JSON из файла
            data_json = json.load(f)

        try:
            ln = data_json['data']['lotDetails']['ln']
        except:
            continue
        url_lot = f"https://www.copart.com/lot/{ln}"
        try:
            url_img_full = data_json['data']['imagesList']['FULL_IMAGE']
            urls_full = str(",".join([u['url'] for u in url_img_full]))
        except:
            urls_full = None
        try:
            url_img_high = data_json['data']['imagesList']['HIGH_RESOLUTION_IMAGE']
            urls_high = str(",".join([u_h['url'] for u_h in url_img_high]))
        except:
            urls_high = None

        name_lot = data_json['data']['lotDetails']['ld']
        lotNumberStr = data_json['data']['lotDetails']['lotNumberStr']
        td_ts = f"{data_json['data']['lotDetails']['ts']}-{data_json['data']['lotDetails']['td']}"
        hk = data_json['data']['lotDetails']['hk']
        la = data_json['data']['lotDetails']['la']
        dd = data_json['data']['lotDetails']['dd']
        try:
            cy = data_json['data']['lotDetails']['cy']
        except:
            cy = None
        try:
            bstl = data_json['data']['lotDetails']['bstl']
        except:
            bstl = None
        try:
            tmtp = data_json['data']['lotDetails']['tmtp']
        except:
            tmtp = 'YES'
        try:
            drv = data_json['data']['lotDetails']['drv']
        except:
            drv = None
        try:
            egn = data_json['data']['lotDetails']['egn']
        except:
            egn = None
        try:
            vehTypDesc = data_json['data']['lotDetails']['vehTypDesc']
        except:
            vehTypDesc = None
        try:
            ft = data_json['data']['lotDetails']['ft']
        except:
            ft = None
        try:
            clr = data_json['data']['lotDetails']['clr']
        except:
            clr = None
        try:
            ess = data_json['data']['lotDetails']['ess']
        except:
            ess = None

        currentBid = data_json['data']['lotDetails']['dynamicLotDetails']['currentBid']
        odometer_lot = data_json['data']['lotDetails']['orr']

        try:
            highlights_lot = data_json['data']['lotDetails']['lcd']
        except:
            highlights_lot = None
        try:
            sale_location = data_json['data']['lotDetails']['yn']
        except:
            sale_location = None
        datas = [url_lot, urls_full, urls_high, name_lot, lotNumberStr, td_ts, odometer_lot, hk, tmtp, la, dd, cy, bstl,
                 drv, egn, vehTypDesc, ft, clr, highlights_lot, ess, currentBid, sale_location]
        insert_query = """
       INSERT INTO copart
        (url_lot, url_img_full, url_img_high, name_lot, lot_number, title_code, odometer, `keys`, transmission, price, primary_damage, cylinders,body_style,
               drive,engine_type,vehicle_type,fuel,color,highlights,sale_status,current_bid,sale_location) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, datas)
    cnx.commit()
    cnx.close()
    now = datetime.now()
    print(f'Загрузил данны в БД {now}')
if __name__ == '__main__':
    print("Вставьте ссылку")
    # """Обновление за сутки"""
    # url = 'https://www.copart.com/vehicleFinderSearch?displayStr=%5B0%20TO%209999999%5D,%5B2011%20TO%202024%5D&from=%2FvehicleFinder&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22NLTS%22:%5B%22expected_sale_assigned_ts_utc:%5BNOW%2FDAY-1DAY%20TO%20NOW%2FDAY%5D%22%5D%7D,%22searchName%22:%22%22,%22watchListOnly%22:false,%22freeFormSearch%22:false%7D'
    """Все объявления"""
    url = 'https://www.copart.com/vehicleFinderSearch?displayStr=%5B0%20TO%209999999%5D,%5B2011%20TO%202024%5D&from=%2FvehicleFinder&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%7D,%22searchName%22:%22%22,%22watchListOnly%22:false,%22freeFormSearch%22:false%7D'
    curl_result = selenium_get_curl(url)  # сохраняем результат функции в переменную
    get_cookie_header(curl_result)
    server.stop()  # остановка сервера должна быть здесь
    url, params, cookies, headers = get_cookie_header(curl_result)
    # save_to_file(url, params, cookies, headers)
    totalElements = get_totalElements()
    multi_threaded_get_request(totalElements, 10)
    # get_id_ad_and_url()
    # get_product_s()
    # parsin()
