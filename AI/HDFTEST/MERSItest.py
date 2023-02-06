# -*- coding:utf-8 -*-
import pickle
import h5py
import numpy as np
import time, datetime

# 阈值范围
outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/YAML/MERSI_A.pkl'
outputfileD = '/STSS/FY3E_STSS/dev/AIWarning/YAML/MERSI_D.pkl'
# outputfileA = 'C:\\Users\\19683\\Downloads\\MERSI_A.pkl'
# outputfileD = 'C:\\Users\\19683\\Downloads\\MERSI_D.pkl'
# 将AD字典读入
pkl_file = open(outputfileA, 'rb')
dicA = pickle.load(pkl_file, encoding='iso-8859-1')
pkl_file = open(outputfileD, 'rb')
dicD = pickle.load(pkl_file, encoding='iso-8859-1')
# print(dicA)
# print('-------------------------------------------------')
# print(dicD)
# exit()

filename = '/FY3E/MERSI/1A/OBC/2022/20220105/FY3E_MERSI_GRAN_1A_20220105_0615_OBC--_V0.HDF'
outfilename = '/STSS/FY3E_STSS/dev/AIWarning/Code/HDFTEST/HDF/FY3E_MERSI_GRAN_1A_20220105_0615_OBC--_V0.HDF'
# filename = 'C:\\Users\\19683\\Downloads\\FY3E_MERSI_GRAN_1A_20220102_0000_OBC--_V0.HDF'
# outfilename = 'C:\\Users\\19683\\Downloads\\FY3E_MERSI_GRAN_1A_20220102_OBC--_V0.HDF'

