# -*- coding: utf-8 -*-
# @Time : 2022/11/3 10:49
# @Author : ANDA
# @Site : 
# @File : WRAD_MIC.py
# @Software: PyCharm
# 读数据
import os
import glob
import h5py
import numpy as np
from minepy import MINE
def array_filter(array,filter_param=2000):
    line_num = array.shape[0]
    array_index = range(line_num)
    need_index = array_index[::filter_param]
    delete_index = list(set(array_index).difference(set(need_index)))
    filter_array = np.delete(array,delete_index,axis=0)
    return filter_array
def ReadData(filelist,use_mean=True,do_filter=True):
    '''

    :param filelist: 输入文件列表
    :return: 所有数据集字典
    '''
    dict = {}
    len_limit = None
    # len_limit = 50
    for eachfile in filelist:
        # try:
        print(eachfile)
        with h5py.File(eachfile, 'r') as f:
            for group in f.keys():
                for k in f[group].keys():
                    if 'cnt' in k:
                        continue
                    if k=='packagetime' or k=='QAFlag':
                        continue
                    data = f[group + '/' + k][()]
                    try:
                        fillvalue = f[group + '/' + k].attrs['Fill Value']
                    except:
                        fillvalue = 999999
                    # print("fillvalue",group + '/' + k,fillvalue)
                    if (isinstance(fillvalue, np.ndarray)):
                        fillvalue = fillvalue[0]
                    dims = data.ndim
                    if dims == 1 :
                        if group + '_' + k not in dict.keys():
                            # 去除数据中的填充值在放入字典
                            if do_filter:
                                filter_array = array_filter(data[:])
                                databool = filter_array.flatten() != fillvalue
                                dict[group + '_' + k] = filter_array.flatten()[databool][0:len_limit]
                            else:
                                databool = data[:].flatten() != fillvalue
                                dict[group + '_' + k] = data[:].flatten()[databool][0:len_limit]

                        else:
                            if do_filter:
                                filter_array = array_filter(data[:])
                                databool = filter_array.flatten() != fillvalue
                                if use_mean:
                                    if len(dict[group + '_' + k]) != len(filter_array.flatten()[databool]):
                                        if min(len(dict[group + '_' + k]),len(filter_array.flatten()[databool]))==0:
                                            continue
                                        len_limit = min(len(dict[group + '_' + k]),len(filter_array.flatten()[databool]))
                                    dict[group + '_' + k] = (dict[group + '_' + k][0:len_limit] + filter_array.flatten()[databool][0:len_limit]) / 2
                                else:
                                    dict[group + '_' + k] = np.concatenate([dict[group + '_' + k][0:len_limit], filter_array.flatten()[databool][0:len_limit]])
                            else:
                                databool = data[:].flatten() != fillvalue
                                if use_mean:
                                    if len(dict[group + '_' + k]) != len(filter_array.flatten()[databool]):
                                        if min(len(dict[group + '_' + k]),len(filter_array.flatten()[databool]))==0:
                                            continue
                                        len_limit = min(len(dict[group + '_' + k]),len(filter_array.flatten()[databool]))
                                    dict[group + '_' + k] = (dict[group + '_' + k][0:len_limit] + data[:].flatten()[databool][0:len_limit]) / 2
                                else:
                                    dict[group + '_' + k] = np.concatenate([dict[group + '_' + k][0:len_limit], data[:].flatten()[databool][0:len_limit]])
                    elif dims == 2:
                        if data.shape[0] < data.shape[1]:
                            data = data.T
                        if k=='Raw_DN_Signal':
                            dim_shape = 2
                        else:
                            dim_shape = data.shape[1]
                        for i in range(dim_shape):
                            if group + '_' + k + str(i) not in dict.keys():
                                if do_filter:
                                    filter_array = array_filter(data[:, i])
                                    databool = filter_array.flatten() != fillvalue
                                    dict[group + '_' + k + str(i)] = filter_array.flatten()[databool][0:len_limit]
                                else:
                                    databool = data[:, i].flatten() != fillvalue
                                    dict[group + '_' + k + str(i)] = data[:, i].flatten()[databool][0:len_limit]
                            else:
                                if do_filter:
                                    filter_array = array_filter(data[:, i])
                                    databool = filter_array.flatten() != fillvalue
                                    if use_mean:
                                        if len(dict[group + '_' + k + str(i)]) != len(filter_array.flatten()[databool]):
                                            if min(len(dict[group + '_' + k + str(i)]),len(filter_array.flatten()[databool])) == 0:
                                                continue
                                            len_limit = min(len(dict[group + '_' + k + str(i)]),len(filter_array.flatten()[databool]))
                                        dict[group + '_' + k + str(i)] = (dict[group + '_' + k + str(i)][0:len_limit] + filter_array.flatten()[databool][0:len_limit]) / 2
                                    else:
                                        dict[group + '_' + k + str(i)] = np.concatenate([dict[group + '_' + k + str(i)][0:len_limit],filter_array.flatten()[databool][0:len_limit]])
                                else:
                                    databool = data[:, i].flatten() != fillvalue
                                    if use_mean:
                                        if len(dict[group + '_' + k + str(i)]) != len(filter_array.flatten()[databool]):
                                            if min(len(dict[group + '_' + k + str(i)]),len(filter_array.flatten()[databool])) == 0:
                                                continue
                                            len_limit = min(len(dict[group + '_' + k + str(i)]),len(filter_array.flatten()[databool]))
                                        dict[group + '_' + k + str(i)] = (dict[group + '_' + k + str(i)][0:len_limit] + data[:, i].flatten()[databool][0:len_limit]) / 2
                                    else:
                                        dict[group + '_' + k + str(i)] = np.concatenate([dict[group + '_' + k + str(i)][0:len_limit], data[:, i].flatten()[databool][0:len_limit]])
                    elif dims == 3:
                        shape = data.shape
                        px = np.argsort(shape)[::-1]
                        data = data.transpose(px)
                        for i in range(data.shape[1]):
                            for j in range(data.shape[2]):
                                if group + '_' + k + str(j) not in dict.keys():
                                    if do_filter:
                                        filter_array = array_filter(data[:, i,j])
                                        databool = filter_array.flatten() != fillvalue
                                        dict[group + '_' + k + str(j)] = filter_array.flatten()[databool][0:len_limit]
                                    else:
                                        databool = data[:, i, j].flatten() != fillvalue
                                        dict[group + '_' + k + str(j)] = data[:, i, j].flatten()[databool][0:len_limit]
                                else:
                                    if do_filter:
                                        filter_array = array_filter(data[:, i, j])
                                        databool = filter_array.flatten() != fillvalue
                                        if use_mean:
                                            if len(dict[group + '_' + k + str(j)]) != len(filter_array.flatten()[databool]):
                                                if min(len(dict[group + '_' + k + str(j)]),len(filter_array.flatten()[databool])) == 0:
                                                    continue
                                                len_limit = min(len(dict[group + '_' + k + str(j)]),len(filter_array.flatten()[databool]))
                                            dict[group + '_' + k + str(j)] = (dict[group + '_' + k + str(j)][0:len_limit] + filter_array.flatten()[databool][0:len_limit]) / 2
                                        else:
                                            dict[group + '_' + k + str(j)] = np.concatenate([dict[group + '_' + k + str(j)][0:len_limit],filter_array.flatten()[databool][0:len_limit]])
                                    else:
                                        databool = data[:, i, j].flatten() != fillvalue
                                        if use_mean:
                                            if len(dict[group + '_' + k + str(j)]) != len(filter_array.flatten()[databool]):
                                                if min(len(dict[group + '_' + k + str(j)]),len(filter_array.flatten()[databool])) == 0:
                                                    continue
                                                len_limit = min(len(dict[group + '_' + k + str(j)]),len(filter_array.flatten()[databool]))
                                            dict[group + '_' + k + str(j)] = (dict[group + '_' + k + str(j)][0:len_limit]+ filter_array.flatten()[databool][0:len_limit])/2
                                        else:
                                            dict[group + '_' + k + str(j)] = np.concatenate([dict[group + '_' + k + str(j)][0:len_limit], filter_array.flatten()[databool][0:len_limit]])

        # except:
        #     continue
    return dict

