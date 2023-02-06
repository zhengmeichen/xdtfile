#coding=utf-8
import h5py
import glob
import numpy as np
import matplotlib
from collections import Counter
from PIL import Image
import os
SYSROOT = os.getenv('SYSTEM_ROOT', '.')
try:
    matplotlib.rc_file(SYSROOT + '/stweb/xlib/matplotlibrc')
except:
    matplotlib.use('Agg')
    traceback.print_exc()
from matplotlib import cm, dates, colors, pyplot as plt, ticker

#滑动窗口检测异常
def SlidingWindowDE(value):
    value = value[value!=-9999.9]
    value_mean = np.mean(value)
    value_std = np.std(value)
    value_up = value_mean-3*value_std
    value_down = value_mean+3*value_std
    # print(value_up)
    # print(value_down)
    vaule_QA = (value>=value_up) & (value<=value_down)
    # value[vaule_QA]
    return value

#傅里叶变换计算数据周期
def CalPeriod(value):
    '''

    :param value: 单参数数据
    :return: 周期内数据个数，即认为个数*数据时间间隔=周期
    '''
    from scipy.fftpack import fft,fftfreq
    fft_series=fft(value)
    power=np.abs(fft_series)
    sample_freq = fftfreq(fft_series.size)

    pos_mask=np.where(sample_freq>0)
    freqs=sample_freq[pos_mask]
    powers=power[pos_mask]
    top_k_seasons=3
    top_k_idx=np.argpartition(powers,-top_k_seasons)[-top_k_seasons:]
    top_k_power=powers[top_k_idx]
    fft_periods=(1/freqs[top_k_idx]).astype(int)
    print(top_k_power)
    print(fft_periods)
    return fft_periods[-1]

#数据去重
def DataDedup(data):
    return np.unique(data)

#数据个数统计
def judge_oneday_files(data_list):
    """
    一天数据聚类 Counter
    :param data_list: 一天的数据(除去填充值后)
    :return:该数据集中出现数据及对应频数的字典 {数值：频数}
    """

    dict = Counter(data_list)
    # print(dict)
    return dict

if __name__ == '__main__':
    filelist = sorted(glob.glob('/FY3E/HIRAS/1A/OBC/2022/20220119/FY3E_HIRAS_GRAN_1A_20220119_*_OBC--_V0.HDF'))
    Alldata = []
    dict={}
    for filename in filelist:
        print(filename)
        with h5py.File(filename, 'r') as f:
            for group in f.keys():
                for k in f[group].keys():
                    data = f[group+'/' + k][:]
                    dims = data.ndim
                    if (data.shape[0] == 37) | (data.shape[0]==38):
                        if dims==2:
                            if group+'_'+k not in dict.keys():
                                dict[group+'_'+k] = data[:,-1].flatten()
                            else:
                                dict[group + '_' + k] =np.concatenate([dict[group + '_' + k], data[:, -1].flatten()])
                        elif dims==3:
                            for i in range(data.shape[2]):
                                if group+'_'+k+str(i) not in dict.keys():
                                    dict[group+'_'+k+str(i)] = data[:,-1,i].flatten()
                                else:
                                    dict[group+'_'+k+str(i)] = np.concatenate([dict[group+'_'+k+str(i)], data[:,-1, i].flatten()])
    outputfile = '/STSS/FY3E_STSS/dev/AIWarning/Data/HIRASCount.HDF'
    with h5py.File(outputfile, 'w') as o:
        for key, value in dict.items():
            print(key)
            result = judge_oneday_files(value)
            o['/Count/'+key+'_keys'] = result.keys()
            o['/Count/'+key+'_values'] = result.values()
            # print(key)
            # print(result.keys())
            # print(result.values())
            valuebool = ((value==-9999.9) | (value==65535) | (value==4294934528) | (value==-32768) |
                         (value==4294967295) | (value==255) | (value==127) | (value==-2147483648) |
                         (value==4294967168))
            value[valuebool] = np.mean(value[~valuebool])
            print("======",np.mean(value[~valuebool]))
            Period = CalPeriod(value)*8
            plt.figure(figsize=(19,12))
            plt.cla()
            plt.plot(value)
            plt.grid()
            plt.savefig('/STSS/FY3E_STSS/dev/AIWarning/PIC/HIRAS/'+key+'.png')
    # plt.plot(Alldata)
    # plt.grid()
    # plt.savefig('/STSS/FY3E_STSS/dev/AIWarning/PIC/test.png')


