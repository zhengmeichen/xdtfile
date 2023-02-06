# coding=utf-8
import h5py
import os
import glob
import datetime
import pickle
import numpy as np
import pandas as pd

# date = sys.argv[1]
date = '20220103'

filepath = sorted(glob.glob(
    '/STSS/FY3E_STSS/dev/system/stweb/data/machine/FY3E/FY3E_SEM/%s/FY3E_SEM--_ORBT_1A_*_XXOBC_V0.HDF' % (date)))
# print(filepath, len(filepath))
for i in filepath:
    print(i)
    outfilename = i.split('/')[-1].replace('XXOBC', 'XXOBCindex')
    outfilepath = '/STSS/FY3E_STSS/dev/system/stweb/data/machine/FY3E/FY3E_SEM/' + date + '/' + outfilename
    # print(outfilepath)
    with h5py.File(i, 'r') as f, h5py.File(outfilepath, 'a') as o:
        for key in f.keys():
            # print(key)
            for datasets in f['/' + key + '/QA'].keys():
                # print(datasets)
                index, = np.where(f['/' + key + '/QA/' + datasets][:] != 0)
                # print(index)
                t = f['/' + key + '/Time/timestamp'][...]
                # 正常数据集
                if index.size == 0:
                    continue
                    # pass
                # 存在异常的数据集
                else:
                    # 插值判断是否连续
                    ls = np.diff(index)
                    ss, = np.where(ls > 1)
                    ss += 1

                    # 分段处理
                    ranges = []
                    start = 0
                    print(key, datasets, ss)
                    # 单点异常和连续异常
                    for end in ss:
                        print(index[start:end])
                        ranges.append(index[start:end][(0, -1),])
                        start = end

                    print(index[start:])
                    # 连续异常
                    ranges.append(index[start:][(0, -1),])
                    print(len(ranges))
                    print(key, datasets, 'RANGES:', ranges)

                    print(datasets, f['/' + key + '/QA/' + datasets].shape[0])
                    # 中间异常
                    if ranges[-1][0] + 1 != f['/' + key + '/QA/' + datasets].shape[0]:
                        o['/' + key + '/' + datasets] = [[t[s], s, t[e + 1], e + 1] for s, e in ranges]
                    else:
                        # 最后单点异常
                        o['/' + key + '/' + datasets] = [[t[s], s, t[e], e] for s, e in ranges]
