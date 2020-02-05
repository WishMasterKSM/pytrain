import aiohttp
import asyncio

from bs4 import BeautifulSoup

semaphore = asyncio.Semaphore(10)

global_urls = list()

def extract_urls(html, urls):
    soup = BeautifulSoup(html)
    for link in soup.findAll('a'):
        new_url = link.get('href')
        print(new_url)
        if new_url.startswith('http') == True:
            if 'facebook' not in new_url:
                urls.append(new_url)

async def inspect(url, session):
    urls = list()
    async with semaphore:
        try:
            async with session.get(url, ssl=False) as resp:
                if resp.status == 200:
                    extract_urls(await resp.text(), urls)
        except aiohttp.client_exceptions.ServerDisconnectedError:
            print('Server disconnected')
        except:
            print('Unknown exception')
    for u in urls:
        if u not in global_urls:
            global_urls.append(u)
            await inspect(u, session)

async def main(url):
    t = aiohttp.ClientTimeout(10)
    async with aiohttp.ClientSession(timeout=t) as session:
        await inspect(url,session)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main('https://tapkinalapki.com.ua'))
