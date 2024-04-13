import os
import re
import json
import requests
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# headers = {
#     # 'Accept': '*/*',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
#               'application/signed-exchange;v=b3;q=0.7',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                   'Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36'
# }


class Proxy:
    proxy_url = ['https://www.proxy-list.download/api/v1/get?type=http', 'http://free-proxy.cz/ru/']
    proxy_list = []

    def __init__(self, proxy_url=''):
        pass
        # if proxy_url:
        #     self.proxy_url = proxy_url
        # else:
        #     response = requests.get(self.proxy_url[0])
        #     if response.status_code == 200:
        #         self.proxy_list = response.text.strip().split('\r\n')
        #         with open(f'url_list.json', 'w', encoding='utf-8') as f:
        #             json.dump({el: '' for el in self.proxy_list}, f, ensure_ascii=False, indent=4)
        #     else:
        #         with open(f'url_list.json', 'r', encoding='utf-8') as f:
        #             self.proxy_list = list(json.load(f))

    def check_proxy_list(self):
        asyncio.run(self.async_check_proxy_list())
        print('Proxy list checked')

    async def async_check_proxy(self, proxy_url):
        try:
            response = await asyncio.to_thread(requests.get, 'http://' + proxy_url)
            if await response.status_code != 200:
                # self.proxy_list.pop(proxy_url)
                print(f'{proxy_url}: OK')
            else:
                print(f'{proxy_url}: ERROR CONNECT')
        except Exception as e:
            print(f'{proxy_url}: ERROR CONNECT')

    async def async_check_proxy_list(self):
        task_list = []
        for proxy in self.proxy_list:
            task_list.append(asyncio.create_task(self.async_check_proxy(proxy)))
        await asyncio.gather(*task_list)


def main():
    '''
    '''
    # session = requests.Session()
    # proxy_url = 'http://free-proxy.cz/ru/proxylist/country/all/http/uptime/all'
    # response = session.get(proxy_url, headers=headers)
    # soup = BeautifulSoup(response.text, 'lxml')
    # print(soup.find('h3').text)
    #
    # # print(soup.find('table', id='proxy_list').find_all('tr'))
    # for tr in soup.find('table', id='proxy_list').find_all('tr')[1:]:
    #     if tr.find('td'):
    #         print(tr.find('td').text)
    #     print(tr)
    #     break
    # print(response.text)
    # with open('test.html', 'w', encoding='utf-8') as file:
    #     file.write(response.text)
    # print(re.search(r'\b\d+\b', soup.find('h3').text))

    # print(json.dumps(requests.get('https://www.proxy-list.download/api/v1/get?type=http').text, indent=4))

    # lst = requests.get('https://www.proxy-list.download/api/v1/get?type=http').text.strip().split('\r\n')
    # u_dict = {el: '' for el in lst}
    # with open(f'url_list.json', 'w', encoding='utf-8') as f:
    #     json.dump(u_dict, f, ensure_ascii=False, indent=4)

    # with open(f'url_list.json', 'r', encoding='utf-8') as f:
    #     print(list(json.load(f)))

    # proxy = Proxy()
    # print(len(proxy.proxy_list))
    # for proxy in proxy.proxy_list:
    #     try:
    #         if requests.get('http://' + proxy).status_code == 200:
    #             print(f'{proxy}: OK')
    #         else:
    #             print(f'{proxy}: ERROR CONNECT')
    #     except ConnectionRefusedError as e:
    #         print(f'{proxy}: ERROR CONNECT')
    #     except Exception as e:
    #         print(f'{proxy}: ERROR CONNECT')
    # proxy.check_proxy_list()
    # print(len(proxy.proxy_list))

    # headers = {
    #     'Accept': '*/*',
    #     'Accept-Language': 'ru,en;q=0.9',
    #     'Connection': 'keep-alive',
    #     'Content-Type': 'text/plain;charset=UTF-8',
    #     'Origin': 'http://free-proxy.cz',
    #     'Referer': 'http://free-proxy.cz/',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
    #     'Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36'
    # }
    #
    # data = {
    #     "result": 0,
    #     "method": "wsm.sessionActivated",
    #     "parameters": "{\"title\":\"свежий список прокси | Free-Proxy.cz\"}"
    # }
    #
    # response = requests.get('http://gc.kis.v2.scr.kaspersky-labs.com/090B8C9F-FD43-4933-AEA0-7BBE0B212988/'
    #                         'CBB067BC-1D04-45E3-8424-07756A67AB58/to/wsm.sessionActivated?'
    #                         'tm=2024-04-13T11%3A07%3A57.389Z',
    #                         headers=headers,
    #                         data=data)
    #
    # print(response.status_code)
    # print(response.content)

    # options = webdriver.ChromeOptions()
    # # binary_yandex_driver_file = 'yandexdriver.exe'
    # browser = webdriver.Chrome(options=options)
    # browser.get('http://free-proxy.cz/ru/proxylist/country/all/http/uptime/all')
    # element = browser.find_element(By.ID, 'clickexport')
    # element.click()
    # generated_html = browser.page_source
    # with open('free-proxy.html', 'w', encoding='utf-8') as f:
    #     f.write(generated_html)

    with open('free-proxy.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'lxml')
    list_proxy = [soup.find('div', id='zkzk').find('br').previousSibling]
    list_proxy += [br.next_sibling for br in soup.find('div', id='zkzk').find_all('br')]
    proxy = Proxy()
    proxy.proxy_list = list_proxy
    proxy.check_proxy_list()


if __name__ == '__main__':
    main()
