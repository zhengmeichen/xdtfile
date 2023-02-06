# -*- coding:utf-8 -*-
import h5py
import pickle
import sys
import glob
import numpy as np
import time, datetime

# 阈值范围
outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/YAML/HIRAS_A.pkl'
outputfileD = '/STSS/FY3E_STSS/dev/AIWarning/YAML/HIRAS_D.pkl'
# outputfileA = 'C:\\Users\\19683\\Downloads\\HIRAS_A.pkl'
# outputfileD = 'C:\\Users\\19683\\Downloads\\HIRAS_D.pkl'

# 将AD字典读入
pkl_file = open(outputfileA, 'rb')
dicA = pickle.load(pkl_file)
pkl_file = open(outputfileD, 'rb')
dicD = pickle.load(pkl_file)
# print(dicA)
# print('-------------------------------------------')
# print(dicD)
# exit()

filename = '/FY3E/HIRAS/1A/OBC/2022/20220105/FY3E_HIRAS_GRAN_1A_20220105_1955_OBC--_V0.HDF'
outfilename = '/STSS/FY3E_STSS/dev/AIWarning/Code/HDFTEST/HDF/FY3E_HIRAS_GRAN_1A_20220105_1955_OBC--_V0.HDF'
# filename = 'C:\\Users\\zhengmeichen\\Downloads\\FY3E_HIRAS_GRAN_1A_20220103_0000_OBC--_V0.HDF'
# outfilename = 'C:\\Users\\zhengmeichen\\Downloads\\FY3E_HIRAS_GRAN_1A_20220103_OBC--_V0.HDF'

