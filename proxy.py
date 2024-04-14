import json
import time
import requests
import asyncio
import re
import os


class Proxy:
    proxy_url = ['https://spys.me/proxy.txt', 'http://free-proxy.cz/ru/']
    proxy_list = []

    def __init__(self):
        if os.path.isfile('url_list.json') and (time.time() - os.path.getmtime('url_list.json')) / 60 < 60:
            with open(f'url_list.json', 'r', encoding='utf-8') as f:
                self.proxy_list = list(json.load(f))
        else:
            response = requests.get(self.proxy_url[0])
            self.proxy_list = re.findall(r'\b\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d{1,5}\b', response.text)
            with open(f'url_list.json', 'w', encoding='utf-8') as f:
                json.dump({el: '' for el in self.proxy_list}, f, ensure_ascii=False, indent=4)

    def check_proxy_list(self):
        asyncio.run(self.async_check_proxy_list())
        print('Proxy list checked')

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
    pass


if __name__ == '__main__':
    main()
