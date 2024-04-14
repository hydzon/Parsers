import aiohttp
from bs4 import BeautifulSoup

from proxy import *
import requests
import json
import asyncio

proxies = Proxy()
headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36'
}


async def async_save_org_page(id):
    try:
        response = await aiohttp.to_thread(requests.get,
                                           f"https://www.list-org.com/company/{id}",
                                           proxies={"http://": "http://" + proxies.get_random_proxy()},
                                           headers=headers)
        print(response)
        with open('files_for_parsing/ogr_id_{id}.html', 'w') as html_file:
            html_file.write(response.text)
    except IOError:
        print(f'{id}: IOError')
    except Exception:
        print(f'{id}: ERROR CONNECT')
    else:
        print(f'{id}: {response.status_code}')


async def async_tasker():
    tasks = []
    for i in range(30):
        tasks.append(asyncio.create_task(async_save_org_page(i)))
    await asyncio.gather(*tasks)


def async_main():
    asyncio.run(async_tasker())


def main():
    '''
        Parser www.list-org.com
    '''
    # with open(f'proxies.html', encoding='utf-8') as file:
    #     soup = BeautifulSoup(file.read(), features="lxml")

    # url = f"https://www.list-org.com/company/2"
    # url = f'https://www.google.com'
    url = 'https://httpbin.org/ip'

    # # async_main()
    # response = requests.get(url, proxies={'http': 'socks5://' + '5.59.141.94:1080',
    #                                       'https': 'socks5://' + '5.59.141.94:1080'})
    session = requests.Session()
    session.proxies = {
        'http': 'http://85.172.0.30:8080',
        'https': 'http://79.111.15.125:8080'
    }
    response = session.get(url)
    print(response.url)
    print(response.text)


if __name__ == '__main__':
    main()
