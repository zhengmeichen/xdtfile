# coding=utf-8
import h5py
import os
import glob
import datetime
import pickle
import numpy as np
import pandas as pd
import sys
date = sys.argv[1]
# date = '20220103'

filepath = sorted(glob.glob('/STSS/FY3E_STSS/dev/system/stweb/data/machine/FY3E/FY3E_SEM/%s/*.HDF' % (date)))

group_f = [filepath[i:i + 5] for i in range(0, len(filepath), 5)]
for i in group_f:
    # 同时次文件
    for j in i:
        file_name = j.split('/')[-1]
        filename = file_name.replace(file_name[-12:-7], 'XXOBC')
        outfilepath = '/STSS/FY3E_STSS/dev/system/stweb/data/machine/FY3E/FY3E_SEM/' + date + '/' + filename
        print(outfilepath)
        if not os.path.exists(outfilepath):
            with h5py.File(j, 'r') as f, h5py.File(outfilepath, 'w') as o:
                for key in f.keys():
                    print("key",key)
                    for group in f['/' + key].keys():
                        for datasets in f['/' + key + '/' + group].keys():
                            o['/' + key + '/' + group + '/' + datasets] = f['/' + key + '/' + group + '/' + datasets][:]
        else:
            with h5py.File(j, 'r') as f, h5py.File(outfilepath, 'a') as o:
                for key in f.keys():
                    for group in f['/' + key].keys():
                        for datasets in f['/' + key + '/' + group].keys():
                            o['/' + key + '/' + group + '/' + datasets] = f['/' + key + '/' + group + '/' + datasets][:]
