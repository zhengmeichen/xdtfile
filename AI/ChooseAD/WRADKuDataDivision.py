# coding=utf-8
import h5py
import glob
import numpy as np
from collections import Counter
import pickle
import sys
import os


# 读数据
def ReadData(filelist):
    '''

    :param filelist: 输入文件列表
    :return: 所有数据集字典
    '''
    dict = {}

    for eachfile in filelist:
        try:
            print(eachfile)
            with h5py.File(eachfile, 'r') as f:
                for group in f.keys():
                    for k in f[group].keys():
                        # group = group.encode('utf-8')
                        # k = k.encode('utf-8')
                        data = f[group + '/' + k][()]
                        try:
                            fillvalue = f[group + '/' + k].attrs['Fill Value']
                        except:
                            fillvalue = 999999
                        # print("fillvalue",group + '/' + k,fillvalue)
                        if (isinstance(fillvalue, np.ndarray)):
                            fillvalue = fillvalue[0]
                        dims = data.ndim
                        if dims == 1:
                            if group + '_' + k not in dict.keys():
                                # 去除数据中的填充值在放入字典
                                databool = data[:].flatten() != fillvalue
                                dict[group + '_' + k] = data[:].flatten()[databool]

                            else:
                                databool = data[:].flatten() != fillvalue
                                dict[group + '_' + k] = np.concatenate(
                                    [dict[group + '_' + k], data[:].flatten()[databool]])
                        elif dims == 2:
                            # if data.shape[0] < data.shape[1]:
                            #     data = data.T
                            for i in range(data.shape[1]):
                                if group + '_' + k + str(i) not in dict.keys():
                                    databool = data[:, i].flatten() != fillvalue
                                    dict[group + '_' + k + str(i)] = data[:, i].flatten()[databool]
                                else:
                                    databool = data[:, i].flatten() != fillvalue
                                    dict[group + '_' + k + str(i)] = np.concatenate(
                                        [dict[group + '_' + k + str(i)], data[:, i].flatten()[databool]])

        except:
            continue
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


# 计算模拟量的数值区间
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


# 用Kmeans聚类方法计算模拟量的数值区间
def CalKMeans(value):
    from sklearn.cluster import KMeans

    value = value[~np.isnan(value)]
    kmeans = KMeans(n_clusters=2, random_state=10000).fit(value[:, np.newaxis])
    labels = np.array(kmeans.labels_)

    labels_count = judge_oneday_files(labels)

    value_valid = value[labels == 1]
    finalmin = np.min(value_valid)
    finalmax = np.max(value_valid)
    return finalmin, finalmax


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


if __name__ == '__main__':

    # date = sys.argv[1]
    # filelist = sorted(glob.glob(r'/FY3E/GNOS/1A/OBC/%s/%s/*.HDF' % (date[0:4], date)))
    # filelist = sorted(glob.glob('/FY3E/GNOS/1A/OBC/2022/20220401/FY3E_GNOS-_ORBT_1A_20220401_*_OBC--_V0.HDF'))

    # date = '20220322'
    date = sys.argv[1]
    file_re = '/FY3E/WRAD/1A/OBC/*Ku/' + date[0:4] + '/' + date + '/FY3E_WRADK_ORB*_1A_*_OBC--_V0.HDF'
    out_root = '/STSS/FY3E_STSS/dev/AIWarning/Param/WRAD/WRADK/'
    os.makedirs(out_root, exist_ok=True)
    filelist = sorted(glob.glob(file_re))

    resultA = {}
    resultD = {}
    # part 0 将所有数据集均存放在字典中
    dict = ReadData(filelist[:5])
    Alldict = ReadData(filelist)
    # part 1 将所有数据集均去重进行个数统计
    for key, value in dict.items():
        # if key != 'Calibration Fields_Raw_DN_Signal265':
        #     continue
        try:
            Value_Count = judge_oneday_files(value)

            # part1.1 对去重后的数据的个数
            Value_Count_key = Value_Count.keys()
            # print(Value_Count_key)
            # part1.1.1 去重后的数据个数小于10
            Alldict_Value = Alldict[key]

            if len(Value_Count_key) < 10:
                AllValue_Count = judge_oneday_files(Alldict_Value)
                if len(AllValue_Count.keys()) < 10:
                    if key not in resultD.keys():
                        AllValue_Count = count_filter(AllValue_Count, Alldict_Value)
                        resultD[key] = list(AllValue_Count.keys())

                        #########此部分输出为数字量
                else:
                    # print("====142=====key===",key)
                    resmin, resmax = CalAnalog(Alldict_Value)
                    # resmin, resmax = CalKMeans(Alldict_Value)
                    resultA[key] = [resmin, resmax]

                # print(AllValue_Count)
            else:
                # 去重个数大于10
                # 按照最值进行区间划分

                # print(key)
                # print("====152=====key===", key)
                resmin, resmax = CalAnalog(Alldict_Value)
                # resmin, resmax = CalKMeans(Alldict_Value)
                resultA[key] = [resmin, resmax]
        except:
            print('Error-->' + key)
    # outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/Param/GNOS/' + date + 'GNOS_A.pkl'
    # outputfileD = '/STSS/FY3E_STSS/dev/AIWarning/Param/GNOS/' + date + 'GNOS_D.pkl'
    outputfileA = out_root + date + 'WRAD_A.pkl'
    outputfileD = out_root + date + 'WRAD_D.pkl'
    fA = open(outputfileA, 'wb')
    data = pickle.dump(resultA, fA, -1)
    fA.close()

    fD = open(outputfileD, 'wb')
    data1 = pickle.dump(resultD, fD, -1)
    fD.close()

    print("=========================================")
    pkl_file = open(outputfileA, 'rb')
    data2 = pickle.load(pkl_file)
    import pprint

    pprint.pprint(data2)

    print("=========================================")
    pkl_file = open(outputfileD, 'rb')
    data3 = pickle.load(pkl_file)
    import pprint

    pprint.pprint(data3)