if __name__ == '__main__':
    # 输入时间,时次
    date = sys.argv[1]
    filelist = sorted(glob.glob(r'/FY3E/HIRAS/1A/OBC/%s/%s/*.HDF' % (date[0:4], date)))
    for i in filelist:
        print(i)
        filename = i
        outfilename = '/STSS/FY3E_STSS/dev/AIWarning/HDFTEST/HDF/HIRAS/' + i.split('/')[-1]
        with h5py.File(filename, 'r') as f, h5py.File(outfilename, 'w') as o:
            # packgetime时间
            Daycnt = (f['/Geo/Daycnt'][:, 0].astype('f4') * 24 * 60 * 60 * 1000).astype('i8')
            Mscnt = (f['/Geo/Mscnt'][:, 0].astype('f4') * 0.1).astype('i8')

            fillvalueD = f['/Geo/Daycnt'].attrs['FillValue']
            fillvalueM = f['/Geo/Daycnt'].attrs['FillValue']

            databoolD = Daycnt[:] != fillvalueD
            Daycnt = Daycnt[:][databoolD]

            databoolM = Mscnt[:] != fillvalueM
            Mscnt = Mscnt[:][databoolM]

            tmp = time.mktime(time.strptime("2000-01-01 12:00:00", '%Y-%m-%d %H:%M:%S'))
            realtime = np.zeros((Daycnt.shape), dtype='S40')
            for i in range(Daycnt.shape[0]):
                realtime[i] = datetime.datetime.fromtimestamp((Daycnt[i] + Mscnt[i]) / 1000 + tmp).strftime(
                    '%Y-%m-%d %H:%M:%S')
            o['/Tele/packagetime'] = realtime
            o['/Temp/packagetime'] = realtime

            for i in f['/Tele'].keys():
                datadim = f['Tele/' + i].ndim
                if datadim == 2:
                    data = f['Tele/' + i][:, -1][databoolM]
                    # data.reshape((f['Tele/' + i].shape[0],))
                elif datadim == 3:
                    data = f['Tele/' + i][:, -1, :][databoolM]
                    data.reshape((f['Tele/' + i].shape[0], -1))
                else:
                    data = f['Tele/' + i][:][databoolM]
                fillvalue = f['Tele/' + i].attrs['FillValue']

                if datadim == 1 or datadim == 2:
                    QAFlag = np.zeros((len(Daycnt)), dtype='u2')
                    # 阈值名称
                    dicname = f'Tele_{i}'
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

                elif datadim == 3:
                    QAFlag = np.zeros(data.shape, dtype='u2')
                    for m in range(data.shape[1]):
                        dicname = f'Tele_{i}{m}'
                        if dicname in dicD.keys():
                            # 全false
                            # print(dicD[dicDname], type(dicD[dicDname]))
                            # 离散的不在范围内置为1，填充值置为2
                            bool = np.isin(data[:, m], dicD[dicname], invert=True)
                            fbool = (data[:, m] == fillvalue)
                        else:
                            # 连续的不在范围内置为1，填充值置为2
                            bool = ((data[:, m] < dicA[dicname][0] - 0.05 * dicA[dicname][1]) & (data[:, m] != fillvalue)) | \
                                   ((data[:, m] > dicA[dicname][1] + 0.05 * dicA[dicname][1]) & (data[:, m] != fillvalue))
                            fbool = (data[:, m] == fillvalue)
                        QAFlag[:, m][bool] = 1
                        QAFlag[:, m][fbool] = 2
                o[f'Tele/QAFlag/{i}'] = QAFlag
                o[f'Tele/{i}'] = data
                # 把属性写进去
                for k in f[f'/Tele/{i}'].attrs.keys():
                    o[f'Tele/{i}'].attrs[k] = f[f'/Tele/{i}'].attrs[k]

                name = []
                if datadim == 3:
                    # length = data.shape[1] * data.shape[2]
                    # for m in range(length):
                    #     name.append(i + str(m))
                    # #     每个数据集对应的每一列都存在一个param写进QAflag里面
                    # o[f'/Calibration/QAFlag/{i}'].attrs['param'] = name
                    for m in range(data.shape[1]):
                        name.append(i + str(m))
                    #     每个数据集对应的每一列都存在一个param写进QAflag里面
                    o[f'/Tele/QAFlag/{i}'].attrs['param'] = name
                else:
                    o[f'/Tele/QAFlag/{i}'].attrs['param'] = i

            for i in f['/Temp'].keys():
                datadim = f['Temp/' + i].ndim
                if datadim == 2:
                    data = f['Temp/' + i][:, -1][databoolM]
                    # data.reshape((f['Temp/' + i].shape[0],))
                elif datadim == 3:
                    data = f['Temp/' + i][:, -1, :][databoolM]
                    data.reshape((f['Temp/' + i].shape[0], -1))
                else:
                    data = f['Temp/' + i][:][databoolM]
                fillvalue = f['Temp/' + i].attrs['FillValue']

                if datadim == 1 or datadim == 2:
                    QAFlag = np.zeros((len(Daycnt)), dtype='u2')
                    # 阈值名称
                    dicname = f'Temp_{i}'
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

     
                elif datadim == 3:
                    QAFlag = np.zeros(data.shape, dtype='u2')
                    for m in range(data.shape[1]):
                        dicname = f'Temp_{i}{m}'
                        if dicname in dicD.keys():
                            # 全false
                            # print(dicD[dicDname], type(dicD[dicDname]))
                            # 离散的不在范围内置为1，填充值置为2
                            bool = np.isin(data[:, m], dicD[dicname], invert=True)
                            fbool = (data[:, m] == fillvalue)
                        else:
                            # 连续的不在范围内置为1，填充值置为2
                            bool = ((data[:, m] < dicA[dicname][0]- 0.05 * dicA[dicname][1]) & (data[:, m] != fillvalue)) | \
                                   ((data[:, m] > dicA[dicname][1]+0.05 * dicA[dicname][1]) & (data[:, m] != fillvalue))
                            fbool = (data[:, m] == fillvalue)
                        QAFlag[:, m][bool] = 1
                        QAFlag[:, m][fbool] = 2
                o[f'Temp/QAFlag/{i}'] = QAFlag
                o[f'Temp/{i}'] = data
                # 把属性写进去
                for k in f[f'Temp/{i}'].attrs.keys():
                    o[f'Temp/{i}'].attrs[k] = f[f'/Temp/{i}'].attrs[k]

                name = []

                if datadim == 3:
                    # length = data.shape[1] * data.shape[2]
                    # for m in range(length):
                    #     name.append(i + str(m))
                    # #     每个数据集对应的每一列都存在一个param写进QAflag里面
                    # o[f'/Calibration/QAFlag/{i}'].attrs['param'] = name
                    for m in range(data.shape[1]):
                        name.append(i + str(m))
                    #     每个数据集对应的每一列都存在一个param写进QAflag里面
                    o[f'/Temp/QAFlag/{i}'].attrs['param'] = name
                else:
                    o[f'/Temp/QAFlag/{i}'].attrs['param'] = i
