import json
import re


def secToTimecode(t):
    s, ms = divmod(t, 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d,%03d" % (h, m, s, ms)


print(r'''draft_info.json
- Windows: C:\Users\Admin\AppData\Local\JianyingPro\User Data\Projects\com.lveditor.draft
- Android: /data/data/com.lemon.lv/files/newdrafts/
- MacOS: /Users/Admin/Movies/JianyinPro/User Data/Projects/com.lveditor.draft/'''
      )

json_path = input("`draft_info.json` path of JianYing: ")
with open(json_path, "r") as f:
    data = json.load(f)

text_list = data['materials']['texts']
texts_dict = {t['id']: t for t in text_list}

srt_index = 1
srt_content, raw_content = "", ""
contents = []
for track in data['tracks']:
    for segment in track['segments']:
        text_id = segment['material_id']

        if text_id not in texts_dict:
            continue

        timerange = segment['target_timerange']
        content = texts_dict[text_id]['content']
        content = re.sub(r"</?(?:font|color|size).*?>", "",
                         content).strip("[]")

        contents.append(content)

        startTime = secToTimecode(int(timerange["start"]) / 1000)
        endTime = secToTimecode(
            (int(timerange["start"]) + int(timerange["duration"])) / 1000)

        srt_content += f'{srt_index}\n{startTime} --> {endTime}\n{content}\n\n'
        raw_content += f'{content}\n'
        srt_index += 1

with open(f"out/subtitle.srt", "w") as f:
    f.write(srt_content)

with open(f"out/subtitle.txt", "w") as f:
    f.write("\n".join(contents))
