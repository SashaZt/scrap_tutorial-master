import glob
import csv
import datetime
import json
import time

import requests
import requests
import json
import random
import os

file_path = "proxy.txt"


def load_proxies(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if '@' in line and ':' in line]
    except FileNotFoundError:
        return []


# def get_random_proxy(proxies):
#     return proxies if proxies else None
#     # return random.choice(proxies) if proxies else None


def get_random_proxy(proxies):
    if not hasattr(get_random_proxy, "_proxy_generator"):
        get_random_proxy._proxy_generator = iter(proxies)
    return next(get_random_proxy._proxy_generator)


def get_wallet():
    name_files = 'wallet.csv'
    with open(name_files, newline='', encoding='utf-8') as files:
        reader = csv.reader(files, delimiter=',', quotechar='|')
        for w in reader:
            if len(w) == 2:  # Убедимся, что в строке два элемента
                yield w[0], w[1]  # Используем yield для генерации кошелька и даты


def main():
    for wallet, date in get_wallet():  # Итерируемся по всем кошелькам и датам
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
        }

        start_time = 0
        while True:
            filename = f'{wallet}_{start_time}.json'
            # if os.path.exists(filename):  # Проверка на существование файла
            #     print(f"File {filename} already exists. Skipping.")
            #     continue
            proxy_dict = None

            # proxies = load_proxies(file_path)
            # proxy = get_random_proxy(proxies)
            proxy = 'proxy_alex:DbrnjhbZ88@141.145.205.4:31281'
            login_password, ip_port = proxy.split('@')
            login, password = login_password.split(':')
            ip, port = ip_port.split(':')
            proxy_url = f'http://{login}:{password}@{ip}:{port}'
            proxy_dict = {'http': proxy_url, 'https': proxy_url}
            params = {
                'user_addr': wallet,
                'start_time': start_time,
                'page_count': '20',
            }
            response = requests.get('https://api.debank.com/history/list', proxies=proxy_dict, params=params,
                                    headers=headers)
            if response.status_code == 200:
                print(f'{proxy_dict}--------------------------{response.status_code}')
                # if os.path.exists(filename):  # Проверка на существование файла
                #     print(f"File {filename} already exists. Skipping.")
                #     break
                json_data = response.json()

                with open(f'{wallet}_{start_time}.json', 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл

                if len(json_data['data']['history_list']) == 0:
                    break  # выход из цикла, если history_list пуст

                # Обновляем start_time на значение time_at последнего элемента
                for j in json_data['data']['history_list'][-1:]:
                    time_at = int(j['time_at'])

                if time_at == date:
                    break  # выход из цикла, если time_at равен date

                start_time = time_at  # обновляем start_time для следующего запроса
                time.sleep(60)
            elif response.status_code == 429:
                print(proxy_dict)
                continue
                # if os.path.exists(filename):  # Проверка на существование файла
                #     print(f"File {filename} already exists. Skipping.")
                #     continue

    #
    # timestamp = 1694034661
    # dt_object = datetime.datetime.fromtimestamp(timestamp)
    #
    # print(dt_object)
    #
    # Создать объект datetime для даты 2023-08-13 00:00:00
    # dt_object = datetime.datetime(year=2023, month=7, day=9, hour=11, minute=47, second=14)
    #
    # # Перевести объект datetime в Unix-время
    # timestamp = int(dt_object.timestamp())
    #
    # print(timestamp)


def get_api():
    for wallet, date in get_wallet():  # Итерируемся по всем кошелькам и датам
        headers = {
            'accept': 'application/json',
            'AccessKey': '09ac3e9d6bce2b9b97672400bc3adf7ab2c2f279',
        }

        start_time = 0
        while True:
            filename = f'{wallet}_{start_time}.json'

            if os.path.exists(filename):  # Проверка на существование файла
                print(f"File {filename} already exists. Skipping.")
                continue
            params = {
                'chain': '',
                'start_time': start_time,
                'page_count': '20',
                'id': wallet,
            }
            response = requests.get('https://pro-openapi.debank.com/v1/user/all_history_list', params=params,
                                    headers=headers)
            json_data = response.json()

            with open(f'{wallet}_{start_time}.json', 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)  # Записываем в файл

            if len(json_data['history_list']) == 0:
                break  # выход из цикла, если history_list пуст

            # Обновляем start_time на значение time_at последнего элемента
            for j in json_data['history_list'][-1:]:
                time_at = int(j['time_at'])

            if time_at == date:
                break  # выход из цикла, если time_at равен date

            start_time = time_at  # обновляем start_time для следующего запроса


def par_json():
    folder = r'c:\scrap_tutorial-master\debank_com\data_json\*.json'
    files_html = glob.glob(folder)
    with (open(f"result.csv", "w",
               errors='ignore', encoding="utf-8") as file_csv):
        writer = csv.writer(file_csv, delimiter=",")
        writer.writerow(
            (
                'wallet', 'cate_id', 'cex_id', 'chain', 'id', 'is_scam', 'other_addr', 'project_id', 'cate_id',
                'receives_amount', 'receives_from_addr', 'receives_token_id', 'sends_amount', 'sends_to_addr',
                'sends_token_id', 'time_at', 'token_approve_spender', 'token_approve_token_id', 'token_approve_value',
                'tx_from_eth_gas_fee', 'tx_from_addr', 'tx_message',
                'tx_name', 'tx_selector', 'tx_status', 'tx_to_addr', 'tx_usd_gas_fee', 'tx_value'
            ))
        for item in files_html:
            file_name = os.path.splitext(os.path.basename(item))[0]
            # Разделяем имя файла по символу "_"
            parts = file_name.split('_')

            # Возьмем первую часть разделенного имени файла
            wallet = parts[0]

            with open(item, 'r', encoding="utf-8") as f:
                data_json = json.load(f)
                for j in data_json['history_list']:

                    # for j in data_json['data']['history_list']:
                    cate_id = j['cate_id']
                    cex_id = j['cex_id']
                    chain = j['chain']
                    j_id = j['id']
                    is_scam = j['is_scam']
                    other_addr = j['other_addr']
                    project_id = j['project_id']

                    receives_data = j.get("receives", [])
                    receives_amount = receives_data[0].get('amount') if receives_data and 'amount' in receives_data[
                        0] else None
                    receives_from_addr = receives_data[0].get('from_addr') if receives_data and 'from_addr' in \
                                                                              receives_data[0] else None
                    receives_token_id = receives_data[0].get('token_id') if receives_data and 'token_id' in \
                                                                            receives_data[0] else None

                    sends_data = j.get("sends", [])
                    sends_amount = sends_data[0].get('amount') if sends_data and 'amount' in sends_data[0] else None
                    sends_price = sends_data[0].get('price') if sends_data and 'price' in sends_data[0] else None
                    sends_to_addr = sends_data[0].get('to_addr') if sends_data and 'to_addr' in sends_data[0] else None
                    sends_token_id = sends_data[0].get('token_id') if sends_data and 'token_id' in sends_data[
                        0] else None

                    time_at = int(j['time_at'])
                    token_approve_data = j.get("token_approve", [])
                    token_approve_spender = token_approve_data.get('spender') if token_approve_data and 'spender' in \
                                                                                    token_approve_data else None
                    token_approve_token_id = token_approve_data.get(
                        'token_id') if token_approve_data and 'token_id' in token_approve_data else None
                    token_approve_value = token_approve_data.get('value') if token_approve_data and 'value' in \
                                                                                token_approve_data else None

                    tx_data = j.get("tx", [])
                    tx_from_eth_gas_fee = tx_data.get('eth_gas_fee') if tx_data and 'eth_gas_fee' in tx_data else None
                    tx_from_addr = tx_data.get('from_addr') if tx_data and 'from_addr' in tx_data else None
                    tx_message = tx_data.get('message') if tx_data and 'message' in tx_data else None
                    tx_name = tx_data.get('name') if tx_data and 'name' in tx_data else None
                    tx_selector = tx_data.get('selector') if tx_data and 'selector' in tx_data else None
                    tx_status = tx_data.get('status') if tx_data and 'status' in tx_data else None
                    tx_to_addr = tx_data.get('to_addr') if tx_data and 'to_addr' in tx_data else None
                    tx_usd_gas_fee = tx_data.get('usd_gas_fee') if tx_data and 'usd_gas_fee' in tx_data else None
                    tx_value = tx_data.get('value') if tx_data and 'value' in tx_data else None

                    datas = [wallet, cate_id, cex_id, chain, j_id, is_scam, other_addr, project_id, cate_id,
                             receives_amount, receives_from_addr, receives_token_id, sends_amount,
                             sends_to_addr, sends_token_id, time_at, token_approve_spender, token_approve_token_id,
                             token_approve_value, tx_from_eth_gas_fee, tx_from_addr,
                             tx_message, tx_name, tx_selector, tx_status, tx_to_addr, tx_usd_gas_fee, tx_value]
                    writer.writerow(datas)


if __name__ == '__main__':
    # main()
    # get_api()
    # get_wallet()
    par_json()