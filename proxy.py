import requests
import asyncio


class Proxy:
    proxy_url = ['https://www.proxy-list.download/api/v1/get?type=http',
                 'http://free-proxy.cz/ru/']
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
