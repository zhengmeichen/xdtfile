#!/usr/bin/python
# encoding:utf-8
import h5py
import sys
import glob
from collections import Counter
import numpy as np
import pickle


# def delete_fillvalue(data, fillvalue):
#     mask = d_data != fillvalue
#     mean = np.mean(d_data[mask])
#     d_data = np.where(mask, d_data, mean)


def ReadData(filelist):
    '''
    :param filelist: 输入文件列表
    :return: 所有数据集字典
    '''
    dict = {}
    for file in filelist:
        print(file)
        with h5py.File(file, 'r') as f:
            for k in f['Data'].keys():
                data = f['/Data/' + k][:]
                dims = data.ndim
                if dims == 2:
                    for i in range(data.shape[1]):
                        if k + str(i) not in dict.keys():
                            dict[k + str(i)] = data[:, i]
                        else:
                            dict[k + str(i)] = np.concatenate([dict[k + str(i)], data[:, i]])
                elif dims == 3:
                    for i in range(data.shape[1]):
                        if k + str(i) not in dict.keys():
                            dict[k + str(i)] = data[:, i]
                        else:
                            dict[k + str(i)] = np.concatenate([dict[k + str(i)], data[:, i]])
                else:
                    if k not in dict.keys():
                        dict[k] = data[:]
                    else:
                        dict[k] = np.concatenate([dict[k], data[:]])
    return dict


def CalAnalog(value):
    valuediff = np.diff(value)
    valuediff = np.append(valuediff, [valuediff[-1]])
    valuemax = np.max(value)
    valuemin = np.min(value)
    valuediffabs = abs(valuediff)
    # valuediffsort = np.argsort(valuediffabs)
    # valuediffsorted = valuediffabs[valuediffsort]
    # diffmedian = np.median(valuediffabs[valuebool])
    valuediffmedian = np.median(valuediffabs)
    valuebool = valuediffabs / (valuemax - valuemin) < (valuediffmedian / (valuemax - valuemin) + 0.05)

    sortedvalue = sorted(value[valuebool])
    finalmin = sortedvalue[0]
    finalmax = sortedvalue[-1]
    diffmedian = np.median(valuediffabs[valuebool])
    for i in sortedvalue[1:10]:
        # 判最小值
        if (i - finalmin) > 10 * diffmedian:
            finalmin = i
    for i in sortedvalue[-10:-1]:
        # 判最小值
        if (finalmax - i) > 10 * diffmedian:
            finalmax = i
    return finalmin, finalmax


if __name__ == '__main__':
    # date = sys.argv[1]
    # kind = sys.argv[2]
    date = '20221001'
    kind = 'SP'
    filelist = sorted(glob.glob(r'/FY3E/SEM/1A/%sOBC/%s/%s/*.HDF' % (kind, date[0:4], date)))
    # filelist = sorted(glob.glob(r'/FY3E/SEM/1A/%sOBC/%s/%s/FY3E_SEM--_ORBT_1A_20220113_0019_SPOBC_V0.HDF' % (kind, date[0:4], date)))
    resultA, resultD = {}, {}

    # part 0 将所有数据集均存放在字典中
    single_dict = ReadData([filelist[0]])
    oneday_dict = ReadData(filelist)

    for key, value in single_dict.items():
        # print("key",key)
        # part1 一轨中数据集均去重进行个数统计
        valuebool = value == -9999.9
        value[valuebool] = np.mean(value[~valuebool])
        value_count = Counter(value)

        # part1.1 一轨去重后的数据个数小于10
        if len(value_count.keys()) < 10:
            oneday_value = oneday_dict[key]
            oneday_valuebool = oneday_value == -9999.9
            oneday_value[oneday_valuebool] = np.mean(oneday_value[~oneday_valuebool])
            oneday_value_count = Counter(oneday_value)

            # part1.1.1 一天去重后的数据簇值小于10
            if len(oneday_value_count.keys()) < 10:
                if key not in resultD.keys():
                    Statistic = {}
                    for k, v in oneday_value_count.items():
                        Statistic[k] = float(v) / float(oneday_value.shape[0])

                    for k, v in Statistic.items():
                        if v < 0.1:
                            del oneday_value_count[k]
                    resultD[key] = oneday_value_count.keys()
                    #########此部分输出为数字量############

            # part1.1.2 一天去重后的数据簇值大于等于10
            else:
                resmin, resmax = CalAnalog(oneday_value)
                resultA[key] = [resmin, resmax]

        # part1.2 一轨去重后的数据个数大于等于10
        else:
            # 按照最值进行区间划分
            oneday_value = oneday_dict[key]
            oneday_valuebool = oneday_value == -9999.9
            oneday_value[oneday_valuebool] = np.mean(oneday_value[~oneday_valuebool])

            resmin, resmax = CalAnalog(oneday_value)

            resultA[key] = [resmin, resmax]

        outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/Param/SEM/' + date + '_SEM' + '_' + kind + '_Analog.pkl'
        outputfileD = '/STSS/FY3E_STSS/dev/AIWarning/Param/SEM/' + date + '_SEM' + '_' + kind + '_Digital.pkl'
        fA = open(outputfileA, 'wb')
        pickle.dump(resultA, fA, -1)
        fA.close()

        fD = open(outputfileD, 'wb')
        pickle.dump(resultD, fD, -1)
        fA.close()