def write_hdf(hdf_path,hdf_array,group_list,tabel_name):
    '''
    根据hdf文件路径写某一表数据
    :param hdf_path:
    :param hdf_array:
    :param group_list:
    :param tabel_name:
    :return:
    '''
    hdffile = h5py.File(hdf_path, 'a')
    hdfgroup = hdffile
    if len(group_list) > 0:
        for group in group_list:
            if group not in hdfgroup.keys():
                hdfgroup.create_group(group)
            hdfgroup = hdfgroup[group]
    # hdfgroup.create_dataset(tabel_name, data=hdf_array, compression='gzip', compression_opts=6)
    hdfgroup.create_dataset(tabel_name, data=hdf_array)

def compute_mic(x,y):
    m = MINE()
    m.compute_score(x, y)
    return m.mic()
def main(file_re,save_path):
    filelist = sorted(glob.glob(file_re))
    file_dict = ReadData(filelist)
    keys = file_dict.keys()
    if os.path.exists(save_path):
        os.remove(save_path)
    array_list = []
    key_list = []
    for key1 in keys:
        if 'Satellite Telemetry Data_' in key1 or 'Raw_' in key1:
            continue
        print(key1)
        key_list.append('_'.join([key1.split('_')[0][0]]+key1.split('_')[1:]))
        array1 = file_dict[key1]
        mic_list = []
        for key2 in keys:
            if 'Satellite Telemetry Data_' in key2 or 'Raw_' in key2:
                continue
            if key1 == key2:
                mic_list.append(1)
                continue
            array2 = file_dict[key2]
            try:
                cur_mic = compute_mic(array1,array2)
            except:
                mic_list.append(-1)
                continue
            mic_list.append(cur_mic)
        mic_array = np.array(mic_list)[:,np.newaxis]
        # key2_array = np.array(key2_list).astype(np.string_)
        array_list.append(mic_array)


    save_array = np.concatenate(array_list,axis=1)
    write_hdf(save_path, save_array, [],'mic')
    write_hdf(save_path, np.array(key_list).astype(np.string_), [],'XName')


if __name__ == '__main__':
    date = '20220601'
    file_re = '/FY3E/WRAD/1A/OBC/ASCENDC/2022/20220601/FY3E_WRADC_ORBA_1A_*_OBC--_V0.HDF'
    out_path = '/STSS/FY3E_STSS/dev/AIWarning/MIC/WRADC/WRADC_MIC_sample.h5'
    os.makedirs(os.path.dirname(out_path),exist_ok=True)
    filelist = sorted(glob.glob(file_re))

    # part 0 将所有数据集均存放在字典中
    main(file_re,out_path)