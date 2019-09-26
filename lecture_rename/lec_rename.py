# lec_rename.py
# Date: 2019.09.26
# Author: Benature

import os
import re

root_path = "path/to/the/lecture/folder"
root_path = root_path.replace("\\", "/").rstrip("/") + "/"  # 以防万一最后没加斜杠

filenames = os.listdir(root_path)
for fn in filenames:
    # 只管pptx和pdf
    fn_split = fn.split(".")
    if fn_split[-1] not in ["pptx", "pdf"]:
        continue
    # 防止重复改名
    if len(re.findall(r"\d.p", fn_split[-2])) == 0:
        continue

    # 提取序号
    ind = re.findall(r"\d", fn) 
    ind = ".".join(ind)

    # 跳过无数字的文件
    if len(ind) == 0:
        continue

    new_fn = fn.replace(ind, "")

    # 补全第一章序号
    if len(ind) == 1:
        ind = "1." + ind
   
    # 拼接新文件名
    new_fn = ind + "_" + new_fn

    # 改名
    os.rename(root_path + fn, root_path + new_fn)