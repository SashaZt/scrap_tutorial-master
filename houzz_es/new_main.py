from bs4 import BeautifulSoup
import csv
import os
import random
import time
import json
import requests
import re
from urllib.parse import urlparse

keywords = ["Commercial", "Residential", "LEED", "Greengaurd", "Phthalates", "Polyvinyl", "PVC"]
cookies = {
    'v': '1689099389_4cfaa9ff-5156-4f08-8fd6-04e463fff45e_f25e391aaf89f6c7e0b1f3b57e1929ed',
    'vct': 'en-US-CR99nK1k8B99nK1kSBx9nK1k4R19nK1k4h19nK1k',
    '_csrf': '6p7nT5pK2EZfk1gsiBzo0WPD',
    'prf': 'prodirDistFil%7C%7D',
    'documentWidth': '1920',
    '_gcl_au': '1.1.2066993161.1689099416',
    '_gid': 'GA1.2.1283829895.1689099416',
    '_pin_unauth': 'dWlkPU1HWm1aakEzWXpZdFlXRmhZaTAwTURsbUxUZzJaV1l0TnpGbU5qbGlOV05oTmpFNA',
    'jdv': 't7WOzUb2vHLZtWVVHSk8XJAeN7ua9zR8UkXoYtRfWRbjhUARyr6uKbLj7Jj5SQXvBLcrdsb3Rw6tTUojfDm1itWv448S',
    '_gali': 'hz-primary-header-container',
    'hzd': '437f5b75-e570-4541-ad1a-32372342f83d%3A%3A%3A%3A%3AGetStarted',
    '_gat': '1',
    '_uetsid': '1feacaa0201711eeaaa28323f46224c5',
    '_uetvid': '1feb0070201711eea7d657adb6a604a8',
    '_ga_PB0RC2CT7B': 'GS1.1.1689139345.3.1.1689139347.58.0.0',
    '_ga': 'GA1.1.1637593233.1689099416',
}

headers = {
    'authority': 'www.houzz.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru',
    'cache-control': 'no-cache',
    # 'cookie': 'v=1689099389_4cfaa9ff-5156-4f08-8fd6-04e463fff45e_f25e391aaf89f6c7e0b1f3b57e1929ed; vct=en-US-CR99nK1k8B99nK1kSBx9nK1k4R19nK1k4h19nK1k; _csrf=6p7nT5pK2EZfk1gsiBzo0WPD; prf=prodirDistFil%7C%7D; documentWidth=1920; _gcl_au=1.1.2066993161.1689099416; _gid=GA1.2.1283829895.1689099416; _pin_unauth=dWlkPU1HWm1aakEzWXpZdFlXRmhZaTAwTURsbUxUZzJaV1l0TnpGbU5qbGlOV05oTmpFNA; jdv=t7WOzUb2vHLZtWVVHSk8XJAeN7ua9zR8UkXoYtRfWRbjhUARyr6uKbLj7Jj5SQXvBLcrdsb3Rw6tTUojfDm1itWv448S; _gali=hz-primary-header-container; hzd=437f5b75-e570-4541-ad1a-32372342f83d%3A%3A%3A%3A%3AGetStarted; _gat=1; _uetsid=1feacaa0201711eeaaa28323f46224c5; _uetvid=1feb0070201711eea7d657adb6a604a8; _ga_PB0RC2CT7B=GS1.1.1689139345.3.1.1689139347.58.0.0; _ga=GA1.1.1637593233.1689099416',
    'dnt': '1',
    'pragma': 'no-cache',
    'referer': 'https://www.houzz.com/professionals/hznb/probr2-bo~t_11785~b_1v3-1v4',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}
file_path = "proxies.txt"


def load_proxies(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if '@' in line and ':' in line]


def get_random_proxy(proxies):
    return random.choice(proxies)


