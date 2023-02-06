# -*- coding:utf-8 -*-
import h5py
import sys
import glob
import pickle
import numpy as np
import time, datetime

# 阈值范围
outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/YAML/WRADC_A.pkl'
outputfileD = '/STSS/FY3E_STSS/dev/AIWarning/YAML/WRADC_D.pkl'

# 将AD字典读入
pkl_file = open(outputfileA, 'rb')
dicA = pickle.load(pkl_file)
pkl_file = open(outputfileD, 'rb')
dicD = pickle.load(pkl_file)
# print(dicA)
# print('-------------------------------------------------')
# print(dicD)
# exit()

# filename = '/FY3E/WRAD/1A/OBC/ASCENDC/2022/20220105/FY3E_WRADC_ORBA_1A_20220105_2150_OBC--_V0.HDF'
# outfilename = '/STSS/FY3E_STSS/dev/AIWarning/Code/HDFTEST/HDF/FY3E_WRADC_ORBA_1A_20220105_2150_OBC--_V0.HDF'

if __name__ == '__main__':
    date = sys.argv[1]
    # A
    filelistA = sorted(glob.glob(r'/FY3E/WRAD/1A/OBC/ASCENDKu/%s/%s/*.HDF' % (date[0:4], date)))
    for i in filelistA:
        print(i)
        filename = i
        outfilename = '/STSS/FY3E_STSS/dev/AIWarning/HDFTEST/HDF/WRADK/ASCENDKu/' + i.split('/')[-1]
        with h5py.File(filename, 'r') as f, h5py.File(outfilename, 'w') as o:

            # PLAT时间
            DaycntA = (f['/Geolocation Fields/Daycnt'][:].astype('f4') * 24 * 60 * 60 * 1000).astype('i8')
            MscntA = (f['/Geolocation Fields/Mscnt'][:].astype('f4') / 10).astype('i8')

            fillvalueDA = f['/Geolocation Fields/Daycnt'].attrs['Fill Value']
            fillvalueMA = f['/Geolocation Fields/Mscnt'].attrs['Fill Value']

            databoolDA = DaycntA[:] != fillvalueDA
            DaycntA = DaycntA[:][databoolDA]

            databoolMA = MscntA[:] != fillvalueMA
            MscntA = MscntA[:][databoolMA]

            # RAW时间
            PackageId = f['/Data/PackageId'][:]
            DaycntB = DaycntA[PackageId].astype('i8')
            MscntB = MscntA[PackageId].astype('i8')

            # Sate时间
            DaycntC = (f['/Satellite Telemetry Data/Daycnt'][:].astype('f4') * 24 * 60 * 60 * 1000).astype('i8')
            MscntC = (f['/Satellite Telemetry Data/Mscnt'][:].astype('f4') / 10).astype('i8')

            fillvalueDC = f['/Satellite Telemetry Data/Daycnt'].attrs['Fill Value']
            fillvalueMC = f['/Satellite Telemetry Data/Mscnt'].attrs['Fill Value']

            databoolDC = DaycntC[:] != fillvalueDC
            DaycntC = DaycntC[:][databoolDC]

            databoolMC = MscntC[:] != fillvalueMC
            MscntC = MscntC[:][databoolMC]

            day_ms_A = (DaycntA + MscntA) // 1000
            set_day_ms_A = list(sorted(set(day_ms_A)))
            day_ms_B = (DaycntB + MscntB) // 1000
            set_day_ms_B = list(sorted(set(day_ms_B)))

            # Cal时间
            tmp = time.mktime(time.strptime("2000-01-01 12:00:00", '%Y-%m-%d %H:%M:%S'))
            realtimeA = np.zeros(len(set_day_ms_A), dtype='S40')
            for i in range(len(set_day_ms_A)):
                # print(set_day_ms_A[i])
                realtimeA[i] = datetime.datetime.fromtimestamp(set_day_ms_A[i] + tmp).strftime(
                    '%Y-%m-%d %H:%M:%S')
            o['/Calibration Fields/packagetime'] = realtimeA
            # Raw时间
            tmp = time.mktime(time.strptime("2000-01-01 12:00:00", '%Y-%m-%d %H:%M:%S'))
            realtimeB = np.zeros(len(set_day_ms_B), dtype='S40')
            for i in range(len(set_day_ms_B)):
                realtimeB[i] = datetime.datetime.fromtimestamp(set_day_ms_B[i] + tmp).strftime(
                    '%Y-%m-%d %H:%M:%S')
            o['/Raw/packagetime'] = realtimeB
            # sate时间
            tmp = time.mktime(time.strptime("2000-01-01 12:00:00", '%Y-%m-%d %H:%M:%S'))
            realtimeC = np.zeros((DaycntC.shape), dtype='S40')
            for i in range(DaycntC.shape[0]):
                realtimeC[i] = datetime.datetime.fromtimestamp(
                    (DaycntC[i] + MscntC[i]) / 1000 + tmp).strftime(
                    '%Y-%m-%d %H:%M:%S')
            o['/Satellite Telemetry Data/packagetime'] = realtimeC

            # sate
            for i in f['Satellite Telemetry Data'].keys():
                if 'cnt' not in i:
                    datadim = f['Satellite Telemetry Data/' + i].ndim
                    data = f['Satellite Telemetry Data/' + i][:][databoolMC]
                    fillvalue = f['Satellite Telemetry Data/' + i].attrs['Fill Value']
                    if datadim == 1:
                        QAFlag = np.zeros((len(DaycntC)), dtype='u2')
                        # 阈值名称
                        dicname = f'Satellite Telemetry Data_{i}'
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
                            dicname = f'Satellite Telemetry Data_{i}{m}'
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

                    o[f'Satellite Telemetry Data/QAFlag/{i}'] = QAFlag
                    o[f'Satellite Telemetry Data/{i}'] = data
                    # 把属性写进去
                    for k in f[f'Satellite Telemetry Data/{i}'].attrs.keys():
                        o[f'Satellite Telemetry Data/{i}'].attrs[k] = f[f'Satellite Telemetry Data/{i}'].attrs[k]

                    name = []
                    if datadim == 2:
                        for m in range(data.shape[1]):
                            name.append(i + str(m))
                        #     每个数据集对应的每一列都存在一个param写进QAflag里面
                        o[f'Satellite Telemetry Data/QAFlag/{i}'].attrs['param'] = name
                    else:
                        o[f'Satellite Telemetry Data/QAFlag/{i}'].attrs['param'] = i

            for i in f['Calibration Fields'].keys():
                datadim = f['Calibration Fields/' + i].ndim
                data = f['Calibration Fields/' + i][:]
                if 'Workstatus' in i:
                    fillvalue = None
                else:
                    fillvalue = f['Calibration Fields/' + i].attrs['Fill Value']
                if 'Raw' not in i:
                    if datadim == 1:
                        QAFlag = np.zeros((len(set_day_ms_A)), dtype='u2')
                        outvalue = np.zeros((len(set_day_ms_A)), dtype='f4')
                        # 阈值名称
                        dicname = f'Calibration Fields_{i}'
                        count = 0
                        for x in set_day_ms_A:
                            timetmp = np.isin(day_ms_A, x)
                            datasetvalue = np.nanmax(abs(data[timetmp]))
                            outvalue[count] = datasetvalue
                            count += 1

                        if dicname in dicD.keys():
                            # 全false
                            # print(dicD[dicDname], type(dicD[dicDname]))
                            # 离散的不在范围内置为1，填充值置为2
                            bool = np.isin(outvalue, dicD[dicname], invert=True)
                            fbool = (outvalue == fillvalue)

                        else:
                            # 连续的不在范围内置为1，填充值置为2
                            bool = ((outvalue < dicA[dicname][0] - 0.05 * dicA[dicname][1]) & (outvalue != fillvalue)) | \
                                   ((outvalue > dicA[dicname][1] + 0.05 * dicA[dicname][1]) & (outvalue != fillvalue))
                            fbool = (outvalue == fillvalue)

                        # print(i, len(bool), bool)
                        # exit()
                        QAFlag[bool] = 1
                        QAFlag[fbool] = 2
                        o[f'Calibration Fields/QAFlag/{i}'] = QAFlag
                        o[f'Calibration Fields/{i}'] = outvalue

                    elif datadim == 2:
                        QAFlag = np.zeros((len(set_day_ms_A), data.shape[1]), dtype='u2')
                        outvalue = np.zeros((len(set_day_ms_A), data.shape[1]), dtype='f4')

                        count = 0
                        for x in set_day_ms_A:
                            timetmp = np.isin(day_ms_A, x)
                            datasetvalue = np.argmax(abs(data[timetmp, :]), axis=0)
                            for dd in range(len(datasetvalue)):
                                outvalue[count, dd] = data[datasetvalue[dd], dd]
                            count += 1

                        for m in range(data.shape[1]):
                            # 阈值名称
                            dicname = f'Calibration Fields_{i}{m}'
                            if dicname in dicD.keys():
                                # 全false
                                # print(dicD[dicDname], type(dicD[dicDname]))
                                # 离散的不在范围内置为1，填充值置为2
                                bool = np.isin(outvalue[:, m], dicD[dicname], invert=True)
                                fbool = (outvalue[:, m] == fillvalue)

                            else:
                                # 连续的不在范围内置为1，填充值置为2
                                bool = ((outvalue[:, m] < dicA[dicname][0] - 0.05 * dicA[dicname][1]) & (
                                        outvalue[:, m] != fillvalue)) | \
                                       ((outvalue[:, m] > dicA[dicname][1] + 0.05 * dicA[dicname][1]) & (
                                               outvalue[:, m] != fillvalue))
                                fbool = (outvalue[:, m] == fillvalue)

                            QAFlag[:, m][bool] = 1
                            QAFlag[:, m][fbool] = 2
                        o[f'Calibration Fields/QAFlag/{i}'] = QAFlag
                        o[f'Calibration Fields/{i}'] = outvalue
                    # 把属性写进去
                    for k in f[f'Calibration Fields/{i}'].attrs.keys():
                        o[f'Calibration Fields/{i}'].attrs[k] = f[f'Calibration Fields/{i}'].attrs[k]

                    name = []
                    if datadim == 2:
                        for m in range(data.shape[1]):
                            name.append(i + str(m))
                        #     每个数据集对应的每一列都存在一个param写进QAflag里面
                        o[f'/Calibration Fields/QAFlag/{i}'].attrs['param'] = name
                    else:
                        o[f'/Calibration Fields/QAFlag/{i}'].attrs['param'] = i

                # Raw
                else:
                    if datadim == 1:
                        QAFlag = np.zeros((len(set_day_ms_B)), dtype='u2')
                        outvalue = np.zeros((len(set_day_ms_B)), dtype='f4')
                        # 阈值名称
                        dicname = f'Calibration Fields_{i}'
                        count = 0
                        for x in set_day_ms_B:
                            timetmp = np.isin(day_ms_B, x)
                            datasetvalue = np.argmax(abs(data[timetmp]))
                            outvalue[count] = data[datasetvalue]
                            count += 1

                        if dicname in dicD.keys():
                            # 全false
                            # print(dicD[dicDname], type(dicD[dicDname]))
                            # 离散的不在范围内置为1，填充值置为2
                            bool = np.isin(outvalue, dicD[dicname], invert=True)
                            fbool = (outvalue == fillvalue)

                        else:
                            # 连续的不在范围内置为1，填充值置为2
                            bool = ((outvalue < dicA[dicname][0] - 0.05 * dicA[dicname][1]) & (outvalue != fillvalue)) | \
                                   ((outvalue > dicA[dicname][1] + 0.05 * dicA[dicname][1]) & (outvalue != fillvalue))
                            fbool = (outvalue == fillvalue)

                        # print(i, len(bool), bool)
                        # exit()
                        QAFlag[bool] = 1
                        QAFlag[fbool] = 2
                        o[f'Raw/QAFlag/{i}'] = QAFlag
                        o[f'Raw/{i}'] = outvalue

                    elif datadim == 2:
                        QAFlag = np.zeros((len(set_day_ms_B), data.shape[1]), dtype='u2')
                        outvalue = np.zeros((len(set_day_ms_B), data.shape[1]), dtype='f4')

                        count = 0
                        for x in set_day_ms_B:
                            timetmp = np.isin(day_ms_B, x)
                            datasetvalue = np.argmax(abs(data[timetmp, :]), axis=0)
                            for dd in range(len(datasetvalue)):
                                outvalue[count, dd] = data[datasetvalue[dd], dd]

                            count += 1

                        for m in range(data.shape[1]):
                            # 阈值名称
                            dicname = f'Calibration Fields_{i}{m}'
                            if dicname in dicD.keys():
                                # 全false
                                # print(dicD[dicDname], type(dicD[dicDname]))
                                # 离散的不在范围内置为1，填充值置为2
                                bool = np.isin(outvalue[:, m], dicD[dicname], invert=True)
                                fbool = (outvalue[:, m] == fillvalue)

                            else:
                                # 连续的不在范围内置为1，填充值置为2
                                bool = ((outvalue[:, m] < dicA[dicname][0] - 0.05 * dicA[dicname][1]) & (
                                        outvalue[:, m] != fillvalue)) | \
                                       ((outvalue[:, m] > dicA[dicname][1] + 0.05 * dicA[dicname][1]) & (
                                               outvalue[:, m] != fillvalue))
                                fbool = (outvalue[:, m] == fillvalue)

                            QAFlag[:, m][bool] = 1
                            QAFlag[:, m][fbool] = 2
                        o[f'Raw/QAFlag/{i}'] = QAFlag
                        o[f'Raw/{i}'] = outvalue
                    # 把属性写进去
                    for k in f[f'Calibration Fields/{i}'].attrs.keys():
                        o[f'Raw/{i}'].attrs[k] = f[f'Calibration Fields/{i}'].attrs[k]

                    name = []
                    if datadim == 2:
                        for m in range(data.shape[1]):
                            name.append(i + str(m))
                        #     每个数据集对应的每一列都存在一个param写进QAflag里面
                        o[f'/Raw/QAFlag/{i}'].attrs['param'] = name
                    else:
                        o[f'/Raw/QAFlag/{i}'].attrs['param'] = i

            for i in f['Data'].keys():
                datadim = f['Data/' + i].ndim
                data = f['Data/' + i][:]
                if 'PackageId' in i or 'packagetime' in i:
                    fillvalue = None
                else:
                    fillvalue = f['Data/' + i].attrs['Fill Value']
                if 'PackageId' in i or 'packagetime' in i:
                    pass
                else:
                    if datadim == 1:
                        QAFlag = np.zeros((len(set_day_ms_A)), dtype='u2')
                        outvalue = np.zeros((len(set_day_ms_A)), dtype='f4')
                        # 阈值名称
                        dicname = f'Data_{i}'
                        count = 0
                        for x in set_day_ms_A:
                            timetmp = np.isin(day_ms_A, x)
                            datasetvalue = np.argmax(abs(data[timetmp]))
                            outvalue[count] = data[datasetvalue]
                            count += 1

                        if dicname in dicD.keys():
                            # 全false
                            # print(dicD[dicDname], type(dicD[dicDname]))
                            # 离散的不在范围内置为1，填充值置为2
                            bool = np.isin(outvalue, dicD[dicname], invert=True)
                            fbool = (outvalue == fillvalue)

                        else:
                            # 连续的不在范围内置为1，填充值置为2
                            bool = ((outvalue < dicA[dicname][0] - 0.05 * dicA[dicname][1]) & (outvalue != fillvalue)) | \
                                   ((outvalue > dicA[dicname][1] + 0.05 * dicA[dicname][1]) & (outvalue != fillvalue))
                            fbool = (outvalue == fillvalue)

                        # print(i, len(bool), bool)
                        # exit()
                        QAFlag[bool] = 1
                        QAFlag[fbool] = 2
                        o[f'Calibration Fields/QAFlag/{i}'] = QAFlag
                        o[f'Calibration Fields/{i}'] = outvalue

                    elif datadim == 2:
                        QAFlag = np.zeros((len(set_day_ms_A), data.shape[1]), dtype='u2')
                        outvalue = np.zeros((len(set_day_ms_A), data.shape[1]), dtype='f4')

                        count = 0
                        for x in set_day_ms_A:
                            timetmp = np.isin(day_ms_A, x)
                            datasetvalue = np.argmax(abs(data[timetmp, :]), axis=0)
                            for dd in range(len(datasetvalue)):
                                outvalue[count, dd] = data[datasetvalue[dd], dd]
                            count += 1

                        for m in range(data.shape[1]):
                            # 阈值名称
                            dicname = f'Data_{i}{m}'
                            if dicname in dicD.keys():
                                # 全false
                                # print(dicD[dicDname], type(dicD[dicDname]))
                                # 离散的不在范围内置为1，填充值置为2
                                bool = np.isin(outvalue[:, m], dicD[dicname], invert=True)
                                fbool = (outvalue[:, m] == fillvalue)

                            else:
                                # 连续的不在范围内置为1，填充值置为2
                                bool = ((outvalue[:, m] < dicA[dicname][0] - 0.05 * dicA[dicname][1]) & (
                                        outvalue[:, m] != fillvalue)) | \
                                       ((outvalue[:, m] > dicA[dicname][1] + 0.05 * dicA[dicname][1]) & (
                                               outvalue[:, m] != fillvalue))
                                fbool = (outvalue[:, m] == fillvalue)

                            QAFlag[:, m][bool] = 1
                            QAFlag[:, m][fbool] = 2
                        o[f'Calibration Fields/QAFlag/{i}'] = QAFlag
                        o[f'Calibration Fields/{i}'] = outvalue

                    # 把属性写进去
                    for k in f[f'Data/{i}'].attrs.keys():
                        o[f'Calibration Fields/{i}'].attrs[k] = f[f'Data/{i}'].attrs[k]

                    name = []
                    if datadim == 2:
                        for m in range(data.shape[1]):
                            name.append(i + str(m))
                        #     每个数据集对应的每一列都存在一个param写进QAflag里面
                        o[f'/Calibration Fields/QAFlag/{i}'].attrs['param'] = name
                    else:
                        o[f'/Calibration Fields/QAFlag/{i}'].attrs['param'] = i

    # D
    filelistD = sorted(glob.glob(r'/FY3E/WRAD/1A/OBC/DESCENDKu/%s/%s/*.HDF' % (date[0:4], date)))
    for i in filelistD:
        print(i)
        filename = i
        outfilename = '/STSS/FY3E_STSS/dev/AIWarning/HDFTEST/HDF/WRADK/DESCENDKu/' + i.split('/')[-1]
        with h5py.File(filename, 'r') as f, h5py.File(outfilename, 'w') as o:
            # PLAT时间
            DaycntA = (f['/Geolocation Fields/Daycnt'][:].astype('f4') * 24 * 60 * 60 * 1000).astype('i8')
            MscntA = (f['/Geolocation Fields/Mscnt'][:].astype('f4') / 10).astype('i8')

            fillvalueDA = f['/Geolocation Fields/Daycnt'].attrs['Fill Value']
            fillvalueMA = f['/Geolocation Fields/Mscnt'].attrs['Fill Value']

            databoolDA = DaycntA[:] != fillvalueDA
            DaycntA = DaycntA[:][databoolDA]

            databoolMA = MscntA[:] != fillvalueMA
            MscntA = MscntA[:][databoolMA]

            # RAW时间
            PackageId = f['/Data/PackageId'][:]
            DaycntB = DaycntA[PackageId].astype('i8')
            MscntB = MscntA[PackageId].astype('i8')

            # Sate时间
            DaycntC = (f['/Satellite Telemetry Data/Daycnt'][:].astype('f4') * 24 * 60 * 60 * 1000).astype('i8')
            MscntC = (f['/Satellite Telemetry Data/Mscnt'][:].astype('f4') / 10).astype('i8')

            fillvalueDC = f['/Satellite Telemetry Data/Daycnt'].attrs['Fill Value']
            fillvalueMC = f['/Satellite Telemetry Data/Mscnt'].attrs['Fill Value']

            databoolDC = DaycntC[:] != fillvalueDC
            DaycntC = DaycntC[:][databoolDC]

            databoolMC = MscntC[:] != fillvalueMC
            MscntC = MscntC[:][databoolMC]

            day_ms_A = (DaycntA + MscntA) // 1000
            set_day_ms_A = list(sorted(set(day_ms_A)))
            day_ms_B = (DaycntB + MscntB) // 1000
            set_day_ms_B = list(sorted(set(day_ms_B)))

            # Cal时间
            tmp = time.mktime(time.strptime("2000-01-01 12:00:00", '%Y-%m-%d %H:%M:%S'))
            realtimeA = np.zeros(len(set_day_ms_A), dtype='S40')
            for i in range(len(set_day_ms_A)):
                # print(set_day_ms_A[i])
                realtimeA[i] = datetime.datetime.fromtimestamp(set_day_ms_A[i] + tmp).strftime(
                    '%Y-%m-%d %H:%M:%S')
            o['/Calibration Fields/packagetime'] = realtimeA
            # Raw时间
            tmp = time.mktime(time.strptime("2000-01-01 12:00:00", '%Y-%m-%d %H:%M:%S'))
            realtimeB = np.zeros(len(set_day_ms_B), dtype='S40')
            for i in range(len(set_day_ms_B)):
                realtimeB[i] = datetime.datetime.fromtimestamp(set_day_ms_B[i] + tmp).strftime(
                    '%Y-%m-%d %H:%M:%S')
            o['/Raw/packagetime'] = realtimeB
            # sate时间
            tmp = time.mktime(time.strptime("2000-01-01 12:00:00", '%Y-%m-%d %H:%M:%S'))
            realtimeC = np.zeros((DaycntC.shape), dtype='S40')
            for i in range(DaycntC.shape[0]):
                realtimeC[i] = datetime.datetime.fromtimestamp(
                    (DaycntC[i] + MscntC[i]) / 1000 + tmp).strftime(
                    '%Y-%m-%d %H:%M:%S')
            o['/Satellite Telemetry Data/packagetime'] = realtimeC

            # sate
            for i in f['Satellite Telemetry Data'].keys():
                if 'cnt' not in i:
                    datadim = f['Satellite Telemetry Data/' + i].ndim
                    data = f['Satellite Telemetry Data/' + i][:][databoolMC]
                    fillvalue = f['Satellite Telemetry Data/' + i].attrs['Fill Value']
                    if datadim == 1:
                        QAFlag = np.zeros((len(DaycntC)), dtype='u2')
                        # 阈值名称
                        dicname = f'Satellite Telemetry Data_{i}'
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
                            dicname = f'Satellite Telemetry Data_{i}{m}'
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

                    o[f'Satellite Telemetry Data/QAFlag/{i}'] = QAFlag
                    o[f'Satellite Telemetry Data/{i}'] = data
                    # 把属性写进去
                    for k in f[f'Satellite Telemetry Data/{i}'].attrs.keys():
                        o[f'Satellite Telemetry Data/{i}'].attrs[k] = f[f'Satellite Telemetry Data/{i}'].attrs[k]

                    name = []
                    if datadim == 2:
                        for m in range(data.shape[1]):
                            name.append(i + str(m))
                        #     每个数据集对应的每一列都存在一个param写进QAflag里面
                        o[f'Satellite Telemetry Data/QAFlag/{i}'].attrs['param'] = name
                    else:
                        o[f'Satellite Telemetry Data/QAFlag/{i}'].attrs['param'] = i

            for i in f['Calibration Fields'].keys():
                datadim = f['Calibration Fields/' + i].ndim
                data = f['Calibration Fields/' + i][:]
                if 'Workstatus' in i:
                    fillvalue = None
                else:
                    fillvalue = f['Calibration Fields/' + i].attrs['Fill Value']
                if 'Raw' not in i:
                    if datadim == 1:
                        QAFlag = np.zeros((len(set_day_ms_A)), dtype='u2')
                        outvalue = np.zeros((len(set_day_ms_A)), dtype='f4')
                        # 阈值名称
                        dicname = f'Calibration Fields_{i}'
                        count = 0
                        for x in set_day_ms_A:
                            timetmp = np.isin(day_ms_A, x)
                            datasetvalue = np.nanmax(abs(data[timetmp]))
                            outvalue[count] = datasetvalue
                            count += 1

                        if dicname in dicD.keys():
                            # 全false
                            # print(dicD[dicDname], type(dicD[dicDname]))
                            # 离散的不在范围内置为1，填充值置为2
                            bool = np.isin(outvalue, dicD[dicname], invert=True)
                            fbool = (outvalue == fillvalue)

                        else:
                            # 连续的不在范围内置为1，填充值置为2
                            bool = ((outvalue < dicA[dicname][0] - 0.05 * dicA[dicname][1]) & (outvalue != fillvalue)) | \
                                   ((outvalue > dicA[dicname][1] + 0.05 * dicA[dicname][1]) & (outvalue != fillvalue))
                            fbool = (outvalue == fillvalue)

                        # print(i, len(bool), bool)
                        # exit()
                        QAFlag[bool] = 1
                        QAFlag[fbool] = 2
                        o[f'Calibration Fields/QAFlag/{i}'] = QAFlag
                        o[f'Calibration Fields/{i}'] = outvalue

                    elif datadim == 2:
                        QAFlag = np.zeros((len(set_day_ms_A), data.shape[1]), dtype='u2')
                        outvalue = np.zeros((len(set_day_ms_A), data.shape[1]), dtype='f4')

                        count = 0
                        for x in set_day_ms_A:
                            timetmp = np.isin(day_ms_A, x)
                            datasetvalue = np.argmax(abs(data[timetmp, :]), axis=0)
                            for dd in range(len(datasetvalue)):
                                outvalue[count, dd] = data[datasetvalue[dd], dd]
                            count += 1

                        for m in range(data.shape[1]):
                            # 阈值名称
                            dicname = f'Calibration Fields_{i}{m}'
                            if dicname in dicD.keys():
                                # 全false
                                # print(dicD[dicDname], type(dicD[dicDname]))
                                # 离散的不在范围内置为1，填充值置为2
                                bool = np.isin(outvalue[:, m], dicD[dicname], invert=True)
                                fbool = (outvalue[:, m] == fillvalue)

                            else:
                                # 连续的不在范围内置为1，填充值置为2
                                bool = ((outvalue[:, m] < dicA[dicname][0] - 0.05 * dicA[dicname][1]) & (
                                        outvalue[:, m] != fillvalue)) | \
                                       ((outvalue[:, m] > dicA[dicname][1] + 0.05 * dicA[dicname][1]) & (
                                               outvalue[:, m] != fillvalue))
                                fbool = (outvalue[:, m] == fillvalue)

                            QAFlag[:, m][bool] = 1
                            QAFlag[:, m][fbool] = 2
                        o[f'Calibration Fields/QAFlag/{i}'] = QAFlag
                        o[f'Calibration Fields/{i}'] = outvalue
                    # 把属性写进去
                    for k in f[f'Calibration Fields/{i}'].attrs.keys():
                        o[f'Calibration Fields/{i}'].attrs[k] = f[f'Calibration Fields/{i}'].attrs[k]

                    name = []
                    if datadim == 2:
                        for m in range(data.shape[1]):
                            name.append(i + str(m))
                        #     每个数据集对应的每一列都存在一个param写进QAflag里面
                        o[f'/Calibration Fields/QAFlag/{i}'].attrs['param'] = name
                    else:
                        o[f'/Calibration Fields/QAFlag/{i}'].attrs['param'] = i

                # Raw
                else:
                    if datadim == 1:
                        QAFlag = np.zeros((len(set_day_ms_B)), dtype='u2')
                        outvalue = np.zeros((len(set_day_ms_B)), dtype='f4')
                        # 阈值名称
                        dicname = f'Calibration Fields_{i}'
                        count = 0
                        for x in set_day_ms_B:
                            timetmp = np.isin(day_ms_B, x)
                            datasetvalue = np.argmax(abs(data[timetmp]))
                            outvalue[count] = data[datasetvalue]
                            count += 1

                        if dicname in dicD.keys():
                            # 全false
                            # print(dicD[dicDname], type(dicD[dicDname]))
                            # 离散的不在范围内置为1，填充值置为2
                            bool = np.isin(outvalue, dicD[dicname], invert=True)
                            fbool = (outvalue == fillvalue)

                        else:
                            # 连续的不在范围内置为1，填充值置为2
                            bool = ((outvalue < dicA[dicname][0] - 0.05 * dicA[dicname][1]) & (outvalue != fillvalue)) | \
                                   ((outvalue > dicA[dicname][1] + 0.05 * dicA[dicname][1]) & (outvalue != fillvalue))
                            fbool = (outvalue == fillvalue)

                        # print(i, len(bool), bool)
                        # exit()
                        QAFlag[bool] = 1
                        QAFlag[fbool] = 2
                        o[f'Raw/QAFlag/{i}'] = QAFlag
                        o[f'Raw/{i}'] = outvalue

                    elif datadim == 2:
                        QAFlag = np.zeros((len(set_day_ms_B), data.shape[1]), dtype='u2')
                        outvalue = np.zeros((len(set_day_ms_B), data.shape[1]), dtype='f4')

                        count = 0
                        for x in set_day_ms_B:
                            timetmp = np.isin(day_ms_B, x)
                            datasetvalue = np.argmax(abs(data[timetmp, :]), axis=0)
                            for dd in range(len(datasetvalue)):
                                outvalue[count, dd] = data[datasetvalue[dd], dd]

                            count += 1

                        for m in range(data.shape[1]):
                            # 阈值名称
                            dicname = f'Calibration Fields_{i}{m}'
                            if dicname in dicD.keys():
                                # 全false
                                # print(dicD[dicDname], type(dicD[dicDname]))
                                # 离散的不在范围内置为1，填充值置为2
                                bool = np.isin(outvalue[:, m], dicD[dicname], invert=True)
                                fbool = (outvalue[:, m] == fillvalue)

                            else:
                                # 连续的不在范围内置为1，填充值置为2
                                bool = ((outvalue[:, m] < dicA[dicname][0] - 0.05 * dicA[dicname][1]) & (
                                        outvalue[:, m] != fillvalue)) | \
                                       ((outvalue[:, m] > dicA[dicname][1] + 0.05 * dicA[dicname][1]) & (
                                               outvalue[:, m] != fillvalue))
                                fbool = (outvalue[:, m] == fillvalue)

                            QAFlag[:, m][bool] = 1
                            QAFlag[:, m][fbool] = 2
                        o[f'Raw/QAFlag/{i}'] = QAFlag
                        o[f'Raw/{i}'] = outvalue
                    # 把属性写进去
                    for k in f[f'Calibration Fields/{i}'].attrs.keys():
                        o[f'Raw/{i}'].attrs[k] = f[f'Calibration Fields/{i}'].attrs[k]

                    name = []
                    if datadim == 2:
                        for m in range(data.shape[1]):
                            name.append(i + str(m))
                        #     每个数据集对应的每一列都存在一个param写进QAflag里面
                        o[f'/Raw/QAFlag/{i}'].attrs['param'] = name
                    else:
                        o[f'/Raw/QAFlag/{i}'].attrs['param'] = i

            for i in f['Data'].keys():
                datadim = f['Data/' + i].ndim
                data = f['Data/' + i][:]
                if 'PackageId' in i or 'packagetime' in i:
                    fillvalue = None
                else:
                    fillvalue = f['Data/' + i].attrs['Fill Value']
                if 'PackageId' in i or 'packagetime' in i:
                    pass
                else:
                    if datadim == 1:
                        QAFlag = np.zeros((len(set_day_ms_A)), dtype='u2')
                        outvalue = np.zeros((len(set_day_ms_A)), dtype='f4')
                        # 阈值名称
                        dicname = f'Data_{i}'
                        count = 0
                        for x in set_day_ms_A:
                            timetmp = np.isin(day_ms_A, x)
                            datasetvalue = np.argmax(abs(data[timetmp]))
                            outvalue[count] = data[datasetvalue]
                            count += 1

                        if dicname in dicD.keys():
                            # 全false
                            # print(dicD[dicDname], type(dicD[dicDname]))
                            # 离散的不在范围内置为1，填充值置为2
                            bool = np.isin(outvalue, dicD[dicname], invert=True)
                            fbool = (outvalue == fillvalue)

                        else:
                            # 连续的不在范围内置为1，填充值置为2
                            bool = ((outvalue < dicA[dicname][0] - 0.05 * dicA[dicname][1]) & (outvalue != fillvalue)) | \
                                   ((outvalue > dicA[dicname][1] + 0.05 * dicA[dicname][1]) & (outvalue != fillvalue))
                            fbool = (outvalue == fillvalue)

                        # print(i, len(bool), bool)
                        # exit()
                        QAFlag[bool] = 1
                        QAFlag[fbool] = 2
                        o[f'Calibration Fields/QAFlag/{i}'] = QAFlag
                        o[f'Calibration Fields/{i}'] = outvalue

                    elif datadim == 2:
                        QAFlag = np.zeros((len(set_day_ms_A), data.shape[1]), dtype='u2')
                        outvalue = np.zeros((len(set_day_ms_A), data.shape[1]), dtype='f4')

                        count = 0
                        for x in set_day_ms_A:
                            timetmp = np.isin(day_ms_A, x)
                            datasetvalue = np.argmax(abs(data[timetmp, :]), axis=0)
                            for dd in range(len(datasetvalue)):
                                outvalue[count, dd] = data[datasetvalue[dd], dd]
                            count += 1

                        for m in range(data.shape[1]):
                            # 阈值名称
                            dicname = f'Data_{i}{m}'
                            if dicname in dicD.keys():
                                # 全false
                                # print(dicD[dicDname], type(dicD[dicDname]))
                                # 离散的不在范围内置为1，填充值置为2
                                bool = np.isin(outvalue[:, m], dicD[dicname], invert=True)
                                fbool = (outvalue[:, m] == fillvalue)

                            else:
                                # 连续的不在范围内置为1，填充值置为2
                                bool = ((outvalue[:, m] < dicA[dicname][0] - 0.05 * dicA[dicname][1]) & (
                                        outvalue[:, m] != fillvalue)) | \
                                       ((outvalue[:, m] > dicA[dicname][1] + 0.05 * dicA[dicname][1]) & (
                                               outvalue[:, m] != fillvalue))
                                fbool = (outvalue[:, m] == fillvalue)

                            QAFlag[:, m][bool] = 1
                            QAFlag[:, m][fbool] = 2
                        o[f'Calibration Fields/QAFlag/{i}'] = QAFlag
                        o[f'Calibration Fields/{i}'] = outvalue

                    # 把属性写进去
                    for k in f[f'Data/{i}'].attrs.keys():
                        o[f'Calibration Fields/{i}'].attrs[k] = f[f'Data/{i}'].attrs[k]

                    name = []
                    if datadim == 2:
                        for m in range(data.shape[1]):
                            name.append(i + str(m))
                        #     每个数据集对应的每一列都存在一个param写进QAflag里面
                        o[f'/Calibration Fields/QAFlag/{i}'].attrs['param'] = name
                    else:
                        o[f'/Calibration Fields/QAFlag/{i}'].attrs['param'] = i
