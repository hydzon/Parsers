import json
import random
import time
import requests
import asyncio
import re
import os

from bs4 import BeautifulSoup


class Proxy:
    proxy_url = ['https://spys.me/proxy.txt', 'http://free-proxy.cz/ru/']
    proxy_list = []

    def __init__(self):
        if os.path.isfile('url_list.json') and (time.time() - os.path.getmtime('url_list.json')) / 60 < 60:
            with open(f'url_list.json', 'r', encoding='utf-8') as f:
                self.proxy_list = list(json.load(f))
            if len(self.proxy_list) == 0:
                self.load_proxies_list()
        else:
            self.load_proxies_list()

    def load_proxies_list(self):
        response = requests.get(self.proxy_url[0])
        self.proxy_list = re.findall(r'\b\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d{1,5}\b', response.text)
        if len(self.proxy_list):
            with open(f'url_list.json', 'w', encoding='utf-8') as f:
                json.dump({el: '' for el in self.proxy_list}, f, ensure_ascii=False, indent=4)
        else:
            with open(f'proxies.html', 'r', encoding='utf-8') as html_file:
                soup = BeautifulSoup(html_file, 'lxml')
            dict_proxies = {}
            for tr in soup.find_all(class_=re.compile('spy1x'))[2:]:
                if tr.find_all('td')[1].find('font', class_='spy14'):
                    dict_proxies[tr.find('td').find('font').text] = tr.find_all('td')[1].find('font').text + 'S'
                else:
                    dict_proxies[tr.find('td').find('font').text] = tr.find_all('td')[1].find('font').text
            with open(f'url_list.json', 'w', encoding='utf-8') as f:
                json.dump(dict_proxies, f, ensure_ascii=False, indent=4)

    def check_proxy_list(self):
        asyncio.run(self.async_check_proxy_list())
        print('Proxy list checked')

    def get_random_proxy(self):
        return random.choice(self.proxy_list)

    @staticmethod
    async def async_check_proxy(self, proxy_url):
        try:
            response = await asyncio.to_thread(requests.get,
                                    'https://www.google.com',
                                    proxies={"http://": "http://" + proxy_url},
                                    timeout=10)
        except IOError:
            print(f'{proxy_url}: IOError')
        except Exception:
            print(f'{proxy_url}: ERROR CONNECT')
        else:
            print(f'{proxy_url}: {response.status_code}')

    async def async_check_proxy_list(self):
        task_list = []
        for proxy in self.proxy_list:
            task_list.append(asyncio.create_task(self.async_check_proxy(proxy)))
        await asyncio.gather(*task_list)


def main():
    print(len(Proxy().proxy_list))


if __name__ == '__main__':
    main()
