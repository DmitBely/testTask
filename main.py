import aiohttp
import asyncio
import hashlib
import urllib.parse


async def download_and_hash(url, session):
    async with session.get(url) as response:
        if response.status != 200:
            raise ValueError(f"HTTP error {response.status}")
        content = await response.read()
        return hashlib.md5(content).hexdigest()


async def download_and_hash_all(semaphore, session, url_list, output_dir):
    tasks = []
    for url in url_list:
        tasks.append(asyncio.create_task(download_and_hash(url, session)))
    results = await asyncio.gather(*tasks)
    return results


async def main():
    CONCURRENT_REQUESTS = 5
    async with aiohttp.ClientSession() as session:
        results = await download_and_hash_all(
            asyncio.Semaphore(CONCURRENT_REQUESTS),
            session,
            ['https://gitea.radium.group/radium/project-configuration'],
            'temp'
        )
    print(results)

if __name__ == '__main__':
    asyncio.run(main())
