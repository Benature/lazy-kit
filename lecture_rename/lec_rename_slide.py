# lec_rename_slide.py
# Date: 2019.11.25
# Author: Benature

'''
提取`filt`字符串到最前->分类
'''

import os

filt = "_slides"

root_path = "path/to/the/lecture/folder"
root_path = root_path.replace("\\", "/").rstrip("/") + "/"  # 以防万一最后没加斜杠

filenames = os.listdir(root_path)

for fn in filenames:
    if filt not in fn:
        continue
    new_fn = filt.strip("_") + "_" + fn.replace(filt, "")
    # print(new_fn)
    os.rename(root_path+fn, root_path+new_fn)
