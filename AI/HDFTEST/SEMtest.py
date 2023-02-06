# -*- coding:utf-8 -*-
import h5py
import pickle
import numpy as np
import time, datetime

# 阈值范围
outputfileA1 = '/STSS/FY3E_STSS/dev/AIWarning/YAML/SEM_HP_A.pkl'
outputfileD1 = '/STSS/FY3E_STSS/dev/AIWarning/YAML/SEM_HP_D.pkl'
outputfileA2 = '/STSS/FY3E_STSS/dev/AIWarning/YAML/SEM_ME_A.pkl'
outputfileD2 = '/STSS/FY3E_STSS/dev/AIWarning/YAML/SEM_ME_D.pkl'
outputfileA3 = '/STSS/FY3E_STSS/dev/AIWarning/YAML/SEM_MF_A.pkl'
outputfileD3 = '/STSS/FY3E_STSS/dev/AIWarning/YAML/SEM_MF_D.pkl'
outputfileA4 = '/STSS/FY3E_STSS/dev/AIWarning/YAML/SEM_MP_A.pkl'
outputfileD4 = '/STSS/FY3E_STSS/dev/AIWarning/YAML/SEM_MP_D.pkl'
outputfileA5 = '/STSS/FY3E_STSS/dev/AIWarning/YAML/SEM_SP_A.pkl'
outputfileD5 = '/STSS/FY3E_STSS/dev/AIWarning/YAML/SEM_SP_D.pkl'

# outputfileA1 = 'C:\\Users\\19683\\Downloads\\SEM_HP_A.pkl'
# outputfileD1 = 'C:\\Users\\19683\\Downloads\\SEM_HP_D.pkl'
# outputfileA2 = 'C:\\Users\\19683\\Downloads\\SEM_ME_A.pkl'
# outputfileD2 = 'C:\\Users\\19683\\Downloads\\SEM_ME_D.pkl'
# outputfileA3 = 'C:\\Users\\19683\\Downloads\\SEM_MF_A.pkl'
# outputfileD3 = 'C:\\Users\\19683\\Downloads\\SEM_MF_D.pkl'
# outputfileA4 = 'C:\\Users\\19683\\Downloads\\SEM_MP_A.pkl'
# outputfileD4 = 'C:\\Users\\19683\\Downloads\\SEM_MP_D.pkl'
# outputfileA5 = 'C:\\Users\\19683\\Downloads\\SEM_SP_A.pkl'
# outputfileD5 = 'C:\\Users\\19683\\Downloads\\SEM_SP_D.pkl'

# 将AD字典读入
pkl_file = open(outputfileA1, 'rb')
dicA1 = pickle.load(pkl_file, encoding='iso-8859-1')
pkl_file = open(outputfileD1, 'rb')
dicD1 = pickle.load(pkl_file, encoding='iso-8859-1')
pkl_file = open(outputfileA2, 'rb')
dicA2 = pickle.load(pkl_file, encoding='iso-8859-1')
pkl_file = open(outputfileD2, 'rb')
dicD2 = pickle.load(pkl_file, encoding='iso-8859-1')
pkl_file = open(outputfileA3, 'rb')
dicA3 = pickle.load(pkl_file, encoding='iso-8859-1')
pkl_file = open(outputfileD3, 'rb')
dicD3 = pickle.load(pkl_file, encoding='iso-8859-1')
pkl_file = open(outputfileA4, 'rb')
dicA4 = pickle.load(pkl_file, encoding='iso-8859-1')
pkl_file = open(outputfileD4, 'rb')
dicD4 = pickle.load(pkl_file, encoding='iso-8859-1')
pkl_file = open(outputfileA5, 'rb')
dicA5 = pickle.load(pkl_file, encoding='iso-8859-1')
pkl_file = open(outputfileD5, 'rb')
dicD5 = pickle.load(pkl_file, encoding='iso-8859-1')
# print(dicA4)
# print('-------------------------------------------------')
# print(dicD4)
# exit()


