# -*- coding:utf-8 -*-
import h5py
import numpy as np
import time, datetime


def get_0_1_array(array, rate=0.2):
    '''按照数组模板生成对应的 0-1 矩阵，默认rate=0.2'''
    zeros_num = int(array.size * rate)  # 根据0的比率来得到 0的个数
    new_array = np.ones(array.size,dtype=int)  # 生成与原来模板相同的矩阵，全为1
    new_array[:zeros_num] = 0  # 将一部分换为0
    new_array[:int(zeros_num / 2)] = 2  # 将一部分换为2
    np.random.shuffle(new_array)  # 将0和1的顺序打乱
    re_array = new_array.reshape(array.shape)  # 重新定义矩阵的维度，与模板相同
    return re_array


# filename = '/FY3E/MWHS/1A/DESCEND/2022/20220218/FY3E_MWHS-_ORBD_1A_20220218_0331_OBC--_V0.HDF'
# outfilename = '/STSS/FY3E_STSS/dev/AIWarning/Code/SelTxt/data/FY3E_MWHS-_ORBD_1A_20220218_BC--_V0.HDF'
filename = 'C:\\Users\\zhengmeichen\\Downloads\\FY3E_SSIM-_SOLR_1A_20220104_2007_OBCSL_V0.HDF'
outfilename = 'C:\\Users\\zhengmeichen\\Downloads\\FY3E_SSIM-_SOLR_1A_20220104_OBCSL_V0.HDF'

with h5py.File(filename, 'r') as f, h5py.File(outfilename, 'w') as o:
    count = 0
    for i in f['/Calibration'].keys():
        if 'Raw_DN_Data' in i or 'Coefficient' in i or 'NEdT' in i or 'SPBB' in i:
            pass
        else:
            o['/Calibration/' + i] = f['/Calibration/' + i][:]
            # 一维数据
            if o['/Calibration/' + i].ndim == 1:
                count = count + 1
            #     二维数据
            elif o['/Calibration/' + i].ndim == 2:
                count = count + f['/Calibration/' + i][:].shape[1]
            #     三维数据
            elif o['/Calibration/' + i].ndim == 3:
                count = count + f['/Calibration/' + i][:].shape[1] * f['/Calibration/' + i][:].shape[2]
            else:
                continue

    # packgetime时间
    Daycnt = f['/Geolocation/Day_Count'][:].astype('f4') * 24 * 60 * 60 * 1000
    Mscnt = f['/Geolocation/Millisecond_Count'][:].astype('f4')
    tmp = time.mktime(time.strptime("2000-01-01 12:00:00", '%Y-%m-%d %H:%M:%S'))
    realtime = np.zeros((Daycnt.shape), dtype='S40')
    for i in range(Daycnt.shape[0]):
        realtime[i] = datetime.datetime.fromtimestamp((Daycnt[i] + Mscnt[i]) / 1000 + tmp).strftime('%Y-%m-%d %H:%M:%S')
    o['/Calibration/packagetime'] = realtime

    arr1 = np.zeros((Daycnt.shape[0], count), dtype='u2')
    QA = get_0_1_array(arr1, rate=0.7)
    o['/Calibration/QAFlag'] = QA
    o['/Calibration/QAFlag'].attrs[
        'param'] = 'Gain,Raw_DN_Data,Inst_Temp,Space_View,NEdTWarm,Cal_Coefficient,Black_Body_View,Pixel_View_Angle,PRT_Tavg'
