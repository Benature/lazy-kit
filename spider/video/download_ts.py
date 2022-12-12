import requests
import re
import os
import time

IDX = 11
with open(f"m3u8/index-{IDX}.m3u8", "r") as f:
    m3u8 = f.read()
ts_list = re.findall(r"\n(http.*?)\n", m3u8)

folder = f"ts/ts-{IDX}"
if not os.path.exists(folder):
    os.mkdir(folder)

while IDX >= 1:
    with open(f"m3u8/index-{IDX}.m3u8", "r") as f:
        m3u8 = f.read()
    ts_list = re.findall(r"\n(http.*?)\n", m3u8)

    folder = f"ts/ts-{IDX}"
    if not os.path.exists(folder):
        os.mkdir(folder)

    while True:
        try:
            for i, ts_url in enumerate(ts_list):
                print(i, end="| ")
                ts_name = re.findall(r"\.mp4/(.*?\.ts)\?", ts_url)[0]
                file_path = os.path.join(folder, ts_name)
                if os.path.exists(file_path):
                    continue
                response = requests.get(ts_url)
                with open(file_path, 'bw') as f:
                    f.write(response.content)
                print(end='.')
            break
        except:
            time.sleep(5)

    IDX -= 1
