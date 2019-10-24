# File Name  : hex2bin.py
# Author     : Benature
# Create Date: 2019.09.29 周日

# 16进制转2进制
# 计算误码率

import math
import numpy as np

path_r = "../data/normal/receiver_sift.bin"
path_t = "../data/normal/transmitter_sift.bin"

with open(path_r , "rb") as f1:
    receiver = f1.read()
with open(path_t , "rb") as f2:
    transmitter = f2.read()

def hex2bin(sift):
    out = []
    for he in sift:
        bi = "{:0>8}".format(bin(he)[2:])
        bi = np.array(list(bi))
        out.append(bi)
    return out

sift_r = np.array(hex2bin(receiver))
sift_t = np.array(hex2bin(transmitter))

judge = (sift_r == sift_t)

correct = np.sum(judge)
total = judge.shape[0] * judge.shape[1]

print("误码率:", (total - correct) / total)