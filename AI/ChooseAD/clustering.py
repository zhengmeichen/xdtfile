# coding=utf-8
import h5py
import sys
import time
import glob
import csv
import numpy as np
from sklearn.cluster import DBSCAN
from collections import Counter
import matplotlib.pyplot as plt

plt.switch_backend('agg')


def Normalize(array):
    mx = np.nanmax(array)
    mn = np.nanmin(array)
    t = (array - mn) / (mx - mn)
    return t


def normalize(data):
    left = np.mean(data) - 3 * np.std(data)
    right = np.mean(data) + 3 * np.std(data)
    new_data = data[np.logical_and(left < data, data < right)]
    return new_data


def judge_single_file(filename):
    """
    一轨数据去重后个数
    :param filename: 文件名
    :return:
    """
    dict = {}
    with h5py.File(filename, 'r') as f:
        for k in f['Data'].keys():
            data = f['/Data/' + k][:]
            dims = data.ndim
            if dims > 1:
                for i in range(data.shape[1]):
                    if k + str(i) not in dict.keys():
                        dict[k + str(i)] = np.unique(data[:, i])
                    else:
                        dict[k + str(i)] = np.concatenate([dict[k + str(i)], np.unique(data[:, i])])
            else:
                if k not in dict.keys():
                    dict[k] = np.unique(data[:])
                else:
                    dict[k] = np.concatenate([dict[k], np.unique(data[:])])
    for key, value in dict.items():
        print(key, len(value))


def judge_oneday_files(datetime, kind, dataname):
    """
    一天数据聚类 Counter
    :param datetime: 日期
    :param kind: OBC类型
    :param dataname: 参数名称
    :return:
    """
    filelist = sorted(glob.glob(r'/FY3E/SEM/1A/%sOBC/%s/%s/*.HDF' % (kind, datetime[0:4], datetime)))
    dict = {}
    for filename in filelist:
        with h5py.File(filename, 'r') as f:
            data = f['/Data/' + dataname][:]
            fillvalue = f['/Data/' + dataname].attrs['FillValue']
            dims = data.ndim
            if dims > 1:
                for i in range(data.shape[1]):
                    d_data = data[:, i]
                    mask = d_data != fillvalue
                    mean = np.mean(d_data[mask])
                    d_data = np.where(mask, d_data, mean)
                    if dataname + str(i) not in dict.keys():
                        dict[dataname + str(i)] = d_data
                    else:
                        dict[dataname + str(i)] = np.concatenate([dict[dataname + str(i)], d_data])
            else:
                mask = data != fillvalue
                mean = np.mean(data[mask])
                data = np.where(mask, data, mean)
                if dataname not in dict.keys():
                    dict[dataname] = data
                else:
                    dict[dataname] = np.concatenate([dict[dataname], data])
    return dict


def dbscan(filename, datename):
    with h5py.File(filename, 'r') as f:
        data = f['/Data/' + datename][:, 0]  # TODO need to change

        time_fields = f['Time']
        year = time_fields['Year'][:]
        month = time_fields['Month'][:]
        day = time_fields['Date'][:]
        hour = time_fields['Hour'][:]
        minute = time_fields['Minute'][:]
        second = time_fields['Second'][:]

        mktime = lambda i: time.mktime(tuple(i) + (0, 0, 0))
        t = np.array([mktime(i) for i in zip(year, month, day, hour, minute, second)])

        t = Normalize(t)[:, np.newaxis]
        # data = Normalize(data)[:,np.newaxis]
        data = data[:, np.newaxis]

        X = np.concatenate([t, data], axis=1)
        y_pred = DBSCAN(eps=1, min_samples=10).fit_predict(X)
        plt.scatter(X[:, 0], X[:, 1], c=y_pred, s=10)
        plt.savefig('/STSS/FY3E_STSS/dev/AIWarning/tmpfiles/dbscan.png', dpi=300)
        # plt.show()


def pinjie(filelt, dataname, dim):
    data_lt = []
    for filename in filelt:
        with h5py.File(filename, 'r') as f:
            data = f['/Data/' + dataname][:]
            fillvalue = f['/Data/' + dataname].attrs['FillValue']

            dims = data.ndim
            if dims > 1:
                data = data[:, dim]

            data = data[data != fillvalue]
            data_lt = np.concatenate([data_lt, data])
    return data_lt


