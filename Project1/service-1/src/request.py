import asyncio

import aiohttp

async def main():
    url = "http://localhost:8000/submit_email/"
    payload = {'id': '1',
               'email': 'test@example.com',
               'inputs': 'example input',
               'language': 'python',
               'enable': '1'}
    files = {'file': open('C:\\Users\\Samin\\Desktop\\test.py', 'rb')}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, files=files) as resp:
            print(await resp.text())

asyncio.run(main())
