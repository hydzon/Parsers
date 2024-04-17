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
    check_urls = ['https://httpbin.org/ip', 'https://icanhazip.com', 'https://api.seeip.org/jsonip']

    # # async_main()
    # response = requests.get(url, proxies={'http': 'socks5://' + '5.59.141.94:1080',
    #                                       'https': 'socks5://' + '5.59.141.94:1080'})
    # session = requests.Session()
    # session.proxies = {
    #     'http': 'http://78.29.33.173:8080',
    #     'https': 'http://78.29.33.173:8080'
    #     # 'socks4': 'http://184.181.217.220:4145',
    #     # 'socks5': 'http://184.181.217.220:4145'
    # }
    # response = session.get(check_urls[0])

    proxy_url = '95.84.166.138:8080'
    proxies = {
        'http': 'http://' + proxy_url,
        'https': 'http://' + proxy_url,
    }
    response = requests.get('https://icanhazip.com',
                            headers=headers,
                            proxies=proxies,
                            timeout=20)
    print(response.url)
    print(response.text)


if __name__ == '__main__':
    main()
