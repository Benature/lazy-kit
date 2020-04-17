import pandas as pd
from pypinyin import lazy_pinyin as lpy

abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

data = pd.read_csv("xxx.csv")
names = list(set(data["name"]))

name_abbrs, name_encry = [], []
for name in names:
    abbr, encry = "", ""
    for py in lpy(name):
        letter = py[0].title()
        abbr += letter
        encry += abc[(abc.index(letter) + len(name)) % len(abc)]
    name_abbrs.append(abbr)
    name_encry.append(encry)
