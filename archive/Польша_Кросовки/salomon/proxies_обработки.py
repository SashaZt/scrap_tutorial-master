# proxies = [
#     ("185.112.12.243", 2831, "36507", "E6KMONDv"),
#     ("185.112.13.180", 2831, "36507", "E6KMONDv"),
#     ("185.112.14.176", 2831, "36507", "E6KMONDv"),
#     ("185.112.15.138", 2831, "36507", "E6KMONDv"),
#     ("195.123.189.188", 2831, "36507", "E6KMONDv"),
#     ("195.123.190.14", 2831, "36507", "E6KMONDv"),
#     ("195.123.193.74", 2831, "36507", "E6KMONDv"),
#     ("195.123.194.171", 2831, "36507", "E6KMONDv"),
#     ("195.123.252.247", 2831, "36507", "E6KMONDv"),
#     ("212.86.111.168", 2831, "36507", "E6KMONDv")
# ]
"""Создавать список серверов для дальнейшего использования"""
# proxies = [
#     ('195.201.161.3', 20561, 'zBoGZh5PqsrQ', 'AIILgcGVH0'),
#     ('193.124.190.63', 9317, 'rdZvZY', '4hB2v9'),
#     ('194.67.201.189', 9874, 'rdZvZY', '4hB2v9'),
#     ('194.67.202.219', 9973, 'rdZvZY', '4hB2v9'),
#     ('194.67.200.169', 9485, 'rdZvZY', '4hB2v9'),
#     ('194.67.202.109', 9013, 'rdZvZY', '4hB2v9'),
#     ('194.67.201.44', 9798, 'rdZvZY', '4hB2v9'),
#     ('194.67.201.206', 9707, 'rdZvZY', '4hB2v9'),
#     ('193.124.191.145', 9587, 'rdZvZY', '4hB2v9'),
#     ('194.67.201.205', 9292, 'rdZvZY', '4hB2v9'),
#     ('194.67.200.64', 9821, 'rdZvZY', '4hB2v9'),
#     ('194.67.202.181', 9851, 'QWyoUo', 'nRTyzY'),
#     ('194.67.202.134', 9450, 'QWyoUo', 'nRTyzY'),
#     ('194.67.202.205', 9319, 'QWyoUo', 'nRTyzY'),
#     ('194.67.202.203', 9417, 'QWyoUo', 'nRTyzY'),
#     ('194.67.202.108', 9223, 'QWyoUo', 'nRTyzY'),
#     ('193.124.191.159', 9233, 'QWyoUo', 'nRTyzY'),
#     ('194.67.202.29', 9387, 'QWyoUo', 'nRTyzY'),
#     ('194.67.202.198', 9839, 'QWyoUo', 'nRTyzY'),
#     ('194.67.201.2', 9043, 'QWyoUo', 'nRTyzY'),
#     ('194.67.201.51', 9636, 'QWyoUo', 'nRTyzY'),
#     ('45.130.63.195', 8000, 'Jk8UKx', 'Ur5JsP'),
#     ('45.130.62.96', 8000, 'Jk8UKx', 'Ur5JsP'),
#     ('45.147.180.108', 8000, 'Jk8UKx', 'Ur5JsP'),
#     ('45.147.183.98', 8000, 'Jk8UKx', 'Ur5JsP'),
#     ('45.147.181.49', 8000, 'Jk8UKx', 'Ur5JsP'),
#     ('45.147.180.14', 8000, 'Jk8UKx', 'Ur5JsP'),
#     ('45.147.183.225', 8000, 'Jk8UKx', 'Ur5JsP'),
#     ('45.147.181.108', 8000, 'Jk8UKx', 'Ur5JsP'),
#     ('45.147.183.241', 8000, 'Jk8UKx', 'Ur5JsP'),
#     ('45.147.180.93', 8000, 'Jk8UKx', 'Ur5JsP'),
#     ('45.147.180.225', 8000, 'Jk8UKx', 'Ur5JsP'),
#     ('45.147.180.132', 8000, 'Jk8UKx', 'Ur5JsP'),
#     ('45.147.182.246', 8000, 'Jk8UKx', 'Ur5JsP'),
#     ('45.147.183.243', 8000, 'Jk8UKx', 'Ur5JsP'),
#     ('45.147.183.42', 8000, 'Jk8UKx', 'Ur5JsP'),
#     ('45.147.183.146', 8000, 'Jk8UKx', 'Ur5JsP'),
#     ('45.147.182.245', 8000, 'Jk8UKx', 'Ur5JsP'),
#     ('45.147.181.136', 8000, 'Jk8UKx', 'Ur5JsP'),
#     ('45.147.183.214', 8000, 'Jk8UKx', 'Ur5JsP'),
#     ('45.147.180.227', 8000, 'Jk8UKx', 'Ur5JsP'),
#     ('176.107.185.49', 2831, '36375', 'JKBiu6VB6v3yy'),
#     ('176.107.188.41', 2831, '36375', 'JKBiu6VB6v3yy'),
#     ('176.107.191.36', 2831, '36375', 'JKBiu6VB6v3yy'),
#     ('193.22.97.44', 2831, '36375', 'JKBiu6VB6v3yy'),
#     ('193.22.99.32', 2831, '36375', 'JKBiu6VB6v3yy'),
#     ('139.28.38.78', 2831, '36375', 'JKBiu6VB6v3yy'),
#     ('139.28.39.35', 2831, '36375', 'JKBiu6VB6v3yy'),
#     ('45.9.236.47', 2831, '36375', 'JKBiu6VB6v3yy'),
#     ('45.9.237.39', 2831, '36375', 'JKBiu6VB6v3yy'),
#     ('45.9.238.120', 2831, '36375', 'JKBiu6VB6v3yy'),
#     ('193.32.153.160', 8000, 'd36jTZ', 'YVoxdp'),
#     ('193.32.153.233', 8000, 'd36jTZ', 'YVoxdp'),
#     ('193.32.153.66', 8000, 'd36jTZ', 'YVoxdp'),
#     ('193.32.153.250', 8000, 'd36jTZ', 'YVoxdp'),
#     ('193.32.155.53', 8000, 'd36jTZ', 'YVoxdp'),
#     ('193.32.154.223', 8000, 'd36jTZ', 'YVoxdp'),
#     ('193.32.153.77', 8000, 'd36jTZ', 'YVoxdp'),
#     ('193.32.153.241', 8000, 'd36jTZ', 'YVoxdp'),
#     ('193.32.152.234', 8000, 'd36jTZ', 'YVoxdp'),
#     ('193.32.153.103', 8000, 'd36jTZ', 'YVoxdp'),
#     ('185.112.12.243', 2831, '36507', 'E6KMONDv'),
#     ('185.112.13.180', 2831, '36507', 'E6KMONDv'),
#     ('185.112.14.176', 2831, '36507', 'E6KMONDv'),
#     ('185.112.15.138', 2831, '36507', 'E6KMONDv'),
#     ('195.123.189.188', 2831, '36507', 'E6KMONDv'),
#     ('195.123.190.14', 2831, '36507', 'E6KMONDv'),
#     ('195.123.193.74', 2831, '36507', 'E6KMONDv'),
#     ('195.123.194.171', 2831, '36507', 'E6KMONDv'),
#     ('195.123.252.247', 2831, '36507', 'E6KMONDv'),
#     ('212.86.111.168', 2831, '36507', 'E6KMONDv')
# ]
proxies = [

    ('193.124.190.63', 9317, 'rdZvZY', '4hB2v9'), ('194.67.201.189', 9874, 'rdZvZY', '4hB2v9'),
    ('194.67.202.219', 9973, 'rdZvZY', '4hB2v9'), ('194.67.200.169', 9485, 'rdZvZY', '4hB2v9'),
    ('194.67.202.109', 9013, 'rdZvZY', '4hB2v9'), ('194.67.201.44', 9798, 'rdZvZY', '4hB2v9'),
    ('194.67.201.206', 9707, 'rdZvZY', '4hB2v9'), ('193.124.191.145', 9587, 'rdZvZY', '4hB2v9'),
    ('194.67.201.205', 9292, 'rdZvZY', '4hB2v9'), ('194.67.200.64', 9821, 'rdZvZY', '4hB2v9'),
    ('194.67.202.181', 9851, 'QWyoUo', 'nRTyzY'), ('194.67.202.134', 9450, 'QWyoUo', 'nRTyzY'),
    ('194.67.202.205', 9319, 'QWyoUo', 'nRTyzY'), ('194.67.202.203', 9417, 'QWyoUo', 'nRTyzY'),
    ('194.67.202.108', 9223, 'QWyoUo', 'nRTyzY'), ('193.124.191.159', 9233, 'QWyoUo', 'nRTyzY'),
    ('194.67.202.29', 9387, 'QWyoUo', 'nRTyzY'), ('194.67.202.198', 9839, 'QWyoUo', 'nRTyzY'),
    ('194.67.201.2', 9043, 'QWyoUo', 'nRTyzY'), ('194.67.201.51', 9636, 'QWyoUo', 'nRTyzY'),
    ('45.130.63.195', 8000, 'Jk8UKx', 'Ur5JsP'), ('45.130.62.96', 8000, 'Jk8UKx', 'Ur5JsP'),
    ('45.147.180.108', 8000, 'Jk8UKx', 'Ur5JsP'), ('45.147.183.98', 8000, 'Jk8UKx', 'Ur5JsP'),
    ('45.147.181.49', 8000, 'Jk8UKx', 'Ur5JsP'), ('45.147.180.14', 8000, 'Jk8UKx', 'Ur5JsP'),
    ('45.147.183.225', 8000, 'Jk8UKx', 'Ur5JsP'), ('45.147.181.108', 8000, 'Jk8UKx', 'Ur5JsP'),
    ('45.147.183.241', 8000, 'Jk8UKx', 'Ur5JsP'), ('45.147.180.93', 8000, 'Jk8UKx', 'Ur5JsP'),
    ('45.147.180.225', 8000, 'Jk8UKx', 'Ur5JsP'), ('45.147.180.132', 8000, 'Jk8UKx', 'Ur5JsP'),
    ('45.147.182.246', 8000, 'Jk8UKx', 'Ur5JsP'), ('45.147.183.243', 8000, 'Jk8UKx', 'Ur5JsP'),
    ('45.147.183.42', 8000, 'Jk8UKx', 'Ur5JsP'), ('45.147.183.146', 8000, 'Jk8UKx', 'Ur5JsP'),
    ('45.147.182.245', 8000, 'Jk8UKx', 'Ur5JsP'), ('45.147.181.136', 8000, 'Jk8UKx', 'Ur5JsP'),
    ('45.147.183.214', 8000, 'Jk8UKx', 'Ur5JsP'), ('45.147.180.227', 8000, 'Jk8UKx', 'Ur5JsP'),
    ('176.107.185.49', 2831, '36375', 'JKBiu6VB6v3yy')
]