if __name__ == '__main__':
    with h5py.File(filename, 'r') as f, h5py.File(outfilename, 'w') as o:
        # packgetime时间
        Daycnt = (f['/Time/Day_Count'][:].astype('f4') * 24 * 60 * 60 * 1000).astype('i8')
        Mscnt = (f['/Time/Millisecond_Count'][:].astype('f4') * 0.1).astype('i8')

        fillvalueD = f['/Time/Day_Count'].attrs['FillValue']
        fillvalueM = f['/Time/Millisecond_Count'].attrs['FillValue']

        databoolD = Daycnt[:] != fillvalueD
        Daycnt = Daycnt[:][databoolD]

        databoolM = Mscnt[:] != fillvalueM
        Mscnt = Mscnt[:][databoolM]

        tmp = time.mktime(time.strptime("2000-01-01 12:00:00", '%Y-%m-%d %H:%M:%S'))
        realtime = np.zeros((Daycnt.shape), dtype='S40')
        for i in range(Daycnt.shape[0]):
            realtime[i] = datetime.datetime.fromtimestamp((Daycnt[i] + Mscnt[i]) / 1000 + tmp).strftime(
                '%Y-%m-%d %H:%M:%S')
        o['/Engineering/packagetime'] = realtime
        o['/Temporary/packagetime'] = realtime
        o['/Telemetry/packagetime'] = realtime

        for i in f['/Engineering'].keys():
            if 'OBC' in i:
                datadim = f['Engineering/' + i].ndim
                # data = f['Engineering/' + i][:].transpose((1, 2, 0))
                data = f['Engineering/' + i][-1, :, :][databoolM]
                data.reshape((f['Engineering/' + i].shape[1], -1))
                fillvalue = f['Engineering/' + i].attrs['FillValue']
                QAFlag = np.zeros(data.shape, dtype='u2')
                for m in range(data.shape[1]):
                    dicname = f'Engineering_{i}{m}'
                    if dicname in dicD.keys():
                        # 全false
                        # print(dicD[dicDname], type(dicD[dicDname]))
                        # 离散的不在范围内置为1，填充值置为2
                        bool = np.isin(data[:, m], dicD[dicname], invert=True)
                        fbool = (data[:, m] == fillvalue)
                    else:
                        # 连续的不在范围内置为1，填充值置为2
                        bool = ((data[:, m] < dicA[dicname][0]) & (data[:, m] != fillvalue)) | \
                               ((data[:, m] > dicA[dicname][1]) & (data[:, m] != fillvalue))
                        fbool = (data[:, m] == fillvalue)
                    QAFlag[:, m][bool] = 1
                    QAFlag[:, m][fbool] = 2

                o[f'Engineering/QAFlag/{i}'] = QAFlag
                o[f'Engineering/{i}'] = data
                # 把属性写进去
                for k in f[f'/Engineering/{i}'].attrs.keys():
                    o[f'Engineering/{i}'].attrs[k] = f[f'/Engineering/{i}'].attrs[k]

                name = []
                for m in range(data.shape[1]):
                    name.append(i + str(m))
                #     每个数据集对应的每一列都存在一个param写进QAflag里面
                o[f'/Engineering/QAFlag/{i}'].attrs['param'] = name

        for i in f['/Telemetry'].keys():
            if 'SD_Angle' in i:
                pass
            else:
                datadim = f['Telemetry/' + i].ndim
                if datadim == 3:
                    data = f['Telemetry/' + i][:, -1, :][databoolM]
                    data.reshape((f['Telemetry/' + i].shape[0], -1))
                    # print(data.shape)
                else:
                    data = f['Telemetry/' + i][:][databoolM]
                fillvalue = f['Telemetry/' + i].attrs['FillValue']

                if datadim == 1:
                    QAFlag = np.zeros((len(Daycnt)), dtype='u2')
                    # 阈值名称
                    dicname = f'Telemetry_{i}'
                    if dicname in dicD.keys():
                        # 全false
                        # print(dicD[dicDname], type(dicD[dicDname]))
                        # 离散的不在范围内置为1，填充值置为2
                        bool = np.isin(data, dicD[dicname], invert=True)
                        fbool = (data == fillvalue)
                    else:
                        # 连续的不在范围内置为1，填充值置为2
                        bool = ((data < dicA[dicname][0]) & (data != fillvalue)) | \
                               ((data > dicA[dicname][1]) & (data != fillvalue))
                        fbool = (data == fillvalue)
                    QAFlag[bool] = 1
                    QAFlag[fbool] = 2

                elif datadim == 2:
                    QAFlag = np.zeros(data.shape, dtype='u2')
                    for m in range(data.shape[1]):
                        dicname = f'Telemetry_{i}{m}'
                        if dicname in dicD.keys():
                            # 全false
                            # print(dicD[dicDname], type(dicD[dicDname]))
                            # 离散的不在范围内置为1，填充值置为2
                            bool = np.isin(data[:, m], dicD[dicname], invert=True)
                            fbool = (data[:, m] == fillvalue)
                        else:
                            # 连续的不在范围内置为1，填充值置为2
                            bool = ((data[:, m] < dicA[dicname][0]) & (data[:, m] != fillvalue)) | \
                                   ((data[:, m] > dicA[dicname][1]) & (data[:, m] != fillvalue))
                            fbool = (data[:, m] == fillvalue)
                        QAFlag[:, m][bool] = 1
                        QAFlag[:, m][fbool] = 2

                elif datadim == 3:
                    QAFlag = np.zeros(data.shape, dtype='u2')
                    for m in range(data.shape[1]):
                        dicname = f'Telemetry_{i}{m}'
                        if dicname in dicD.keys():
                            # 全false
                            # print(dicD[dicDname], type(dicD[dicDname]))
                            # 离散的不在范围内置为1，填充值置为2
                            bool = np.isin(data[:, m], dicD[dicname], invert=True)
                            fbool = (data[:, m] == fillvalue)
                        else:
                            # 连续的不在范围内置为1，填充值置为2
                            bool = ((data[:, m] < dicA[dicname][0]) & (data[:, m] != fillvalue)) | \
                                   ((data[:, m] > dicA[dicname][1]) & (data[:, m] != fillvalue))
                            fbool = (data[:, m] == fillvalue)
                        QAFlag[:, m][bool] = 1
                        QAFlag[:, m][fbool] = 2

                o[f'Telemetry/QAFlag/{i}'] = QAFlag
                o[f'Telemetry/{i}'] = data
                # 把属性写进去
                for k in f[f'Telemetry/{i}'].attrs.keys():
                    o[f'Telemetry/{i}'].attrs[k] = f[f'/Telemetry/{i}'].attrs[k]

                name = []
                if datadim == 2:
                    for m in range(data.shape[1]):
                        name.append(i + str(m))
                    #     每个数据集对应的每一列都存在一个param写进QAflag里面
                    o[f'/Telemetry/QAFlag/{i}'].attrs['param'] = name
                elif datadim == 3:
                    # length = data.shape[1] * data.shape[2]
                    # for m in range(length):
                    #     name.append(i + str(m))
                    # #     每个数据集对应的每一列都存在一个param写进QAflag里面
                    # o[f'/Calibration/QAFlag/{i}'].attrs['param'] = name
                    for m in range(data.shape[1]):
                        name.append(i + str(m))
                    #     每个数据集对应的每一列都存在一个param写进QAflag里面
                    o[f'/Telemetry/QAFlag/{i}'].attrs['param'] = name
                else:
                    o[f'/Telemetry/QAFlag/{i}'].attrs['param'] = i

        for i in f['/Temporary'].keys():
            if 'BB_DN_average' in i or 'BB_DN_standard' in i or 'SV_DN_average' in i or 'SV_DN_standard' in i \
                    or 'VOC_DN_average' in i or 'VOC_DN_standard' in i:

                datadim = f['Temporary/' + i].ndim
                data = f['Temporary/' + i][:][databoolM].T
                # data = f['Temporary/' + i][:][databoolM]
                fillvalue = f['Temporary/' + i].attrs['FillValue']
                QAFlag = np.zeros(data.shape, dtype='u2')
                for m in range(data.shape[1]):
                    dicname = f'Temporary_{i}{m}'
                    if dicname in dicD.keys():
                        # 全false
                        # print(dicD[dicDname], type(dicD[dicDname]))
                        # 离散的不在范围内置为1，填充值置为2
                        bool = np.isin(data[:, m], dicD[dicname], invert=True)
                        fbool = (data[:, m] == fillvalue)
                    else:
                        # 连续的不在范围内置为1，填充值置为2
                        bool = ((data[:, m] < dicA[dicname][0]) & (data[:, m] != fillvalue)) | \
                               ((data[:, m] > dicA[dicname][1]) & (data[:, m] != fillvalue))
                        fbool = (data[:, m] == fillvalue)
                    QAFlag[:, m][bool] = 1
                    QAFlag[:, m][fbool] = 2
                o[f'/Temporary/QAFlag/{i}'] = QAFlag
                o[f'/Temporary/{i}'] = data
                # 把属性写进去
                for k in f[f'/Temporary/{i}'].attrs.keys():
                    o[f'Temporary/{i}'].attrs[k] = f[f'/Temporary/{i}'].attrs[k]
                name = []
                for m in range(data.shape[1]):
                    name.append(i + str(m))
                #     每个数据集对应的每一列都存在一个param写进QAflag里面
                o[f'/Temporary/QAFlag/{i}'].attrs['param'] = name

            elif 'Average_Temperature' in i:
                datadim = f['Temporary/' + i].ndim
                data = f['Temporary/' + i][:][databoolM]
                fillvalue = f['Temporary/' + i].attrs['FillValue']
                QAFlag = np.zeros((len(Daycnt)), dtype='u2')
                # 阈值名称
                dicname = f'Temporary_{i}'
                if dicname in dicD.keys():
                    # 全false
                    # print(dicD[dicDname], type(dicD[dicDname]))
                    # 离散的不在范围内置为1，填充值置为2
                    bool = np.isin(data, dicD[dicname], invert=True)
                    fbool = (data == fillvalue)
                else:
                    # 连续的不在范围内置为1，填充值置为2
                    bool = ((data < dicA[dicname][0]) & (data != fillvalue)) | \
                           ((data > dicA[dicname][1]) & (data != fillvalue))
                    fbool = (data == fillvalue)
                QAFlag[bool] = 1
                QAFlag[fbool] = 2

                o[f'Temporary/QAFlag/{i}'] = QAFlag
                o[f'Temporary/{i}'] = data
                # 把属性写进去
                for k in f[f'/Temporary/{i}'].attrs.keys():
                    o[f'Temporary/{i}'].attrs[k] = f[f'/Temporary/{i}'].attrs[k]
                o[f'Temporary/QAFlag/{i}'].attrs['param'] = i
