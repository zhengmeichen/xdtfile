# -*- coding:utf-8 -*-
import h5py
import sys
import glob
import pickle
import numpy as np
import time, datetime

# 阈值范围
outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/YAML/XEUVI_A.pkl'
outputfileD = '/STSS/FY3E_STSS/dev/AIWarning/YAML/XEUVI_D.pkl'
# outputfileA = 'C:\\Users\\19683\\Downloads\\XEUVI_A.pkl'
# outputfileD = 'C:\\Users\\19683\\Downloads\\XEUVI_D.pkl'
# 将AD字典读入
pkl_file = open(outputfileA, 'rb')
dicA = pickle.load(pkl_file)
pkl_file = open(outputfileD, 'rb')
dicD = pickle.load(pkl_file)
# print(dicA)
# print('-------------------------------------------------')
# print(dicD)
# exit()

# filename = '/FY3E/XEUVI/1A/GRAN/2022/20220105/FY3E_XEUVI_GRAN_1A_20220105_1415_OBC--_V0.HDF'
# outfilename = '/STSS/FY3E_STSS/dev/AIWarning/Code/HDFTEST/HDF/FY3E_XEUVI_GRAN_1A_20220105_1415_OBC--_V0.HDF'


if __name__ == '__main__':
    date = sys.argv[1]
    filelist = sorted(glob.glob(r'/FY3E/XEUVI/1A/GRAN/%s/%s/*.HDF' % (date[0:4], date)))
    for i in filelist:
        print(i)
        filename = i
        outfilename = '/STSS/FY3E_STSS/dev/AIWarning/HDFTEST/HDF/XEUVI/' + i.split('/')[-1]

        with h5py.File(filename, 'r') as f, h5py.File(outfilename, 'w') as o:

            # packgetime时间
            Daycnt = (f['/Time/Day_Count'][:, 0].astype('f4') * 24 * 60 * 60 * 1000).astype('i8')
            Mscnt = (f['/Time/Msec_Count'][:, 0].astype('f4') * 0.1).astype('i8')

            tmp = time.mktime(time.strptime("2000-01-01 12:00:00", '%Y-%m-%d %H:%M:%S'))
            realtime = np.zeros((Daycnt.shape), dtype='S40')

            for i in range(Daycnt.shape[0]):
                # print(Mscnt[i])
                realtime[i] = datetime.datetime.fromtimestamp((Daycnt[i] + Mscnt[i]) / 1000 + tmp).strftime(
                    '%Y-%m-%d %H:%M:%S')
            o['/Ancillary/packagetime'] = realtime
            o['/Telemetry/packagetime'] = realtime

            for i in f['/Ancillary'].keys():
                datadim = f['Ancillary/' + i].ndim
                data = f['Ancillary/' + i][:]
                # XEUVI没有fillvalue属性
                # fillvalue = f['Ancillary/' + i].attrs['FillValue']

                if datadim == 1:
                    QAFlag = np.zeros((len(Daycnt)), dtype='u2')
                    # 阈值名称
                    dicname = f'Ancillary_{i}'
                    if dicname in dicD.keys():
                        # 全false
                        # print(dicD[dicDname], type(dicD[dicDname]))
                        # 离散的不在范围内置为1，填充值置为2
                        bool = np.isin(data, dicD[dicname], invert=True)
                    else:
                        # 连续的不在范围内置为1，填充值置为2
                        bool = (data < dicA[dicname][0] - 0.05 * dicA[dicname][1]) | (
                                data > dicA[dicname][1] + 0.05 * dicA[dicname][1])
                    QAFlag[bool] = 1

                elif datadim == 2:
                    QAFlag = np.zeros(data.shape, dtype='u2')
                    for m in range(data.shape[1]):
                        dicname = f'Ancillary_{i}_{m}'
                        if dicname in dicD.keys():
                            # 全false
                            # print(dicD[dicDname], type(dicD[dicDname]))
                            # 离散的不在范围内置为1，填充值置为2
                            bool = np.isin(data[:, m], dicD[dicname], invert=True)
                        else:
                            # 连续的不在范围内置为1，填充值置为2
                            bool = (data[:, m] < dicA[dicname][0] - 0.05 * dicA[dicname][1]) | (
                                    data[:, m] > dicA[dicname][1] + 0.05 * dicA[dicname][1])
                        QAFlag[:, m][bool] = 1

                o[f'Ancillary/QAFlag/{i}'] = QAFlag
                o[f'Ancillary/{i}'] = data
                # 把属性写进去
                for k in f[f'/Ancillary/{i}'].attrs.keys():
                    o[f'Ancillary/{i}'].attrs[k] = f[f'/Ancillary/{i}'].attrs[k]

                name = []
                if datadim == 2:
                    for m in range(data.shape[1]):
                        name.append(i + str(m))
                    #     每个数据集对应的每一列都存在一个param写进QAflag里面
                    o[f'/Ancillary/QAFlag/{i}'].attrs['param'] = name
                else:
                    o[f'/Ancillary/QAFlag/{i}'].attrs['param'] = i

            for i in f['/Telemetry'].keys():
                if 'Sat_Lon_Lat_Height' in i or 'NaviMirrData' in i:
                    pass
                else:
                    datadim = f['Telemetry/' + i].ndim
                    data = f['Telemetry/' + i][:]
                    # XEUVI没有fillvalue属性
                    # fillvalue = f['Ancillary/' + i].attrs['FillValue']

                    if datadim == 1:
                        QAFlag = np.zeros((len(Daycnt)), dtype='u2')
                        # 阈值名称
                        dicname = f'Telemetry_{i}'
                        if dicname in dicD.keys():
                            # 全false
                            # print(dicD[dicDname], type(dicD[dicDname]))
                            # 离散的不在范围内置为1，填充值置为2
                            bool = np.isin(data, dicD[dicname], invert=True)
                        else:
                            # 连续的不在范围内置为1，填充值置为2
                            bool = (data < dicA[dicname][0] - 0.05 * dicA[dicname][1]) | (
                                    data > dicA[dicname][1] + 0.05 * dicA[dicname][1])
                        QAFlag[bool] = 1

                    elif datadim == 2:
                        QAFlag = np.zeros(data.shape, dtype='u2')
                        for m in range(data.shape[1]):
                            dicname = f'Telemetry_{i}_{m}'
                            if dicname in dicD.keys():
                                # 全false
                                # print(dicD[dicDname], type(dicD[dicDname]))
                                # 离散的不在范围内置为1，填充值置为2
                                bool = np.isin(data[:, m], dicD[dicname], invert=True)
                            else:
                                # 连续的不在范围内置为1，填充值置为2
                                bool = (data[:, m] < dicA[dicname][0] - 0.05 * dicA[dicname][1]) | (
                                        data[:, m] > dicA[dicname][1] + 0.05 * dicA[dicname][1])
                            QAFlag[:, m][bool] = 1

                    o[f'Telemetry/QAFlag/{i}'] = QAFlag
                    o[f'Telemetry/{i}'] = data
                    # 把属性写进去
                    for k in f[f'Telemetry/{i}'].attrs.keys():
                        o[f'Telemetry/{i}'].attrs[k] = f[f'Telemetry/{i}'].attrs[k]

                    name = []
                    if datadim == 2:
                        for m in range(data.shape[1]):
                            name.append(i + str(m))
                        #     每个数据集对应的每一列都存在一个param写进QAflag里面
                        o[f'Telemetry/QAFlag/{i}'].attrs['param'] = name
                    else:
                        o[f'Telemetry/QAFlag/{i}'].attrs['param'] = i