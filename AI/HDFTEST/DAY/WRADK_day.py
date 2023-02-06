# -*- coding:utf-8 -*-
import h5py
import pickle
import glob
import os
import sys
import numpy as np
import time, datetime

# 文件读取
filelist1 = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/HDFTEST/HDF/WRADK/ASCENDKu/*.HDF'))
filelist2 = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/HDFTEST/HDF/WRADK/DESCENDKu/*.HDF'))


shijian1 = int(filelist1[0].split('/')[-1][-17:-13])
shijian2 = int(filelist2[0].split('/')[-1][-17:-13])
# print(shijian1, shijian2,type(shijian2))
filelist = []
if shijian1 < shijian2:
    for x in range(len(filelist1)):
        filelist.append(filelist1[x])
        filelist.append(filelist2[x])
else:
    for x in range(len(filelist1)):
        filelist.append(filelist2[x])
        filelist.append(filelist1[x])
# print(filelist)
# exit()
# 文件保存名称
# FY3E_GNOS-_ORBT_1A_20220105_OBC--_V0.HDF
filename = (filelist[0].split('/')[-1][:27] + filelist[0].split('/')[-1][32:])
# print(filename)
# 20220105
date = (filelist[0].split('/')[-1][-26:-18])
# print(date)
# exit()
# 文件输出路径
try:
    os.mkdir('/STSS/FY3E_STSS/dev/system/stweb/data/machine/FY3E/FY3E_WindRadK/' + date)
except:
    pass

inputs = [h5py.File(filelist[i], 'r') for i in range(len(filelist))]

# sds返回hdf所有数据集名称
sds = []


def nn(name, obj):
    if isinstance(obj, h5py.Dataset):
        sds.append(name)


inputs[0].visititems(nn)
c = len(sds)
# print(sds)
# print('files:', len(inputs))
# print("filename:", filename)

outfile = '/STSS/FY3E_STSS/dev/system/stweb/data/machine/FY3E/FY3E_WindRadK/' + date + "/" + filename
print(outfile, type(outfile))
with h5py.File(outfile, 'w') as o:
    for i, s in enumerate(sds):
        print('merge[%d/%d]: %s' % (i, c, s))
        # 合并保持列不变，行追加
        o[s] = np.concatenate([p[s] for p in inputs], axis=0)