def get_url_company():
    with open('houzz_input.txt', 'r') as file:
        for line in file:
            url = line.strip()

            proxies = load_proxies(file_path)
            proxy = get_random_proxy(proxies)
            login_password, ip_port = proxy.split('@')
            login, password = login_password.split(':')
            ip, port = ip_port.split(':')

            proxy_dict = {
                "http": f"http://{login}:{password}@{ip}:{port}",
                "https": f"http://{login}:{password}@{ip}:{port}"
            }

            response = requests.get(url, cookies=cookies, headers=headers, proxies=proxy_dict)
            src = response.text
            soup = BeautifulSoup(src, 'lxml')
            script_json = soup.find('script', type="application/json")
            data_json = json.loads(script_json.string)
            try:
                pagination_total = int(
                    data_json['data']['stores']['data']['ViewProfessionalsStore']['data']['paginationSummary'][
                        'total'].replace(',', ''))
            except:
                continue
            amount_page = pagination_total // 15
            coun = 0
            if os.path.exists('url_products.csv'):
                os.remove('url_products.csv')
            with open('url_products.csv', 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                count = 0
                for i in range(1, amount_page + 2):
                    proxies = load_proxies(file_path)

                    proxy = get_random_proxy(proxies)
                    login_password, ip_port = proxy.split('@')
                    login, password = login_password.split(':')
                    ip, port = ip_port.split(':')

                    proxy_dict = {
                        "http": f"http://{login}:{password}@{ip}:{port}",
                        "https": f"http://{login}:{password}@{ip}:{port}"
                    }

                    pause_time = random.randint(1, 5)
                    count += 1
                    datas_urls = []
                    if i == 1:
                        url_first = url
                        try:
                            response = requests.get(url_first, cookies=cookies, headers=headers, proxies=proxy_dict)
                            src_1 = response.text
                            soup = BeautifulSoup(src_1, 'lxml')
                            try:
                                products_urls = soup.find('ul', attrs={'class': 'hz-pro-search-results mb0'}).find_all(
                                    'a')
                            except:
                                continue
                            for u in products_urls:
                                url_sc = u.get("href")
                                writer.writerow([url_sc])
                        except:
                            continue

                    elif i > 1:
                        coun += 15
                        urls = f'{url}?fi={coun}'
                        try:
                            response = requests.get(urls, cookies=cookies, headers=headers, proxies=proxy_dict)
                            src_2 = response.text
                            soup = BeautifulSoup(src_2, 'lxml')
                            try:
                                products_urls = soup.find('ul', attrs={'class': 'hz-pro-search-results mb0'}).find_all(
                                    'a')
                            except:
                                continue
                            for u in products_urls:
                                url_pr = u.get("href")
                                writer.writerow([url_pr])
                        except:
                            continue
                    time.sleep(pause_time)


def get_company():
    with open(f'data_test.csv', "w", errors='ignore', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=",", lineterminator="\r", quoting=csv.QUOTE_ALL)
        headers_csv = ('url', 'name_company', 'www_company', 'telephone_company', 'address', 'street_address',
                       'addressLocality', 'addressRegion', 'postalCode', 'addressCountry', 'emails',
                       "Commercial", "Residential", "LEED", "Greengaurd", "Phthalates", "Polyvinyl", "PVC")
        writer.writerow(headers_csv)
        with open('url_products.csv', newline='',
                  encoding='utf-8') as files:
            csv_reader = list(csv.reader(files, delimiter=' ', quotechar='|'))
            for url in csv_reader:
                proxies = load_proxies(file_path)
                proxy = get_random_proxy(proxies)
                login_password, ip_port = proxy.split('@')
                login, password = login_password.split(':')
                ip, port = ip_port.split(':')

                proxy_dict = {
                    "http": f"http://{login}:{password}@{ip}:{port}",
                    "https": f"http://{login}:{password}@{ip}:{port}"
                }
                emails = set()
                response = requests.get(url[0], cookies=cookies, headers=headers, proxies=proxy_dict)
                src = response.text
                soup = BeautifulSoup(src, 'lxml')
                script_tag = soup.find('script', {'type': 'application/json'})
                try:
                    json_data = json.loads(script_tag.string)
                except:

                    continue
                try:
                    sfru = json_data['sfru']

                except:
                    sfru = None
                try:
                    name_company = json_data['data']['stores']['data']['MetaDataStore']['data']['htmlMetaTags'][
                        2]['attributes']['content']
                except:
                    name_company = None
                try:
                    telephone_company = \
                        json_data['data']['stores']['data']['ProProfileStore']['data']['user']['professional'][
                            'formattedPhone']
                except:
                    telephone_company = None
                contact_email = ""
                try:
                    www_company = \
                        json_data['data']['stores']['data']['ProProfileStore']['data']['user']['professional'][
                            'rawDomain']
                except:
                    www_company = None

                try:
                    main_site = requests.get(www_company, proxies=proxy_dict)
                except requests.exceptions.RequestException:
                    main_site = None
                Commercial = ''
                Residential = ''
                LEED = ''
                Greengaurd = ''
                Phthalates = ''
                Polyvinyl = ''
                PVC = ''
                if main_site is not None:
                    main_soup = BeautifulSoup(main_site.text, 'html.parser')
                    emails |= set(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', main_site.text))
                    main_text = main_soup.get_text().lower()

                    Commercial = 'yes' if 'commercial' in main_text else 'no'
                    Residential = 'yes' if 'residential' in main_text else 'no'
                    LEED = 'yes' if 'leed' in main_text else 'no'
                    Greengaurd = 'yes' if 'greengaurd' in main_text else 'no'
                    Phthalates = 'yes' if 'phthalates' in main_text else 'no'
                    Polyvinyl = 'yes' if 'polyvinyl' in main_text else 'no'
                    PVC = 'yes' if 'pvc' in main_text else 'no'
                    main_links = set([a['href'] for a in main_soup.find_all('a', href=True)])
                    for link in main_links:
                        if not link.startswith('http'):
                            if www_company.endswith('/') and link.startswith('/'):
                                link = www_company + link[1:]
                            else:
                                link = www_company + link
                        try:
                            site = requests.get(link, proxies=proxy_dict)
                        except requests.exceptions.RequestException:
                            continue
                        soup = BeautifulSoup(site.text, 'html.parser')
                        domain = urlparse(www_company).netloc
                        matches = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', site.text)
                        emails |= set([email for email in matches if
                                       not (email.endswith('.png') or email.endswith('.jpg')) and email.endswith(
                                           domain)])

                        text = soup.get_text().lower()
                        Commercial = 'yes' if 'commercial' in text else Commercial
                        Residential = 'yes' if 'residential' in text else Residential
                        LEED = 'yes' if 'leed' in text else LEED
                        Greengaurd = 'yes' if 'greengaurd' in text else Greengaurd
                        Phthalates = 'yes' if 'phthalates' in text else Phthalates
                        Polyvinyl = 'yes' if 'polyvinyl' in text else Polyvinyl
                        PVC = 'yes' if 'pvc' in text else PVC

                try:
                    address_company = \
                        json_data['data']['stores']['data']['ProProfileStore']['data']['user']['professional'][
                            'formattedAddress']
                except:
                    continue
                address = ''

                try:
                    soup_add = BeautifulSoup(address_company, 'html.parser')
                    address_elements = soup_add.find_all('span', itemprop='streetAddress')
                    for element in address_elements:
                        address += element.text.strip() + ' '
                except:
                    continue

                try:
                    postal_code_element = soup_add.find('span', itemprop='postalCode')
                    if postal_code_element:
                        address += postal_code_element.text.strip() + ' '
                except:
                    continue

                try:
                    locality_element = soup_add.find('span', itemprop='addressLocality')
                    if locality_element:
                        address += locality_element.text.strip() + ' '
                except:
                    continue
                street_address = ""
                addressLocality = ""
                addressRegion = ""
                postalCode = ""
                addressCountry = ""
                try:
                    street_add = json_data['data']['stores']['data']['PageStore']['data']['pageDescriptionFooter']
                    soup_s = BeautifulSoup(street_add, 'html.parser')
                    script_tag = soup_s.find('runnable', type='application/ld+json')
                    if script_tag:
                        json_data_script = script_tag.string.strip()
                        data = json.loads(json_data_script)
                        for item_add in data:
                            if 'address' in item_add:
                                try:
                                    street_address = item_add['address'].get('streetAddress')
                                except:
                                    street_address = ""
                                try:
                                    addressLocality = item_add['address'].get('addressLocality')
                                except:
                                    addressLocality = ""
                                try:
                                    addressRegion = item_add['address'].get('addressRegion')
                                except:
                                    addressRegion = ""
                                try:
                                    postalCode = item_add['address'].get('postalCode')
                                except:
                                    postalCode = ""
                                try:
                                    addressCountry = item_add['address'].get('addressCountry')
                                except:
                                    addressCountry = ""
                except:
                    continue
                if not postalCode:
                    postalCode = \
                        json_data['data']['stores']['data']['ProProfileStore']['data']['user']['professional']['zip']
                if not addressLocality:
                    addressLocality = \
                        json_data['data']['stores']['data']['ProProfileStore']['data']['user']['professional']['city']
                if not addressCountry:
                    addressCountry = \
                        json_data['data']['stores']['data']['FooterStore']['data']['footerInfo']['currentCcTld'][
                            'countryNativeName']
                datas = [
                    [sfru, name_company, www_company, telephone_company, address, street_address,
                     addressLocality, addressRegion, postalCode, addressCountry, emails, Commercial, Residential,
                     LEED, Greengaurd, Phthalates, Polyvinyl, PVC]
                ]

                writer.writerows(datas)


if __name__ == '__main__':
    get_url_company()
    get_company()
