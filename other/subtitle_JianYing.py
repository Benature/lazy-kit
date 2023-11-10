import json
import re
import os
import platform
import getpass


def secToTimecode(t):
    s, ms = divmod(t, 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d,%03d" % (h, m, s, ms)

username = getpass.getuser()
draft_dir_dict = {
    'Windows':
    rf'C:\Users\{username}\AppData\Local\JianyingPro\User Data\Projects\com.lveditor.draft',
    'Darwin':
    f'/Users/{username}/Movies/JianyingPro/User Data/Projects/com.lveditor.draft',
}
draft_json_fn = {
    'Windows': 'draft_content.json',
    'Darwin': 'draft_info.json',
}[platform.system()]


def get_project():
    fast_config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.fast_JY.ignore')
    if os.path.exists(fast_config_path):
        with open(fast_config_path, 'r') as f:
            config_content = f.read()
            draft_dir_re_finds = re.findall(r"draft_dir=(.*)", config_content)
        if len(draft_dir_re_finds) == 0:
            draft_dir = draft_dir_dict[platform.system()]
        else:
            draft_dir = draft_dir_re_finds[0].strip()
            print("config set path as:", draft_dir)
            
    else:
        draft_dir = draft_dir_dict[platform.system()]

    projects = sorted(
        [dd for dd in os.listdir(draft_dir) if not dd.endswith('.json')],
        key=lambda x: os.path.getmtime(os.path.join(draft_dir, x)),
        reverse=True)

    
    if os.path.exists(fast_config_path) == False:
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
        draft_json_fn) if json_path.strip() == "" else json_path
    print(json_path)
    with open(json_path, "r", encoding="utf8") as f:
        data = json.load(f)
    return data


class VIDEO_INFO:
    def __init__(self, path, duration):
        self.path = path
        self.duration = int(duration)
        
        self.srt_content = ""
        self.raw_content = ""
        self.contents = []
        

def analysis_videos(data):
    video_infos = []
    for video in data['materials']['videos']:
        if len(video_infos) > 0 and video_infos[-1].path==video['path']:
            video_infos[-1].duration += int(video['duration'])
        else:
            video_infos.append(VIDEO_INFO(video['path'], video['duration']))
    return video_infos
    

data = get_project()

video_infos = analysis_videos(data)
text_list = data['materials']['texts']
texts_dict = {t['id']: t for t in text_list}

video_idx = 0
prev_video_duration = 0

for track in data['tracks']:
    for segment in track['segments']:
        text_id = segment['material_id']

        if text_id not in texts_dict:
            continue

        timerange = segment['target_timerange']
        current_t = int(timerange["start"])
        
        if current_t > prev_video_duration + video_infos[video_idx].duration:
            video_idx += 1
            prev_video_duration += video_infos[video_idx-1].duration
            # print(video_idx, current_t, video_infos[video_idx-1].duration)

        content = texts_dict[text_id]['content']
        content = re.sub(r"</?(?:font|color|size).*?>", "",
                         content).strip("[]")

        video_infos[video_idx].contents.append(content)

        startTime = secToTimecode((current_t - prev_video_duration) / 1000)
        endTime = secToTimecode((current_t + int(timerange["duration"]) - prev_video_duration) / 1000)

        srt_index = len(video_infos[video_idx].contents)
        video_infos[video_idx].srt_content += f'{srt_index}\n{startTime} --> {endTime}\n{content}\n\n'
        video_infos[video_idx].raw_content += f'{content}\n'

for video_info in video_infos:
    contents = video_info.contents
    srt_content = video_info.srt_content
    
    if len(contents) == 0:
        print("No subtitle found")
        continue

    try:
        video_path = video_info.path

        srt_path = os.path.splitext(video_path)[0] + ".srt"
        print("Output path:", srt_path)
        if os.path.exists(srt_path):
            cmd_tmp = input(
                "File already exists. Enter to go on... (`q` to quit) ")
            if cmd_tmp.strip().lower() == "q":
                continue
        print("File name:", os.path.basename(srt_path))

        with open(srt_path, "w", encoding="utf8") as f:
            f.write(srt_content)
        video_folder = os.path.dirname(video_path)
        txt_dir = os.path.join(video_folder, "txt")
        if not os.path.exists(txt_dir): # touch txt folder
            os.makedirs(txt_dir)
        with open(
                os.path.join(
                    txt_dir,
                    os.path.basename(os.path.splitext(video_path)[0]) + '.txt'),
                "w", encoding="utf8") as f:
            f.write("\n".join(contents))

    except Exception as e:
        print(e)
        with open(f"out/subtitle.srt", "w", encoding="utf8") as f:
            f.write(srt_content)

        with open(f"out/subtitle.txt", "w", encoding="utf8") as f:
            f.write("\n".join(contents))
