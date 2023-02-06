# -*- coding:utf-8 -*-
import h5py
import pickle
import sys
import glob
import numpy as np
import time, datetime

# 阈值范围
outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/YAML/MWTS_A.pkl'
outputfileD = '/STSS/FY3E_STSS/dev/AIWarning/YAML/MWTS_D.pkl'

# 将AD字典读入
pkl_file = open(outputfileA, 'rb')
dicA = pickle.load(pkl_file)
pkl_file = open(outputfileD, 'rb')
dicD = pickle.load(pkl_file)
# print(dicA)
# print('-------------------------------------------------')
# print(dicD)
# exit()

# filename = '/FY3E/MWTS/1A/2022/20220105/FY3E_MWTS-_ORBT_1A_20220105_2125_OBC--_V0.HDF'
# outfilename = '/STSS/FY3E_STSS/dev/AIWarning/Code/HDFTEST/HDF/FY3E_MWTS-_ORBT_1A_20220105_2125_OBC--_V0.HDF'

if __name__ == '__main__':
    date = sys.argv[1]
    # A
    filelistA = sorted(glob.glob(r'/FY3E/MWTS/1A/%s/%s/*.HDF' % (date[0:4], date)))
    for i in filelistA:
        print(i)
        filename = i
        outfilename = '/STSS/FY3E_STSS/dev/AIWarning/HDFTEST/HDF/MWTS/' + i.split('/')[-1]
        with h5py.File(filename, 'r') as f, h5py.File(outfilename, 'w') as o:
            Daycnt = (f['/Geolocation/ScnlinDay'][:].astype('f4') * 24 * 60 * 60 * 1000).astype('i8')
            Mscnt = (f['/Geolocation/ScnlinMillSecond'][:].astype('f4') * 0.1).astype('i8')

            fillvalueD = f['/Geolocation/ScnlinDay'].attrs['FillValue']
            fillvalueM = f['/Geolocation/ScnlinMillSecond'].attrs['FillValue']

            databoolD = Daycnt[:] != fillvalueD
            Daycnt = Daycnt[:][databoolD]

            databoolM = Mscnt[:] != fillvalueM
            Mscnt = Mscnt[:][databoolM]

            tmp = time.mktime(time.strptime("2000-01-01 12:00:00", '%Y-%m-%d %H:%M:%S'))
            realtime = np.zeros((Daycnt.shape), dtype='S40')
            for i in range(Daycnt.shape[0]):
                realtime[i] = datetime.datetime.fromtimestamp((Daycnt[i] + Mscnt[i]) / 1000 + tmp).strftime(
                    '%Y-%m-%d %H:%M:%S')
            o['/Calibration/packagetime'] = realtime

            for i in f['/Calibration'].keys():
                if 'Count' in i or 'Coefficient' in i or 'NEdT' in i or 'QA_Flag_Process' in i:
                    pass
                else:
                    datadim = f['Calibration/' + i].ndim
                    if datadim == 2:
                        if f['Calibration/' + i].shape[0] < f['Calibration/' + i].shape[1]:
                            data = f['Calibration/' + i][:].T[databoolM]
                        else:
                            data = f['Calibration/' + i][:][databoolM]
                    elif datadim == 3:
                        data = f['Calibration/' + i][:].transpose((1, 0, 2))[databoolM]
                    else:
                        data = f['Calibration/' + i][:][databoolM]
                    fillvalue = f['Calibration/' + i].attrs['FillValue']

                    if datadim == 1:
                        QAFlag = np.zeros((len(Daycnt)), dtype='u2')
                        # 阈值名称
                        dicname = f'Calibration_{i}'
                        if dicname in dicD.keys():
                            # 全false
                            # print(dicD[dicDname], type(dicD[dicDname]))
                            # 离散的不在范围内置为1，填充值置为2
                            bool = np.isin(data, dicD[dicname], invert=True)
                            fbool = (data == fillvalue)
                        else:
                            # 连续的不在范围内置为1，填充值置为2
                            bool = ((data < dicA[dicname][0] - 0.1 * dicA[dicname][1]) & (data != fillvalue)) | \
                                   ((data > dicA[dicname][1] + 0.1 * dicA[dicname][1]) & (data != fillvalue))
                            fbool = (data == fillvalue)
                        QAFlag[bool] = 1
                        QAFlag[fbool] = 2

                    elif datadim == 2:
                        QAFlag = np.zeros(data.shape, dtype='u2')
                        for m in range(data.shape[1]):
                            dicname = f'Calibration_{i}_{m}'
                            if dicname in dicD.keys():
                                # 全false
                                # print(dicD[dicDname], type(dicD[dicDname]))
                                # 离散的不在范围内置为1，填充值置为2
                                bool = np.isin(data[:, m], dicD[dicname], invert=True)
                                fbool = (data[:, m] == fillvalue)
                            else:
                                # 连续的不在范围内置为1，填充值置为2
                                bool = ((data[:, m] < dicA[dicname][0] - 0.1 * dicA[dicname][1]) & (
                                        data[:, m] != fillvalue)) | \
                                       ((data[:, m] > dicA[dicname][1] + 0.1 * dicA[dicname][1]) & (
                                               data[:, m] != fillvalue))
                                fbool = (data[:, m] == fillvalue)
                            QAFlag[:, m][bool] = 1
                            QAFlag[:, m][fbool] = 2

                    elif datadim == 3:
                        QAFlag = np.zeros(data.shape, dtype='u2')
                        for m in range(data.shape[1]):
                            for n in range(data.shape[2]):
                                dicname = f'Calibration_{i}_{m}_{n}'
                                if dicname in dicD.keys():
                                    # 全false
                                    # print(dicD[dicDname], type(dicD[dicDname]))
                                    # 离散的不在范围内置为1，填充值置为2
                                    bool = np.isin(data[:, m, n], dicD[dicname], invert=True)
                                    fbool = (data[:, m, n] == fillvalue)
                                else:
                                    # 连续的不在范围内置为1，填充值置为2
                                    bool = ((data[:, m, n] < dicA[dicname][0] - 0.1 * dicA[dicname][1]) & (
                                            data[:, m, n] != fillvalue)) | \
                                           ((data[:, m, n] > dicA[dicname][1] + 0.1 * dicA[dicname][1]) & (
                                                   data[:, m, n] != fillvalue))
                                    fbool = (data[:, m, n] == fillvalue)
                                QAFlag[:, m, n][bool] = 1
                                QAFlag[:, m, n][fbool] = 2

                    o[f'Calibration/QAFlag/{i}'] = QAFlag
                    o[f'Calibration/{i}'] = data
                    # 把属性写进去
                    for k in f[f'/Calibration/{i}'].attrs.keys():
                        o[f'Calibration/{i}'].attrs[k] = f[f'/Calibration/{i}'].attrs[k]

                    name = []
                    if datadim == 2:
                        for m in range(data.shape[1]):
                            name.append(i + str(m))
                        #     每个数据集对应的每一列都存在一个param写进QAflag里面
                        o[f'/Calibration/QAFlag/{i}'].attrs['param'] = name
                    elif datadim == 3:
                        length = data.shape[1] * data.shape[2]
                        for m in range(length):
                            name.append(i + str(m))
                        #     每个数据集对应的每一列都存在一个param写进QAflag里面
                        o[f'/Calibration/QAFlag/{i}'].attrs['param'] = name
                    else:
                        o[f'/Calibration/QAFlag/{i}'].attrs['param'] = i