def Periodic_map(signal):
    data = normalize(signal)
    N = len(data)
    f = np.linspace(0, N - 1, N) / N

    xfft = np.fft.fft(data)
    pper = np.abs(xfft) ** 2 / N

    plt.plot(f, np.abs(pper))
    plt.savefig('/STSS/FY3E_STSS/dev/AIWarning/tmpfiles/Periodic_map.png', dpi=300)


# 傅里叶变换计算数据周期
def CalPeriod(value):
    from scipy.fftpack import fft, fftfreq
    fft_series = fft(value)
    power = np.abs(fft_series)
    sample_freq = fftfreq(fft_series.size)

    pos_mask = np.where(sample_freq > 0)
    freqs = sample_freq[pos_mask]
    powers = power[pos_mask]
    top_k_seasons = 3
    top_k_idx = np.argpartition(powers, -top_k_seasons)[-top_k_seasons:]
    top_k_power = powers[top_k_idx]
    fft_periods = (1 / freqs[top_k_idx]).astype(int)
    return fft_periods[-1]
    # print(top_k_power)
    # print(fft_periods)


# 统计数字量
def digit_static(datetime, kind_dataname_lt, csvpath):
    with open(csvpath, 'w') as csvf:
        writer = csv.writer(csvf)
        for item in kind_dataname_lt:
            dict = judge_oneday_files(datetime, item[0], item[1])
            for key, value in dict.items():
                dd = Counter(value)
                writer.writerow([key, dd])


# 统计模拟量
def analog_static(datetime, kind_dataname_lt, csvpath):
    with open(csvpath, 'w') as csvf:
        writer = csv.writer(csvf)
        for item in kind_dataname_lt:
            dict = judge_oneday_files(datetime, item[0], item[1])
            for key, value in dict.items():
                dd = CalPeriod(value)
                plt.plot(value[0:dd*4+1])
                plt.axvline(x=dd,linestyle='--',color='r')
                plt.axvline(x=dd*2,linestyle='--',color='r')
                plt.axvline(x=dd*3,linestyle='--',color='r')
                plt.savefig('/STSS/FY3E_STSS/dev/AIWarning/PIC/SEM/%s.png'%key,dpi=300)
                plt.clf()
                writer.writerow([key, dd])


if __name__ == '__main__':
    datetime = '20220101'
    csvpath = '/STSS/FY3E_STSS/dev/AIWarning/Data/SEM_analog.csv'
    # kind_dataname_lt = [['MF','SVD'],
    #                     ['MF','CD'],
    #                     ['MF','RCount'],
    #                     ['HP','MD'],
    #                     ['ME','IEEVolDetect'],
    #                     ['ME','P5V2YC'],
    #                     ['ME','VREF']]

    kind_dataname_lt = [['MF', 'CD'], ['MF', 'FTD'], ['MF', 'ST'], ['MF', 'GMTC'], ['MF', 'GMTS'], ['MF', 'VS'],
                        ['HP', 'HPD'], ['HP', '5D'], ['HP', 'HPT'], ['HP', 'HET'], ['HP', 'MPT'], ['HP', 'MET'],
                        ['ME', 'BVMYC'], ['ME', 'THMB'],
                        ['MP', '12D'], ['MP', 'A5VD'], ['MP', 'D5VD'], ['MP', 'ND'],
                        ['SP', 'ESA'], ['SP', 'HVC'], ['SP', 'MHV'], ['SP', 'MCP'],['SP', 'APD'], ['SP', 'DHV'], ['SP', 'HVS'], ['SP', 'DV12'],['SP', 'ITel'], ['SP', 'ETel']
                        ]

    # analog_static(datetime, kind_dataname_lt, csvpath)

    #统计填充值
    # for kind in ['MF','HP','SP','MP','ME']:
    #     filename = sorted(glob.glob(r'/FY3E/SEM/1A/%sOBC/%s/%s/*.HDF' % (kind, datetime[0:4], datetime)))[0]
    #
    #     with h5py.File(filename, 'r') as f:
    #         for k in f['Data'].keys():
    #             fillvalue = f['/Data/' + k].attrs['FillValue']
    #             print(kind,k,fillvalue)
    import pickle
    kind = 'HP'
    param_file_path = '/STSS/FY3E_STSS/dev/AIWarning/YAML/SEM_%s_A.pkl' % kind
    param_file = open(param_file_path, 'rb')
    param_dict = pickle.load(param_file, encoding='bytes')
    for key, value in param_dict.items():
        print(key)
        flag = np.array([i.isdigit() for i in key])
        pos = np.argwhere(~flag)[-1][0]
        if len(key) == pos:
            print('1',key)
        else:
            print('2',key[0:(pos + 1)],key[(pos + 1):])
