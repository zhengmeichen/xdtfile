# coding=utf-8
import h5py
import os
import glob
import datetime
import pickle
import numpy as np
import pandas as pd
import sys

# 输入开始结束时间
S_date = sys.argv[1]
E_date = sys.argv[2]


# 根据开始日期、结束日期返回这段时间里所有天的集合
def getDatesByTimes(sDateStr, eDateStr):
    list = []
    datestart = datetime.datetime.strptime(sDateStr, '%Y%m%d')
    dateend = datetime.datetime.strptime(eDateStr, '%Y%m%d')
    list.append(datestart.strftime('%Y%m%d'))
    while datestart < dateend:
        datestart += datetime.timedelta(days=1)
        list.append(datestart.strftime('%Y%m%d'))
    # 返回['20221001','20221002'....]
    return list


count = 0
time_ls = getDatesByTimes(S_date, E_date)
# print(time_ls)
for date in time_ls:
    filepath = sorted(glob.glob(
        '/STSS/FY3E_STSS/dev/system/stweb/data/machine/FY3E/FY3E_SEM/%s/FY3E_SEM--_ORBT_1A_*_XXOBC_V0.HDF' % (date)))
    # print(filepath, len(filepath))
    for i in filepath:
        print('i', i, i[-26:-12])
        outfilename = i.split('/')[-1].replace(i[-26:-12], '')
        outfilepath = '/STSS/FY3E_STSS/dev/system/stweb/data/machine/FY3E/FY3E_SEM/ERROR_TIME/' + outfilename
        # print(outfilepath)
        # exit()
        if count == 0:
            with h5py.File(i, 'r') as f, h5py.File(outfilepath, 'w') as o:
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
                                o['/' + key + '/' + datasets] = [[t[s], t[e + 1]] for s, e in ranges]
                            else:
                                # 最后单点异常
                                o['/' + key + '/' + datasets] = [[t[s], t[e]] for s, e in ranges]
        else:
            with h5py.File(i, 'r') as f, h5py.File(outfilepath, 'a') as o:
                for key in f.keys():
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
                                if key in o.keys():
                                    if datasets in o['/' + key].keys():
                                        before = o['/' + key + '/' + datasets]
                                        rightnow = [[t[s], t[e + 1]] for s, e in ranges]
                                        all = np.append(before, rightnow, axis=0)
                                        del o['/' + key + '/' + datasets]
                                        o['/' + key + '/' + datasets] = all
                                    else:
                                        o['/' + key + '/' + datasets] = [[t[s], t[e + 1]] for s, e in ranges]
                                else:
                                    o['/' + key + '/' + datasets] = [[t[s], t[e + 1]] for s, e in ranges]
                            else:
                                if key in o.keys():
                                    # 最后单点异常
                                    if datasets in o['/' + key].keys():
                                        before = o['/' + key + '/' + datasets]
                                        rightnow = [[t[s], t[e]] for s, e in ranges]
                                        all = np.append(before, rightnow, axis=0)
                                        del o['/' + key + '/' + datasets]
                                        o['/' + key + '/' + datasets] = all
                                    else:
                                        o['/' + key + '/' + datasets] = [[t[s], t[e]] for s, e in ranges]
                                else:
                                    o['/' + key + '/' + datasets] = [[t[s], t[e]] for s, e in ranges]
        count += 1
