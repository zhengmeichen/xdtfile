# coding=utf-8
import h5py
import glob
import numpy as np
from collections import Counter
import pickle
import sys


# 读数据
def ReadData(filelist):
    '''

    :param filelist: 输入文件列表
    :return: 所有数据集字典
    '''
    dict = {}

    for eachfile in filelist:
        print(eachfile)
        with h5py.File(eachfile, 'r') as f:
            for group in f.keys():
                for k in f[group].keys():
                    data = f[group + '/' + k][:]
                    dims = data.ndim
                    if (data.shape[0] == 37) | (data.shape[0] == 38):
                        if dims == 2:
                            if group + '_' + k not in dict.keys():
                                dict[group + '_' + k] = data[:, -1].flatten()
                            else:
                                dict[group + '_' + k] = np.concatenate([dict[group + '_' + k], data[:, -1].flatten()])
                        elif dims == 3:
                            for i in range(data.shape[2]):
                                if group + '_' + k + str(i) not in dict.keys():
                                    dict[group + '_' + k + str(i)] = data[:, -1, i].flatten()
                                else:
                                    dict[group + '_' + k + str(i)] = np.concatenate(
                                        [dict[group + '_' + k + str(i)], data[:, -1, i].flatten()])
    return dict


# 数据个数统计
def judge_oneday_files(data_list):
    """
    一天数据聚类 Counter
    :param data_list: 一天的数据(除去填充值后)
    :return:该数据集中出现数据及对应频数的字典 {数值：频数}
    """
    dict = Counter(data_list)
    return dict


'''
# 计算模拟量的数值区间
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
'''


def get_count_percent(input_count, input_value):
    value_list = []
    percent_list = []
    for k, v in input_count.items():
        percent_list.append(float(v) / float(input_value.shape[0]))
        value_list.append(k)
    return value_list, percent_list


def count_filter(input_count, input_value, filter_value=0.1):
    Statistic = {}
    for k, v in input_count.items():
        Statistic[k] = float(v) / float(input_value.shape[0])
    if not max(Statistic.values()) < filter_value:
        for k, v in Statistic.items():
            if v < filter_value:
                del input_count[k]
    return input_count


def CalAnalog(value):
    value = value[~np.isnan(value)]
    valuediff = np.diff(value)
    valuediff = np.append(valuediff, [valuediff[-1]])
    valuemax = np.max(value)
    valuemin = np.min(value)
    valuediffabs = abs(valuediff)

    ####模拟量中存在数值变化基本相同的值，取valuediffmedian时如果占比最大值超过0.2，则valuediffmedian取占比最大数值，否则取真值
    diff_count = judge_oneday_files(valuediffabs)
    value_list, percent_list = get_count_percent(diff_count, valuediffabs)
    max_percent = max(percent_list)
    if max_percent < 0.2:
        # valuediffmedian = np.median(valuediffabs)
        valuediffmedian = np.median(np.unique(sorted(valuediffabs)))  # Anda
    else:
        valuediffmedian = value_list[percent_list.index(max_percent)]
    ###########################################

    # print("valuediffmedian",valuediffmedian)
    # print("valuemax",valuemax)
    # print("valuemin",valuemin)
    valuebool = valuediffabs / (valuemax - valuemin) <= (valuediffmedian / (valuemax - valuemin) + 0.05)

    ###去除掉其中所有异常值---ANDA
    # invalid_value = value[~valuebool]
    # valid_value = value[value != invalid_value[0]]
    # for iv in invalid_value:
    #     valid_value = valid_value[valid_value!=iv]
    # sortedvalue = sorted(valid_value)
    ##################

    sortedvalue = sorted(value[valuebool])
    finalmin = sortedvalue[0]
    finalmax = sortedvalue[-1]

    # diffmedian = np.median(valuediffabs[valuebool])
    # diffmedian = np.median(np.unique(valuediffabs[valuebool])) #Anda

    ####模拟量中存在数值变化基本相同的值，取valuediffmedian时如果占比最大值超过0.2，则valuediffmedian取占比最大数值，否则取真值
    diff_count = judge_oneday_files(valuediffabs)
    value_list, percent_list = get_count_percent(diff_count, valuediffabs)
    max_percent = max(percent_list)
    if max_percent < 0.2:
        # valuediffmedian = np.median(valuediffabs)
        diffmedian = np.median(np.unique(sorted(valuediffabs)))  # Anda
    else:
        diffmedian = value_list[percent_list.index(max_percent)]
    ###########################################

    # for i in sortedvalue[1:10]:
    for i in np.unique(sortedvalue)[1:10]:  # Anda
        # 判最小值
        if (i - finalmin) > 10 * diffmedian:
            finalmin = i
    # for i in sortedvalue[-10:-1]:
    for i in np.unique(sortedvalue)[-10:-1]:  # Anda
        # 判最大值
        if (finalmax - i) > 10 * diffmedian:
            finalmax = i
    return finalmin, finalmax


