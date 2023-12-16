import json
import re
import os
import platform
import getpass
from pathlib import Path


def secToTimecode(t):
    t /= 1000
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
    """找到剪映视频项目的草稿目录"""
    fast_config_path = Path(__file__).resolve().parent / '.fast_JY.ignore'
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

    # sort result: the first = the most recent
    projects = sorted(
        [
            dd for dd in os.listdir(draft_dir)
            if not dd.endswith('.json') and not dd.startswith('.')  # .DS_Store
        ],
        key=lambda x: os.path.getmtime(os.path.join(draft_dir, x)),
        reverse=True)

    if os.path.exists(fast_config_path) == False:
        # a self added file, to fast up project selection (default the latest one)
        print(rf'''draft_info.json
- Windows: C:\Users\{username}\AppData\Local\JianyingPro\User Data\Projects\com.lveditor.draft
- Android: /data/data/com.lemon.lv/files/newdrafts/
- MacOS: /Users/{username}/Movies/JianyinPro/User Data/Projects/com.lveditor.draft/'''
              )
        print(projects)
        json_path = input(
            f"`draft_info.json` path of JianYing: (default: {projects[0]})\n")
    else:
        print("Retrieve data from", projects[0])
        json_path = ""
    json_path = Path(draft_dir, projects[0],
                     draft_json_fn) if json_path.strip() == "" else json_path
    print(str(json_path))
    with open(json_path, "r", encoding="utf8") as f:
        data = json.load(f)
    return data


class VIDEO_INFO:

    def __init__(self, path, duration):
        self.path = Path(path)
        self.duration = int(duration)

        self.srt_content = ""
        self.raw_content = ""
        self.contents = []


def analysis_videos(data):
    """多视频文件情况处理：分析每个视频文件的时长，用于区分字幕属于哪份视频文件。"""
    video_infos = []
    for video in data['materials']['videos']:
        if len(video_infos) > 0 and str(video_infos[-1].path) == video['path']:
            continue
            """
            大概在剪映版本 v5.0.0 之前每一个 video 的 duration 是其单独片段的时长
            v5.0.0 之后是整个视频的时长，每个片段的时长数据存放在 
            `['tracks'][0]['segments'][i]['source_timerange'/'target)timerange']`
            因为不需要用到片段的时长所以全部当作完整视频长度了
            （切片只是为了满足文字识别要求 2h 以内的要求）
            """
            # merge for same file
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
            prev_video_duration += video_infos[video_idx - 1].duration
            # print(video_idx, current_t, video_infos[video_idx-1].duration)

        content = texts_dict[text_id]['content']
        # v5.0.0 之后字幕是 json 格式
        content = json.loads(content)['text']
        # v5.0.0 之前字幕是 html 格式
        # content = re.sub(r"</?(?:font|color|size).*?>", "",content).strip("[]")

        video_infos[video_idx].contents.append(content)

        startTime = secToTimecode(current_t - prev_video_duration)
        endTime = secToTimecode(current_t + int(timerange["duration"]) -
                                prev_video_duration)

        srt_index = len(video_infos[video_idx].contents)
        video_infos[
            video_idx].srt_content += f'{srt_index}\n{startTime} --> {endTime}\n{content}\n\n'
        video_infos[video_idx].raw_content += f'{content}\n'

for video_info in video_infos:
    contents = video_info.contents
    srt_content = video_info.srt_content

    if len(contents) == 0:
        print("No subtitle found")
        continue

    video_path = video_info.path
    video_folder = video_path.parent

    srt_path = video_folder / f"{video_path.stem}.srt"
    print("Output path:", srt_path)
    if srt_path.exists():
        cmd_tmp = input(
            "[WARN] File already exists. Enter to REWRITE the file... (`q` to quit) "
        )
        if cmd_tmp.strip().lower() == "q":
            continue
    print("File name:", srt_path.name)

    with open(srt_path, "w", encoding="utf8") as f:
        f.write(srt_content)
    txt_dir = video_folder / "txt"
    txt_dir.mkdir(exist_ok=True)
    with open(txt_dir / f'{video_path.stem}.txt', "w", encoding="utf8") as f:
        f.write("\n".join(contents))
