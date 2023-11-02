import json
import re
import os
import sys
import platform
import getpass


def secToTimecode(t):
    s, ms = divmod(t, 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d,%03d" % (h, m, s, ms)


def get_project():

    username = getpass.getuser()
    draft_dir_dict = {
        'Windows':
        rf'C:\Users\{username}\AppData\Local\JianyingPro\User Data\Projects\com.lveditor.draft',
        'Darwin':
        f'/Users/{username}/Movies/JianyingPro/User Data/Projects/com.lveditor.draft',
    }

    draft_dir = draft_dir_dict[platform.system()]

    projects = sorted(
        [dd for dd in os.listdir(draft_dir) if not dd.endswith('.json')],
        key=lambda x: os.path.getmtime(os.path.join(draft_dir, x)),
        reverse=True)

    if os.path.exists(
            os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         '.fast_JY.ignore')) == False:
        # a self added file, to fast up project selection (default the latest one)
        print(r'''draft_info.json
- Windows: C:\Users\Admin\AppData\Local\JianyingPro\User Data\Projects\com.lveditor.draft
- Android: /data/data/com.lemon.lv/files/newdrafts/
- MacOS: /Users/Admin/Movies/JianyinPro/User Data/Projects/com.lveditor.draft/'''
              )
        print(projects)
        json_path = input(
            f"`draft_info.json` path of JianYing: (default: {projects[0]})\n")
    else:
        print("Retrieve data from", projects[0])
        json_path = ""
    json_path = os.path.join(
        draft_dir, projects[0],
        "draft_info.json") if json_path.strip() == "" else json_path
    print(json_path)
    with open(json_path, "r") as f:
        data = json.load(f)
    return data


data = get_project()

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

if len(contents) == 0:
    print("No subtitle found")
    sys.exit()

try:
    video = data['materials']['videos'][0]
    video_path = video['path']

    srt_path = os.path.splitext(video_path)[0] + ".srt"
    print("Output path:", srt_path)
    if os.path.exists(srt_path):
        cmd_tmp = input(
            "File already exists. Enter to go on... (`q` to quit) ")
        if cmd_tmp.strip().lower() == "q":
            sys.exit()
    print("File name:", os.path.basename(srt_path))

    with open(srt_path, "w") as f:
        f.write(srt_content)
    video_folder = os.path.dirname(video_path)
    txt_dir = os.path.join(video_folder, "txt")
    if not os.path.exists(txt_dir):
        os.makedirs(txt_dir)
    with open(
            os.path.join(
                txt_dir,
                os.path.basename(os.path.splitext(video_path)[0]) + '.txt'),
            "w") as f:
        f.write("\n".join(contents))

except Exception as e:
    print(e)
    with open(f"out/subtitle.srt", "w") as f:
        f.write(srt_content)

    with open(f"out/subtitle.txt", "w") as f:
        f.write("\n".join(contents))