# """Код для проверки прокси серверов"""
# import requests
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}
# work_proxy = []
# try:
#     for i in proxies:
#         PROXY_HOST = i[0]
#         PROXY_PORT = i[1]
#         PROXY_USER = i[2]
#         PROXY_PASS = i[3]
#         # print(PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
#         proxies = {
#             "http": f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}",
#             "https": f"https://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"
#         }
#         # print(proxies)
#         r = requests.get('http://ident.me/', headers=headers, proxies=proxies, timeout=1)
#         # print(r.text)
#
#         if PROXY_HOST == r.text:
#             work_proxy.append((PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS))
# except:
#     print(f'Не рабочие прокси {proxies}')
# print(work_proxy)


"""Код для создание списка серверов"""
proxy_list = """
36675:g6Qply4q@185.112.12.122:2831
36675:g6Qply4q@185.112.14.126:2831
36675:g6Qply4q@185.112.15.239:2831
36675:g6Qply4q@195.123.189.137:2831
36675:g6Qply4q@195.123.190.104:2831
36675:g6Qply4q@195.123.193.81:2831
36675:g6Qply4q@195.123.194.134:2831
36675:g6Qply4q@195.123.197.233:2831
36675:g6Qply4q@195.123.252.157:2831
36675:g6Qply4q@212.86.111.68:2831
"""

# Разделение списка на отдельные строки
proxy_servers = proxy_list.split("\n")

result_list = []

# Обработка каждой строки
for server in proxy_servers:
    if server.strip() == "":
        continue  # Пропустить пустые строки

    # Разделение строки на отдельные значения
    split_list = server.split("@")

    # Извлечение IP-адреса и порта
    ip_port = split_list[1].split(":")
    ip_address = ip_port[0]
    port = int(ip_port[1])

    # Извлечение числа и строки из первого элемента
    first_element = split_list[0].split(":")
    number = first_element[0]
    string = first_element[1]

    # Добавление результатов в список
    result_list.append((ip_address, port, number, string))

# Вывод результирующего списка
for result in result_list:
    print(f'{result},')
