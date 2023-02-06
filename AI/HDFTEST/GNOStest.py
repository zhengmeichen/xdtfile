# -*- coding:utf-8 -*-
import h5py
import pickle
import sys
import glob
import numpy as np
import time, datetime

# 阈值范围
outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/YAML/GNOS_A.pkl'
outputfileD = '/STSS/FY3E_STSS/dev/AIWarning/YAML/GNOS_D.pkl'
# 将AD字典读入
pkl_file = open(outputfileA, 'rb')
dicA = pickle.load(pkl_file)
pkl_file = open(outputfileD, 'rb')
dicD = pickle.load(pkl_file)
# print(dicA)
# print('-------------------------------------------------')
# print(dicD)
# exit()


# filename = 'C:\\Users\\zhengmeichen\\Downloads\\FY3E_GNOS-_ORBT_1A_20220102_0008_OBC--_V0.HDF'
# outfilename = 'C:\\Users\\zhengmeichen\\Downloads\\FY3E_GNOS-_ORBT_1A_20220102_OBC--_V0.HDF'


if __name__ == '__main__':
    # 输入时间,时次
    date = sys.argv[1]
    filelist = sorted(glob.glob(r'/FY3E/GNOS/1A/OBC/%s/%s/*.HDF' % (date[0:4], date)))
    for i in filelist:
        print(i)
        filename = i
        outfilename = '/STSS/FY3E_STSS/dev/AIWarning/HDFTEST/HDF/GNOS/' + i.split('/')[-1]
        print(outfilename)
        with h5py.File(filename, 'r') as f, h5py.File(outfilename, 'w') as o:
            # PlatformTele时间
            DaycntA = (f['/PlatformTele/Day_Count_Tel'][:].astype('f4') * 24 * 60 * 60 * 1000).astype('i8')
            MscntA = f['/PlatformTele/Msec_Count_Tel'][:].astype('i8')

            fillvalueDA = f['/PlatformTele/Day_Count_Tel'].attrs['FillValue']
            fillvalueMA = f['/PlatformTele/Msec_Count_Tel'].attrs['FillValue']

            databoolDA = DaycntA[:] != fillvalueDA
            DaycntA = DaycntA[:][databoolDA]

            databoolMA = MscntA[:] != fillvalueMA
            MscntA = MscntA[:][databoolMA]

            tmp = time.mktime(time.strptime("2000-01-01 12:00:00", '%Y-%m-%d %H:%M:%S'))
            realtimeA = np.zeros((DaycntA.shape), dtype='S40')
            for i in range(DaycntA.shape[0]):
                realtimeA[i] = datetime.datetime.fromtimestamp((DaycntA[i] + MscntA[i]) / 1000.0 + tmp).strftime(
                    '%Y-%m-%d %H:%M:%S')

            o['/PlatformTele/packagetime'] = realtimeA
            # RoTele和RfTele
            DaycntB = (f['/RoTele/Day_Count'][:].astype('f4') * 24 * 60 * 60 * 1000).astype('i8')
            MscntB = f['/RoTele/Msec_Count'][:].astype('i8')

            fillvalueDB = f['/RoTele/Day_Count'].attrs['FillValue']
            fillvalueMB = f['/RoTele/Msec_Count'].attrs['FillValue']

            databoolDB = DaycntB[:] != fillvalueDB
            DaycntB = DaycntB[:][databoolDB]

            databoolMB = MscntB[:] != fillvalueMB
            MscntB = MscntB[:][databoolMB]

            tmp = time.mktime(time.strptime("2000-01-01 12:00:00", '%Y-%m-%d %H:%M:%S'))
            realtimeB = np.zeros((DaycntB.shape), dtype='S40')
            for i in range(DaycntB.shape[0]):
                realtimeB[i] = datetime.datetime.fromtimestamp((DaycntB[i] + MscntB[i]) / 1000 + tmp).strftime(
                    '%Y-%m-%d %H:%M:%S')
            o['/RfTele/packagetime'] = realtimeB
            o['/RoTele/packagetime'] = realtimeB

            for i in f['/PlatformTele'].keys():
                datadim = f['PlatformTele/' + i].ndim
                data = f['PlatformTele/' + i][:][databoolMA]
                fillvalue = f['PlatformTele/' + i].attrs['FillValue']
                if 'Count' not in i:
                    if datadim == 1:
                        # print(len(DaycntA))
                        QAFlag = np.zeros((len(DaycntA)), dtype='u2')
                        # print(QAFlag.shape)
                        # 阈值名称
                        dicname = f'PlatformTele_{i}'
                        if dicname in dicD.keys():
                            # 全false
                            # print(dicD[dicDname], type(dicD[dicDname]))
                            # 离散的不在范围内置为1，填充值置为2
                            bool = np.isin(data, dicD[dicname], invert=True)
                            fbool = (data == fillvalue)
                            sbool = (data == 255)
                        else:
                            # 连续的不在范围内置为1，填充值置为2
                            bool = ((data < dicA[dicname][0] - 0.05 * dicA[dicname][1]) & (data != fillvalue)) | \
                                   ((data > dicA[dicname][1] + 0.05 * dicA[dicname][1]) & (data != fillvalue))
                            fbool = (data == fillvalue)
                        QAFlag[bool] = 1
                        QAFlag[fbool] = 2
                        QAFlag[sbool] = 2

                    elif datadim == 2:
                        QAFlag = np.zeros(data.shape, dtype='u2')
                        for m in range(data.shape[1]):
                            dicname = f'PlatformTele_{i}_{m}'
                            if dicname in dicD.keys():
                                # 全false
                                # print(dicD[dicDname], type(dicD[dicDname]))
                                # 离散的不在范围内置为1，填充值置为2
                                bool = np.isin(data[:, m], dicD[dicname], invert=True)
                                fbool = (data[:, m] == fillvalue)
                            else:
                                # 连续的不在范围内置为1，填充值置为2
                                bool = ((data[:, m] < dicA[dicname][0] - 0.05 * dicA[dicname][1]) & (
                                        data[:, m] != fillvalue)) | \
                                       ((data[:, m] > dicA[dicname][1] + 0.05 * dicA[dicname][1]) & (
                                               data[:, m] != fillvalue))
                                fbool = (data[:, m] == fillvalue)
                            QAFlag[:, m][bool] = 1
                            QAFlag[:, m][fbool] = 2

                    o[f'PlatformTele/QAFlag/{i}'] = QAFlag
                    o[f'PlatformTele/{i}'] = data
                    # 把属性写进去
                    for k in f['/PlatformTele/' + i].attrs.keys():
                        o[f'PlatformTele/{i}'].attrs[k] = f['/PlatformTele/' + i].attrs[k]

                    name = []
                    if datadim == 2:
                        for m in range(data.shape[1]):
                            name.append(i + str(m))
                        #     每个数据集对应的每一列都存在一个param写进QAflag里面
                        o['/PlatformTele/QAFlag/' + i].attrs['param'] = name
                    else:
                        o['/PlatformTele/QAFlag/' + i].attrs['param'] = i
                else:
                    continue

            for i in f['/RfTele'].keys():
                datadim = f['RfTele/' + i].ndim
                data = f['RfTele/' + i][:][databoolMB]
                fillvalue = f['RfTele/' + i].attrs['FillValue']
                if datadim == 1:
                    QAFlag = np.zeros((len(DaycntB)), dtype='u2')
                    # 阈值名称
                    dicname = f'RfTele_{i}'
                    if dicname in dicD.keys():
                        # 全false
                        # print(dicD[dicDname], type(dicD[dicDname]))
                        # 离散的不在范围内置为1，填充值置为2
                        bool = np.isin(data, dicD[dicname], invert=True)
                        fbool = (data == fillvalue)
                    else:
                        # 连续的不在范围内置为1，填充值置为2
                        bool = ((data < dicA[dicname][0] - 0.05 * dicA[dicname][1]) & (data != fillvalue)) | \
                               ((data > dicA[dicname][1] + 0.05 * dicA[dicname][1]) & (data != fillvalue))
                        fbool = (data == fillvalue)
                    QAFlag[bool] = 1
                    QAFlag[fbool] = 2

                elif datadim == 2:
                    QAFlag = np.zeros(data.shape, dtype='u2')
                    for m in range(data.shape[1]):
                        dicname = f'RfTele_{i}_{m}'
                        if dicname in dicD.keys():
                            # 全false
                            # print(dicD[dicDname], type(dicD[dicDname]))
                            # 离散的不在范围内置为1，填充值置为2
                            bool = np.isin(data[:, m], dicD[dicname], invert=True)
                            fbool = (data[:, m] == fillvalue)
                        else:
                            # 连续的不在范围内置为1，填充值置为2
                            bool = ((data[:, m] < dicA[dicname][0] - 0.05 * dicA[dicname][1]) & (
                                    data[:, m] != fillvalue)) | \
                                   ((data[:, m] > dicA[dicname][1] + 0.05 * dicA[dicname][1]) & (
                                           data[:, m] != fillvalue))
                            fbool = (data[:, m] == fillvalue)
                        QAFlag[:, m][bool] = 1
                        QAFlag[:, m][fbool] = 2

                o[f'RfTele/QAFlag/{i}'] = QAFlag
                o[f'RfTele/{i}'] = data
                # 把属性写进去
                for k in f['/RfTele/' + i].attrs.keys():
                    o[f'RfTele/{i}'].attrs[k] = f['/RfTele/' + i].attrs[k]

                name = []
                if datadim == 2:
                    for m in range(data.shape[1]):
                        name.append(i + str(m))
                    #     每个数据集对应的每一列都存在一个param写进QAflag里面
                    o['/RfTele/QAFlag/' + i].attrs['param'] = name
                else:
                    o['/RfTele/QAFlag/' + i].attrs['param'] = i

            # 数据集3
            for i in f['/RoTele'].keys():
                if 'Count' in i:
                    pass
                else:
                    datadim = f['RoTele/' + i].ndim
                    data = f['RoTele/' + i][:][databoolMB]
                    fillvalue = f['RoTele/' + i].attrs['FillValue']
                    if datadim == 1:
                        QAFlag = np.zeros((len(DaycntB)), dtype='u2')
                        # 阈值名称
                        dicname = f'RoTele_{i}'
                        if dicname in dicD.keys():
                            # 全false
                            # print(dicD[dicDname], type(dicD[dicDname]))
                            # 离散的不在范围内置为1，填充值置为2
                            bool = np.isin(data, dicD[dicname], invert=True)
                            fbool = (data == fillvalue)
                        else:
                            # 连续的不在范围内置为1，填充值置为2
                            bool = ((data < dicA[dicname][0] - 0.05 * dicA[dicname][1]) & (data != fillvalue)) | \
                                   ((data > dicA[dicname][1] + 0.05 * dicA[dicname][1]) & (data != fillvalue))
                            fbool = (data == fillvalue)
                        QAFlag[bool] = 1
                        QAFlag[fbool] = 2


                    elif datadim == 2:
                        QAFlag = np.zeros((len(DaycntB), data.shape[1]), dtype='u2')
                        for m in range(data.shape[1]):
                            dicname = f'RoTele_{i}_{m}'
                            if dicname in dicD.keys():
                                # 全false
                                # print(dicD[dicDname], type(dicD[dicDname]))
                                # 离散的不在范围内置为1，填充值置为2
                                bool = np.isin(data[:, m], dicD[dicname], invert=True)
                                fbool = (data[:, m] == fillvalue)
                            else:
                                # 连续的不在范围内置为1，填充值置为2
                                bool = ((data[:, m] < dicA[dicname][0] - 0.05 * dicA[dicname][1]) & (
                                        data[:, m] != fillvalue)) | \
                                       ((data[:, m] > dicA[dicname][1] + 0.05 * dicA[dicname][1]) & (
                                               data[:, m] != fillvalue))
                                fbool = (data[:, m] == fillvalue)
                            QAFlag[:, m][bool] = 1
                            QAFlag[:, m][fbool] = 2

                    o[f'RoTele/QAFlag/{i}'] = QAFlag
                    o[f'RoTele/{i}'] = data
                    # 把属性写进去
                    for k in f['/RoTele/' + i].attrs.keys():
                        o[f'RoTele/{i}'].attrs[k] = f['/RoTele/' + i].attrs[k]

                    name = []
                    if datadim == 2:
                        for m in range(data.shape[1]):
                            name.append(i + str(m))
                        #     每个数据集对应的每一列都存在一个param写进QAflag里面
                        o['/RoTele/QAFlag/' + i].attrs['param'] = name
                    else:
                        o['/RoTele/QAFlag/' + i].attrs['param'] = i
