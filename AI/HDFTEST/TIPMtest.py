# -*- coding:utf-8 -*-
import h5py
import pickle
import sys
import glob
import numpy as np
import time, datetime

# 阈值范围
outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/YAML/TRIPM_A.pkl'
outputfileD = '/STSS/FY3E_STSS/dev/AIWarning/YAML/TRIPM_D.pkl'
# 将AD字典读入
pkl_file = open(outputfileA, 'rb')
dicA = pickle.load(pkl_file)
pkl_file = open(outputfileD, 'rb')
dicD = pickle.load(pkl_file)
# print(dicA)
# print('-------------------------------------------------')
# print(dicD)
# exit()

# filename = '/FY3E/TRIPM/1A/2022/20220105/FY3E_TRIPM_ORBT_1A_20220105_2311_OBC--_V0.HDF'
# outfilename = '/STSS/FY3E_STSS/dev/AIWarning/Code/HDFTEST/HDF/FY3E_TRIPM_ORBT_1A_20220105_2311_OBC--_V0.HDF'

if __name__ == '__main__':
    # 输入时间,时次
    date = sys.argv[1]
    filelist = sorted(glob.glob(r'/FY3E/TRIPM/1A/%s/%s/*.HDF' % (date[0:4], date)))
    for i in filelist:
        print(i)
        filename = i
        outfilename = '/STSS/FY3E_STSS/dev/AIWarning/HDFTEST/HDF/TRIPM/' + i.split('/')[-1]
        with h5py.File(filename, 'r') as f, h5py.File(outfilename, 'w') as o:
            # packgetime时间
            Daycnt = (f['/Telemetry/Orbit_daycnt'][:].astype('f4') * 24 * 60 * 60 * 1000).astype('i8')
            Mscnt = (f['/Telemetry/Orbit_mscnt'][:].astype('f4')).astype('i8')

            fillvalueD = f['/Telemetry/Orbit_daycnt'].attrs['FillValue']
            fillvalueM = f['/Telemetry/Orbit_mscnt'].attrs['FillValue']

            databoolD = (Daycnt[:] != fillvalueD) & (Daycnt[:] != 0)
            Daycnt = Daycnt[:][databoolD]

            databoolM = (Mscnt[:] != fillvalueM) & (Mscnt[:] != 0)
            Mscnt = Mscnt[:][databoolM]

            tmp = time.mktime(time.strptime("2000-01-01 12:00:00", '%Y-%m-%d %H:%M:%S'))
            realtime = np.zeros((Mscnt.shape), dtype='S40')
            for i in range(Mscnt.shape[0]):
                realtime[i] = datetime.datetime.fromtimestamp((Daycnt[i] + Mscnt[i]) / 1000 + tmp).strftime(
                    '%Y-%m-%d %H:%M:%S')
            o['/Telemetry/packagetime'] = realtime

            for i in f['/Telemetry'].keys():
                if 'Calibra_' in i or 'Cnt' in i or 'cnt' in i:
                    pass
                else:
                    datadim = f['Telemetry/' + i].ndim
                    data = f['Telemetry/' + i][:][databoolM]
                    fillvalue = f['Telemetry/' + i].attrs['FillValue']
                    if datadim == 1:
                        QAFlag = np.zeros((len(Mscnt)), dtype='u2')
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
                            bool = ((data < dicA[dicname][0] - 0.05 * dicA[dicname][1]) & (data != fillvalue)) | \
                                   ((data > dicA[dicname][1] + 0.05 * dicA[dicname][1]) & (data != fillvalue))
                            fbool = (data == fillvalue)
                        QAFlag[bool] = 1
                        QAFlag[fbool] = 2

                    elif datadim == 2:
                        QAFlag = np.zeros(data.shape, dtype='u2')
                        for m in range(data.shape[1]):
                            dicname = f'Telemetry_{i}_{m}'
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
                        o[f'/Telemetry/QAFlag/{i}'].attrs['param'] = name
                    else:
                        o[f'/Telemetry/QAFlag/{i}'].attrs['param'] = i