if __name__ == '__main__':
    date = sys.argv[1]
    filelist = sorted(glob.glob(r'/FY3E/HIRAS/1A/OBC/%s/%s/*.HDF' % (date[0:4], date)))
    resultA = {}
    resultD = {}
    # part 0 将所有数据集均存放在字典中
    dict = ReadData(filelist[:21])
    Alldict = ReadData(filelist[:])
    # part 1 将所有数据集均去重进行个数统计
    for key, value in dict.items():
        valuebool = ((value == -9999.9) | (value == 65535) | (value == 4294934528) | (value == -32768) |
                     (value == 4294967295) | (value == 255) | (value == 127) | (value == -2147483648) |
                     (value == 4294967168))
        value[valuebool] = np.mean(value[~valuebool])
        Value_Count = judge_oneday_files(value)
        # part1.1 对去重后的数据的个数
        Value_Count_key = Value_Count.keys()
        # print(Value_Count_key)
        # part1.1.1 去重后的数据个数小于10
        Alldict_Value = Alldict[key]
        Alldict_Valuebool = ((Alldict_Value == -9999.9) | (Alldict_Value == 65535) | (Alldict_Value == 4294934528) | (
                Alldict_Value == -32768) |
                             (Alldict_Value == 4294967295) | (Alldict_Value == 255) | (Alldict_Value == 127) | (
                                     Alldict_Value == -2147483648) |
                             (Alldict_Value == 4294967168))
        Alldict_Value[Alldict_Valuebool] = np.mean(Alldict_Value[~Alldict_Valuebool])

        if len(Value_Count_key) < 10:
            AllValue_Count = judge_oneday_files(Alldict_Value)
            if len(AllValue_Count.keys()) < 10:
                if key not in resultD.keys():
                    Statistic = {}
                    for k, v in AllValue_Count.items():
                        Statistic[k] = float(v) / float(Alldict_Value.shape[0])

                    for k, v in Statistic.items():
                        if v < 0.1:
                            del AllValue_Count[k]
                    resultD[key] = list(AllValue_Count.keys())

                    #########此部分输出为数字量
            else:
                resmin, resmax = CalAnalog(Alldict_Value)
                resultA[key] = [resmin, resmax]

            # print(AllValue_Count)
        else:
            # 去重个数大于10
            # 按照最值进行区间划分

            # print(key)
            resmin, resmax = CalAnalog(Alldict_Value)
            resultA[key] = [resmin, resmax]
    outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/Param/HIRAS/' + date + 'HIRAS_A.pkl'
    outputfileD = '/STSS/FY3E_STSS/dev/AIWarning/Param/HIRAS/' + date + 'HIRAS_D.pkl'
    fA = open(outputfileA, 'wb')
    dataA = pickle.dump(resultA, fA, -1)
    fA.close()

    fD = open(outputfileD, 'wb')
    dataD = pickle.dump(resultD, fD, -1)
    fD.close()

    # print("=========================================")
    # pkl_file = open(outputfileA,'rb')
    # data1 = pickle.load(pkl_file)
    # import pprint
    # pprint.pprint(data1)
