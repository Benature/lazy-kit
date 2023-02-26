import re
import os

import asyncio
from aiohttp import ClientSession
import time


async def fetch(client, url, folder):
    ts_name = re.findall(r"\.mp4/(.*?\.ts)\?", url)[0]
    file_path = os.path.join(folder, ts_name)
    if os.path.exists(file_path):
        return None
    async with client.get(url) as resp:
        assert resp.status == 200
        content = await resp.read()
        # content = await resp.text()
        with open(file_path, 'bw') as f:
            f.write(content)
        print("", ts_name, end="|")
        return resp


async def main(IDX):
    print(IDX)
    with open(f"m3u8/index-{IDX}.m3u8", "r") as f:
        m3u8 = f.read()
    ts_list = re.findall(r"\n(http.*?)\n", m3u8)

    folder = f"ts/ts-{IDX}"
    if not os.path.exists(folder):
        os.mkdir(folder)

    async with ClientSession() as client:
        for url in ts_list:
            html = await fetch(client, url, folder)
            # print(html)


IDX = 2
while IDX >= 1:
    # await main(IDX) # in jupyter notebook
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(IDX))
    IDX -= 1