filename1 = '/FY3E/SEM/1A/HPOBC/%Y/%Y%m%d/FY3E_SEM--_ORBT_1A_%Y%m%d_%H%M_HPOBC_V0.HDF'
filename2 = '/FY3E/SEM/1A/MEOBC/%Y/%Y%m%d/FY3E_SEM--_ORBT_1A_%Y%m%d_%H%M_MEOBC_V0.HDF'
filename3 = '/FY3E/SEM/1A/MFOBC/%Y/%Y%m%d/FY3E_SEM--_ORBT_1A_%Y%m%d_%H%M_MFOBC_V0.HDF'
filename4 = '/FY3E/SEM/1A/MPOBC/%Y/%Y%m%d/FY3E_SEM--_ORBT_1A_%Y%m%d_%H%M_MPOBC_V0.HDF'
filename5 = '/FY3E/SEM/1A/SPOBC/%Y/%Y%m%d/FY3E_SEM--_ORBT_1A_%Y%m%d_%H%M_SPOBC_V0.HDF'
outfilename = '/STSS/FY3E_STSS/dev/AIWarning/HDFTEST/HDF/SEM/FY3E_SEM--_ORBT_1A_%Y%m%d_%H%M_OBC_V0.HDF'


def xx(filename):
    fb = os.path.basename(filename)[:-12]
    t = datetime.datetime.strptime(fb, 'FY3E_SEM--_ORBT_1A_%Y%m%d_%H%M_')
    tf = t.strftime

    with h5py.File(tf(filename1), 'r') as f1, h5py.File(tf(filename2), 'r') as f2, h5py.File(tf(filename3), 'r') as f3, \
            h5py.File(tf(filename4), 'r') as f4, h5py.File(tf(filename5), 'r') as f5, h5py.File(tf(outfilename),
                                                                                                'w') as o:
        # 时间
        Year1 = f1['/Time/Year'][:].astype('i4')
        Month1 = f1['/Time/Month'][:].astype('i4')
        Date1 = f1['/Time/Date'][:].astype('i4')
        Hour1 = f1['/Time/Hour'][:].astype('i4')
        Minute1 = f1['/Time/Minute'][:].astype('i4')
        Second1 = f1['/Time/Second'][:].astype('i4')

        boolYear1 = f1['/Time/Year'].attrs['FillValue']
        boolMonth1 = f1['/Time/Month'].attrs['FillValue']
        boolDate1 = f1['/Time/Date'].attrs['FillValue']
        boolHour1 = f1['/Time/Hour'].attrs['FillValue']
        boolMinute1 = f1['/Time/Minute'].attrs['FillValue']
        boolSecond1 = f1['/Time/Second'].attrs['FillValue']

        databoolYear1 = Year1[:] != boolYear1
        Year1 = Year1[:][databoolYear1]
        databoolMonth1 = Month1[:] != boolMonth1
        Month1 = Month1[:][databoolMonth1]
        databoolDate1 = Date1[:] != boolDate1
        Date1 = Date1[:][databoolDate1]
        databoolHour1 = Hour1[:] != boolHour1
        Hour1 = Hour1[:][databoolHour1]
        databoolMinute1 = Minute1[:] != boolMinute1
        Minute1 = Minute1[:][databoolMinute1]
        databoolSecond1 = Second1[:] != boolSecond1
        Second1 = Second1[:][databoolSecond1]

        realtime1 = np.zeros((Year1.shape), dtype='S40')
        for i in range(Year1.shape[0]):
            realtime1[i] = datetime.datetime(Year1[i], Month1[i], Date1[i], Hour1[i], Minute1[i], Second1[i])
        o['/HPOBC/packagetime'] = realtime1

        Year2 = f2['/Time/Year'][:].astype('i4')
        Month2 = f2['/Time/Month'][:].astype('i4')
        Date2 = f2['/Time/Date'][:].astype('i4')
        Hour2 = f2['/Time/Hour'][:].astype('i4')
        Minute2 = f2['/Time/Minute'][:].astype('i4')
        Second2 = f2['/Time/Second'][:].astype('i4')

        boolYear2 = f2['/Time/Year'].attrs['FillValue']
        boolMonth2 = f2['/Time/Month'].attrs['FillValue']
        boolDate2 = f2['/Time/Date'].attrs['FillValue']
        boolHour2 = f2['/Time/Hour'].attrs['FillValue']
        boolMinute2 = f2['/Time/Minute'].attrs['FillValue']
        boolSecond2 = f2['/Time/Second'].attrs['FillValue']

        databoolYear2 = Year2[:] != boolYear2
        Year2 = Year2[:][databoolYear2]
        databoolMonth2 = Month2[:] != boolMonth2
        Month2 = Month2[:][databoolMonth2]
        databoolDate2 = Date2[:] != boolDate2
        Date2 = Date2[:][databoolDate2]
        databoolHour2 = Hour2[:] != boolHour2
        Hour2 = Hour2[:][databoolHour2]
        databoolMinute2 = Minute2[:] != boolMinute2
        Minute2 = Minute2[:][databoolMinute2]
        databoolSecond2 = Second2[:] != boolSecond2
        Second2 = Second2[:][databoolSecond2]

        realtime2 = np.zeros((Year2.shape), dtype='S40')
        for i in range(Year2.shape[0]):
            realtime2[i] = datetime.datetime(Year2[i], Month2[i], Date2[i], Hour2[i], Minute2[i], Second2[i])
        o['/MEOBC/packagetime'] = realtime2

        Year3 = f3['/Time/Year'][:].astype('i4')
        Month3 = f3['/Time/Month'][:].astype('i4')
        Date3 = f3['/Time/Date'][:].astype('i4')
        Hour3 = f3['/Time/Hour'][:].astype('i4')
        Minute3 = f3['/Time/Minute'][:].astype('i4')
        Second3 = f3['/Time/Second'][:].astype('i4')

        boolYear3 = f3['/Time/Year'].attrs['FillValue']
        boolMonth3 = f3['/Time/Month'].attrs['FillValue']
        boolDate3 = f3['/Time/Date'].attrs['FillValue']
        boolHour3 = f3['/Time/Hour'].attrs['FillValue']
        boolMinute3 = f3['/Time/Minute'].attrs['FillValue']
        boolSecond3 = f3['/Time/Second'].attrs['FillValue']

        databoolYear3 = Year3[:] != boolYear3
        Year3 = Year3[:][databoolYear3]
        databoolMonth3 = Month3[:] != boolMonth3
        Month3 = Month3[:][databoolMonth3]
        databoolDate3 = Date3[:] != boolDate3
        Date3 = Date3[:][databoolDate3]
        databoolHour3 = Hour3[:] != boolHour3
        Hour3 = Hour3[:][databoolHour3]
        databoolMinute3 = Minute3[:] != boolMinute3
        Minute3 = Minute3[:][databoolMinute3]
        databoolSecond3 = Second3[:] != boolSecond3
        Second3 = Second3[:][databoolSecond3]

        realtime3 = np.zeros((Year3.shape), dtype='S40')
        for i in range(Year3.shape[0]):
            realtime3[i] = datetime.datetime(Year3[i], Month3[i], Date3[i], Hour3[i], Minute3[i], Second3[i])
        o['/MFOBC/packagetime'] = realtime3

        Year4 = f4['/Time/Year'][:].astype('i4')
        Month4 = f4['/Time/Month'][:].astype('i4')
        Date4 = f4['/Time/Date'][:].astype('i4')
        Hour4 = f4['/Time/Hour'][:].astype('i4')
        Minute4 = f4['/Time/Minute'][:].astype('i4')
        Second4 = f4['/Time/Second'][:].astype('i4')

        boolYear4 = f4['/Time/Year'].attrs['FillValue']
        boolMonth4 = f4['/Time/Month'].attrs['FillValue']
        boolDate4 = f4['/Time/Date'].attrs['FillValue']
        boolHour4 = f4['/Time/Hour'].attrs['FillValue']
        boolMinute4 = f4['/Time/Minute'].attrs['FillValue']
        boolSecond4 = f4['/Time/Second'].attrs['FillValue']

        databoolYear4 = Year4[:] != boolYear4
        Year4 = Year4[:][databoolYear4]
        databoolMonth4 = Month4[:] != boolMonth4
        Month4 = Month4[:][databoolMonth4]
        databoolDate4 = Date4[:] != boolDate4
        Date4 = Date4[:][databoolDate4]
        databoolHour4 = Hour4[:] != boolHour4
        Hour4 = Hour4[:][databoolHour4]
        databoolMinute4 = Minute4[:] != boolMinute4
        Minute4 = Minute4[:][databoolMinute4]
        databoolSecond4 = Second4[:] != boolSecond4
        Second4 = Second4[:][databoolSecond4]

        realtime4 = np.zeros((Year4.shape), dtype='S40')
        for i in range(Year4.shape[0]):
            realtime4[i] = datetime.datetime(Year4[i], Month4[i], Date4[i], Hour4[i], Minute4[i], Second4[i])
        o['/MPOBC/packagetime'] = realtime4

        Year5 = f5['/Time/Year'][:].astype('i4')
        Month5 = f5['/Time/Month'][:].astype('i4')
        Date5 = f5['/Time/Date'][:].astype('i4')
        Hour5 = f5['/Time/Hour'][:].astype('i4')
        Minute5 = f5['/Time/Minute'][:].astype('i4')
        Second5 = f5['/Time/Second'][:].astype('i4')

        boolYear5 = f5['/Time/Year'].attrs['FillValue']
        boolMonth5 = f5['/Time/Month'].attrs['FillValue']
        boolDate5 = f5['/Time/Date'].attrs['FillValue']
        boolHour5 = f5['/Time/Hour'].attrs['FillValue']
        boolMinute5 = f5['/Time/Minute'].attrs['FillValue']
        boolSecond5 = f5['/Time/Second'].attrs['FillValue']

        databoolYear5 = Year5[:] != boolYear5
        Year5 = Year5[:][databoolYear5]
        databoolMonth5 = Month5[:] != boolMonth5
        Month5 = Month5[:][databoolMonth5]
        databoolDate5 = Date5[:] != boolDate5
        Date5 = Date5[:][databoolDate5]
        databoolHour5 = Hour5[:] != boolHour5
        Hour5 = Hour5[:][databoolHour5]
        databoolMinute5 = Minute5[:] != boolMinute5
        Minute5 = Minute5[:][databoolMinute5]
        databoolSecond5 = Second5[:] != boolSecond5
        Second5 = Second5[:][databoolSecond5]

        realtime5 = np.zeros((Year5.shape), dtype='S40')
        for i in range(Year5.shape[0]):
            realtime5[i] = datetime.datetime(Year5[i], Month5[i], Date5[i], Hour5[i], Minute5[i], Second5[i])
        o['/SPOBC/packagetime'] = realtime5

        for i in f1['/Data'].keys():
            # print(i)
            datadim = f1['Data/' + i].ndim
            data = f1['Data/' + i][:][databoolSecond1]
            fillvalue = f1['Data/' + i].attrs['FillValue']
            if 'Count' not in i:
                if datadim == 1:
                    QAFlag = np.zeros((len(Year1)), dtype='u2')
                    # 阈值名称
                    dicname = i
                    if dicname in dicD1.keys():
                        # 全false
                        # print(dicD[dicDname], type(dicD[dicDname]))
                        # 离散的不在范围内置为1，填充值置为2
                        bool = np.isin(data, dicD1[dicname], invert=True)
                        fbool = (data == fillvalue)
                    else:
                        # 连续的不在范围内置为1，填充值置为2
                        bool = ((data < dicA1[dicname][0] - 0.05 * dicA1[dicname][1]) & (data != fillvalue)) | \
                               ((data > dicA1[dicname][1] + 0.05 * dicA1[dicname][1]) & (data != fillvalue))
                        fbool = (data == fillvalue)
                    QAFlag[bool] = 1
                    QAFlag[fbool] = 2

                elif datadim == 2:
                    QAFlag = np.zeros(data.shape, dtype='u2')
                    for m in range(data.shape[1]):
                        dicname = f'{i}{m}'
                        if dicname in dicD1.keys():
                            # 全false
                            # print(dicD[dicDname], type(dicD[dicDname]))
                            # 离散的不在范围内置为1，填充值置为2
                            bool = np.isin(data[:, m], dicD1[dicname], invert=True)
                            fbool = (data[:, m] == fillvalue)
                        else:
                            # 连续的不在范围内置为1，填充值置为2
                            bool = ((data[:, m] < dicA1[dicname][0] - 0.05 * dicA1[dicname][1]) & (
                                    data[:, m] != fillvalue)) | \
                                   ((data[:, m] > dicA1[dicname][1] + 0.05 * dicA1[dicname][1]) & (
                                           data[:, m] != fillvalue))
                            fbool = (data[:, m] == fillvalue)
                        QAFlag[:, m][bool] = 1
                        QAFlag[:, m][fbool] = 2

                o[f'HPOBC/QAFlag/{i}'] = QAFlag
                o[f'HPOBC/{i}'] = data
                # 把属性写进去
                for k in f1[f'/Data/{i}'].attrs.keys():
                    o[f'/HPOBC/{i}'].attrs[k] = f1[f'/Data/{i}'].attrs[k]

                name = []
                if datadim == 2:
                    for m in range(data.shape[1]):
                        name.append(i + str(m))
                    #     每个数据集对应的每一列都存在一个param写进QAflag里面
                    o[f'/HPOBC/QAFlag/{i}'].attrs['param'] = name
                else:
                    o[f'/HPOBC/QAFlag/{i}'].attrs['param'] = i
            else:
                continue

        for i in f2['/Data'].keys():
            # print(i)
            datadim = f2['Data/' + i].ndim
            data = f2['Data/' + i][:][databoolSecond2]
            fillvalue = f2['Data/' + i].attrs['FillValue']
            if 'Count' not in i:
                if datadim == 1:
                    QAFlag = np.zeros((len(Year2)), dtype='u2')
                    # 阈值名称
                    dicname = i
                    if dicname in dicD2.keys():
                        # 全false
                        # print(dicD[dicDname], type(dicD[dicDname]))
                        # 离散的不在范围内置为1，填充值置为2
                        bool = np.isin(data, dicD2[dicname], invert=True)
                        fbool = (data == fillvalue)
                    else:
                        # 连续的不在范围内置为1，填充值置为2
                        bool = ((data < dicA2[dicname][0] - 0.05 * dicA2[dicname][1]) & (data != fillvalue)) | \
                               ((data > dicA2[dicname][1] + 0.05 * dicA2[dicname][1]) & (data != fillvalue))
                        fbool = (data == fillvalue)
                    QAFlag[bool] = 1
                    QAFlag[fbool] = 2

                elif datadim == 2:
                    QAFlag = np.zeros(data.shape, dtype='u2')
                    for m in range(data.shape[1]):
                        dicname = f'{i}{m}'
                        if dicname in dicD2.keys():
                            # 全false
                            # print(dicD[dicDname], type(dicD[dicDname]))
                            # 离散的不在范围内置为1，填充值置为2
                            bool = np.isin(data[:, m], dicD2[dicname], invert=True)
                            fbool = (data[:, m] == fillvalue)
                        else:
                            # 连续的不在范围内置为1，填充值置为2
                            bool = ((data[:, m] < dicA2[dicname][0] - 0.05 * dicA2[dicname][1]) & (
                                    data[:, m] != fillvalue)) | \
                                   ((data[:, m] > dicA2[dicname][1] + 0.05 * dicA2[dicname][1]) & (
                                           data[:, m] != fillvalue))
                            fbool = (data[:, m] == fillvalue)
                        QAFlag[:, m][bool] = 1
                        QAFlag[:, m][fbool] = 2

                o[f'MEOBC/QAFlag/{i}'] = QAFlag
                o[f'MEOBC/{i}'] = data
                # 把属性写进去
                for k in f2[f'/Data/{i}'].attrs.keys():
                    o[f'/MEOBC/{i}'].attrs[k] = f2[f'/Data/{i}'].attrs[k]

                name = []
                if datadim == 2:
                    for m in range(data.shape[1]):
                        name.append(i + str(m))
                    #     每个数据集对应的每一列都存在一个param写进QAflag里面
                    o[f'/MEOBC/QAFlag/{i}'].attrs['param'] = name
                else:
                    o[f'/MEOBC/QAFlag/{i}'].attrs['param'] = i
            else:
                continue

        for i in f3['/Data'].keys():
            datadim = f3['Data/' + i].ndim
            data = f3['Data/' + i][:][databoolSecond3]
            fillvalue = f3['Data/' + i].attrs['FillValue']
            if 'Count' not in i:
                if datadim == 1:
                    QAFlag = np.zeros((len(Year3)), dtype='u2')
                    # 阈值名称
                    dicname = i
                    if dicname in dicD3.keys():
                        # 全false
                        # print(dicD[dicDname], type(dicD[dicDname]))
                        # 离散的不在范围内置为1，填充值置为2
                        bool = np.isin(data, dicD3[dicname], invert=True)
                        fbool = (data == fillvalue)
                    else:
                        # 连续的不在范围内置为1，填充值置为2
                        bool = ((data < dicA3[dicname][0] - 0.05 * dicA3[dicname][1]) & (data != fillvalue)) | \
                               ((data > dicA3[dicname][1] + 0.05 * dicA3[dicname][1]) & (data != fillvalue))
                        fbool = (data == fillvalue)
                    QAFlag[bool] = 1
                    QAFlag[fbool] = 2

                elif datadim == 2:
                    QAFlag = np.zeros(data.shape, dtype='u2')
                    for m in range(data.shape[1]):
                        dicname = f'{i}{m}'
                        if dicname in dicD3.keys():
                            # 全false
                            # print(dicD[dicDname], type(dicD[dicDname]))
                            # 离散的不在范围内置为1，填充值置为2
                            bool = np.isin(data[:, m], dicD3[dicname], invert=True)
                            fbool = (data[:, m] == fillvalue)
                        else:
                            # 连续的不在范围内置为1，填充值置为2
                            bool = ((data[:, m] < dicA3[dicname][0] - 0.05 * dicA3[dicname][1]) & (
                                    data[:, m] != fillvalue)) | \
                                   ((data[:, m] > dicA3[dicname][1] + 0.05 * dicA3[dicname][1]) & (
                                           data[:, m] != fillvalue))
                            fbool = (data[:, m] == fillvalue)
                        QAFlag[:, m][bool] = 1
                        QAFlag[:, m][fbool] = 2

                o[f'MFOBC/QAFlag/{i}'] = QAFlag
                o[f'MFOBC/{i}'] = data
                # 把属性写进去
                for k in f3[f'/Data/{i}'].attrs.keys():
                    o[f'/MFOBC/{i}'].attrs[k] = f3[f'/Data/{i}'].attrs[k]

                name = []
                if datadim == 2:
                    for m in range(data.shape[1]):
                        name.append(i + str(m))
                    #     每个数据集对应的每一列都存在一个param写进QAflag里面
                    o[f'/MFOBC/QAFlag/{i}'].attrs['param'] = name
                else:
                    o[f'/MFOBC/QAFlag/{i}'].attrs['param'] = i
            else:
                continue

        for i in f4['/Data'].keys():
            datadim = f4['Data/' + i].ndim
            data = f4['Data/' + i][:][databoolSecond4]
            fillvalue = f4['Data/' + i].attrs['FillValue']
            if '12D' in i:
                if datadim == 1:
                    QAFlag = np.zeros((len(Year4)), dtype='u2')
                    # 阈值名称
                    dicname = i
                    if dicname in dicD4.keys():
                        # 全false
                        # print(dicD[dicDname], type(dicD[dicDname]))
                        # 离散的不在范围内置为1，填充值置为2
                        bool = np.isin(data, dicD4[dicname], invert=True)
                        fbool = (data == fillvalue)
                    else:
                        # 连续的不在范围内置为1，填充值置为2
                        bool = ((data < dicA4[dicname][0] - 0.05 * dicA4[dicname][1]) & (data != fillvalue)) | \
                               ((data > dicA4[dicname][1] + 0.05 * dicA4[dicname][1]) & (data != fillvalue))
                        fbool = (data == fillvalue)
                    QAFlag[bool] = 1
                    QAFlag[fbool] = 2

                elif datadim == 2:
                    QAFlag = np.zeros(data.shape, dtype='u2')
                    for m in range(data.shape[1]):
                        dicname = f'{i}{m}'
                        if dicname in dicD4.keys():
                            # 全false
                            # print(dicD[dicDname], type(dicD[dicDname]))
                            # 离散的不在范围内置为1，填充值置为2
                            bool = np.isin(data[:, m], dicD4[dicname], invert=True)
                            fbool = (data[:, m] == fillvalue)
                        else:
                            # 连续的不在范围内置为1，填充值置为2
                            bool = ((data[:, m] < dicA4[dicname][0] - 0.05 * dicA5[dicname][1]) & (
                                    data[:, m] != fillvalue)) | \
                                   ((data[:, m] > dicA4[dicname][1] + 0.05 * dicA5[dicname][1]) & (
                                           data[:, m] != fillvalue))
                            fbool = (data[:, m] == fillvalue)
                        QAFlag[:, m][bool] = 1
                        QAFlag[:, m][fbool] = 2

                o[f'MPOBC/QAFlag/{i}'] = QAFlag
                o[f'MPOBC/{i}'] = data
                # 把属性写进去
                for k in f4[f'/Data/{i}'].attrs.keys():
                    o[f'/MPOBC/{i}'].attrs[k] = f4[f'/Data/{i}'].attrs[k]

                name = []
                if datadim == 2:
                    for m in range(data.shape[1]):
                        name.append(i + str(m))
                    #     每个数据集对应的每一列都存在一个param写进QAflag里面
                    o[f'/MPOBC/QAFlag/{i}'].attrs['param'] = name
                else:
                    o[f'/MPOBC/QAFlag/{i}'].attrs['param'] = i

        for i in f5['/Data'].keys():
            datadim = f5['Data/' + i].ndim
            data = f5['Data/' + i][:][databoolSecond5]
            fillvalue = f5['Data/' + i].attrs['FillValue']
            if 'Count' not in i:
                if datadim == 1:
                    QAFlag = np.zeros((len(Year5)), dtype='u2')
                    # 阈值名称
                    dicname = i
                    if dicname in dicD5.keys():
                        # 全false
                        # print(dicD[dicDname], type(dicD[dicDname]))
                        # 离散的不在范围内置为1，填充值置为2
                        bool = np.isin(data, dicD5[dicname], invert=True)
                        fbool = (data == fillvalue)
                    else:
                        # 连续的不在范围内置为1，填充值置为2
                        bool = ((data < dicA5[dicname][0] - 0.05 * dicA5[dicname][1]) & (data != fillvalue)) | \
                               ((data > dicA5[dicname][1] + 0.05 * dicA5[dicname][1]) & (data != fillvalue))
                        fbool = (data == fillvalue)
                    QAFlag[bool] = 1
                    QAFlag[fbool] = 2

                elif datadim == 2:
                    QAFlag = np.zeros(data.shape, dtype='u2')
                    for m in range(data.shape[1]):
                        dicname = f'{i}{m}'
                        if dicname in dicD5.keys():
                            # 全false
                            # print(dicD[dicDname], type(dicD[dicDname]))
                            # 离散的不在范围内置为1，填充值置为2
                            bool = np.isin(data[:, m], dicD5[dicname], invert=True)
                            fbool = (data[:, m] == fillvalue)
                        else:
                            # 连续的不在范围内置为1，填充值置为2
                            bool = ((data[:, m] < dicA5[dicname][0] - 0.05 * dicA5[dicname][1]) & (
                                    data[:, m] != fillvalue)) | \
                                   ((data[:, m] > dicA5[dicname][1] + 0.05 * dicA5[dicname][1]) & (
                                           data[:, m] != fillvalue))
                            fbool = (data[:, m] == fillvalue)
                        QAFlag[:, m][bool] = 1
                        QAFlag[:, m][fbool] = 2

                o[f'SPOBC/QAFlag/{i}'] = QAFlag
                o[f'SPOBC/{i}'] = data
                # 把属性写进去
                for k in f5[f'/Data/{i}'].attrs.keys():
                    o[f'/SPOBC/{i}'].attrs[k] = f5[f'/Data/{i}'].attrs[k]

                name = []
                if datadim == 2:
                    for m in range(data.shape[1]):
                        name.append(i + str(m))
                    #     每个数据集对应的每一列都存在一个param写进QAflag里面
                    o[f'/SPOBC/QAFlag/{i}'].attrs['param'] = name
                else:
                    o[f'/SPOBC/QAFlag/{i}'].attrs['param'] = i


import glob
import os

x = glob.glob('/FY3E/SEM/1A/HPOBC/2022/20220105/FY3E_SEM--_ORBT_1A_*_*_HPOBC_V0.HDF')
for i in x:
    xx(i)
