# -*- coding:utf-8 -*-
import datetime
import glob
import math
import os
import sys
import time

import h5py
import numpy as np
import pandas as pd

from netCDF4 import Dataset
from numpy import *
from numpy import NaN


# 读取hdf文件
def read_save(ls1, ls2, date, kind):
    
    with h5py.File(ls1, 'r') as f:
        # 读取Z数据
        ds_z = f['z'][()]
        print('z', ds_z.shape)

        # 读取ref_zef数据
        ds_r = f['ref_zef'][()]
        print('ref_zef', ds_r.shape)

        # 读取lat数据
        ds_lat = f['lat'][()]

        # 读取lon数据
        ds_lon = f['lon'][()]

    # print data_lon.shape, data_lat.shape
    # 读取每个文件的数据
    with h5py.File(ls2, 'r') as f:
        # 读取height数据
        ds_h = f['/FS/PRE/height'][()]
        print('height', ds_h.shape)

        # 新建三维空数组
        data_all = np.zeros(ds_h.shape)

        # 读取height数据
        ds_zf = f['/FS/PRE/zFactorMeasured'][:, :, :, 0]
        print(ds_zf.shape)

        # z与height数据进行做差，找出最小值
        for i in range(ds_h.shape[0]):
            for j in range(ds_h.shape[1]):

                # zlist就是37层的数据
                zlist = list(dic_z[str(i) + '_' + str(j)])

                # hlist就是176层的数据
                hlist = list(dic_h[str(i) + '_' + str(j)])

                # clist是37层的refzef数据
                clist = list(ds_r[i, j, :])

                # 相同x,y下,对z轴,两数组做差
                # zlist--37,hlist--176
                # 对比做差
                for x in range(len(zlist)):
                    # print zlist.index(a)
                    result = list(abs(zlist[x] - hlist))
                    # print result, len(result)
                    # index位置即为176对应的最接近z单一数据的位置，也是ref去取出后要填入的位置
                    height = result.index(min(result))
                    # 写入新建的数据集
                    data_all[i, j, height] = clist[x]

    # 三维数组保存为hdf文件
    with h5py.File(
            "/STSS/FY3E_STSS/Simulator/GPM_DRP/output/ERA5/20210720/match/GPM_DRP_KU_L2_" + date + '_' + kind + "_ref.hdf5",
            'w') as f:  # 写入的时候是‘w’
        print('alreaady write')
        f.create_dataset("sub_data", data=data_all, compression=9)
        f.create_dataset("lat", data=ds_lat, compression=9)
        f.create_dataset("lon", data=ds_lon, compression=9)
        f.create_dataset("zFactorMeasured", data=ds_zf, compression=9)
    return


if __name__ == '__main__':
    # 输入时间,时次
    date = sys.argv[1]
    kind = sys.argv[2]
    # 查找数据文件
    ls1 = sorted(
        glob.glob(
            r'/STSS/FY3E_STSS/Simulator/GPM_DRP/output/ERA5/%s/new1/GPM_DRP_KU_L2_%s_%s_ref.h5' % (date, date, kind)))
    # ls2 = sorted(glob.glob(r'/NWPDATA/FY3FG/GPM_DPR/L2/%s/2A.GPM.DPR.*.V07A.HDF5' % (date)))
    ls2 = sorted(
        glob.glob(r'/NWPDATA/FY3FG/GPM_DPR/L2/%s/2A.GPM.DPR.V9-20211125.20210720-S%s*-*.*.V07A.HDF5' % (date, kind)))
    print(ls1, ls2)
    # 数据读取，做差,并将数据保存为hdf格式
    read_save(ls1[0], ls2[0], date, kind)
