# -*- coding: utf-8 -*-
# @Time : 2022/11/3 10:38
# @Author : ANDA
# @Site : 
# @File : GIIRS_MIC.py
# @Software: PyCharm
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
        try:
            print(eachfile)
            with h5py.File(eachfile, 'r') as f:
                for group in f.keys():
                    for k in f[group].keys():
                        # group = group.encode('utf-8')
                        # k = k.encode('utf-8')
                        if k=='Time' or k=='timestamp':
                            continue
                        for l in f[group + '/' + k].keys():
                            data = f[group + '/' + k + '/' + l][()]
                            try:
                                fillvalue = f[group + '/' + k + '/' + l].attrs['Fill Value']
                            except:
                                fillvalue = 999999
                            if (isinstance(fillvalue, np.ndarray)):
                                fillvalue = fillvalue[0]
                            if k=='OBCG':
                                data = data[0]
                            else:
                                data = data[:, :, 0]
                            dims = data.ndim
                            if dims == 1:
                                if group + '_' + k + '_' + l not in dict.keys():
                                    # 去除数据中的填充值在放入字典
                                    # databool = data[:].flatten() != fillvalue
                                    # dict[group + '_' + k + '_' + l] = data[:].flatten()[databool]

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
                                                if min(len(dict[group + '_' + k]),
                                                       len(filter_array.flatten()[databool])) == 0:
                                                    continue
                                                len_limit = min(len(dict[group + '_' + k]),
                                                                len(filter_array.flatten()[databool]))
                                            dict[group + '_' + k] = (dict[group + '_' + k][0:len_limit] +
                                                                     filter_array.flatten()[databool][0:len_limit]) / 2
                                        else:
                                            dict[group + '_' + k] = np.concatenate([dict[group + '_' + k][0:len_limit],
                                                                                    filter_array.flatten()[databool][
                                                                                    0:len_limit]])
                                    else:
                                        databool = data[:].flatten() != fillvalue
                                        if use_mean:
                                            if len(dict[group + '_' + k]) != len(data[:].flatten()[databool]):
                                                if min(len(dict[group + '_' + k]),
                                                       len(data[:].flatten()[databool])) == 0:
                                                    continue
                                                len_limit = min(len(dict[group + '_' + k]),
                                                                len(data[:].flatten()[databool]))
                                            dict[group + '_' + k] = (dict[group + '_' + k][0:len_limit] +
                                                                     data[:].flatten()[databool][0:len_limit]) / 2
                                        else:
                                            dict[group + '_' + k] = np.concatenate([dict[group + '_' + k][0:len_limit],
                                                                                    data[:].flatten()[databool][
                                                                                    0:len_limit]])
                            elif dims == 2:
                                if data.shape[0] < data.shape[1]:
                                    data = data.T
                                for i in range(data.shape[1]):
                                    if group + '_' + k + '_' + l + str(i) not in dict.keys():
                                        # databool = data[:, i].flatten() != fillvalue
                                        # dict[group + '_' + k + '_' + l + str(i)] = data[:, i].flatten()[databool]

                                        if do_filter:
                                            filter_array = array_filter(data[:, i])
                                            databool = filter_array.flatten() != fillvalue
                                            dict[group + '_' + k + str(i)] = filter_array.flatten()[databool][
                                                                             0:len_limit]
                                        else:
                                            databool = data[:, i].flatten() != fillvalue
                                            dict[group + '_' + k + str(i)] = data[:, i].flatten()[databool][0:len_limit]
                                    else:
                                        # databool = data[:, i].flatten() != fillvalue
                                        # dict[group + '_' + k + '_' + l + str(i)] = np.concatenate([dict[group + '_' + k + '_' + l + str(i)], data[:, i].flatten()[databool]])

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
                                                if len(dict[group + '_' + k + str(i)]) != len(data[:, i].flatten()[databool]):
                                                    if min(len(dict[group + '_' + k + str(i)]),len(data[:, i].flatten()[databool])) == 0:
                                                        continue
                                                    len_limit = min(len(dict[group + '_' + k + str(i)]),len(data[:, i].flatten()[databool]))
                                                dict[group + '_' + k + str(i)] = (dict[group + '_' + k + str(i)][0:len_limit] + data[:, i].flatten()[databool][0:len_limit]) / 2
                                            else:
                                                dict[group + '_' + k + str(i)] = np.concatenate([dict[group + '_' + k + str(i)][0:len_limit],data[:, i].flatten()[databool][0:len_limit]])
                            elif dims == 3:
                                shape = data.shape
                                px = np.argsort(shape)[::-1]
                                data = data.transpose(px)
                                for i in range(data.shape[1]):
                                    for j in range(data.shape[2]):
                                        if group + '_' + k + '_' + l + str(j) not in dict.keys():
                                            # databool = data[:, i, j].flatten() != fillvalue
                                            # dict[group + '_' + k + '_' + l + str(j)] = data[:, i, j].flatten()[databool]

                                            if do_filter:
                                                filter_array = array_filter(data[:, i, j])
                                                databool = filter_array.flatten() != fillvalue
                                                dict[group + '_' + k + str(j)] = filter_array.flatten()[databool][0:len_limit]
                                            else:
                                                databool = data[:, i, j].flatten() != fillvalue
                                                dict[group + '_' + k + str(j)] = data[:, i, j].flatten()[databool][0:len_limit]
                                        else:
                                            # databool = data[:, i, j].flatten() != fillvalue
                                            # dict[group + '_' + k + '_' + l + str(j)] = np.concatenate([dict[group + '_' + k + '_' + l + str(j)],data[:, i, j].flatten()[databool]])
                                            databool = data[:, i, j].flatten() != fillvalue
                                            if use_mean:
                                                if len(dict[group + '_' + k + str(j)]) != len(data[:, i, j].flatten()[databool]):
                                                    if min(len(dict[group + '_' + k + str(j)]),len(data[:, i, j].flatten()[databool])) == 0:
                                                        continue
                                                    len_limit = min(len(dict[group + '_' + k + str(j)]),len(data[:, i, j].flatten()[databool]))
                                                dict[group + '_' + k + str(j)] = (dict[group + '_' + k + str(j)][0:len_limit] + data[:, i, j].flatten()[databool][0:len_limit]) / 2
                                            else:
                                                dict[group + '_' + k + str(j)] = np.concatenate([dict[group + '_' + k + str(j)][0:len_limit],data[:, i, j].flatten()[databool][0:len_limit]])
        except:
            continue
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
    file_dict = ReadData(filelist,use_mean=True,do_filter=False)
    keys = file_dict.keys()
    if os.path.exists(save_path):
        os.remove(save_path)
    for key1 in keys:
        array1 = file_dict[key1]
        key2_list = []
        mic_list = []
        for key2 in keys:
            if key1 == key2:
                continue
            array2 = file_dict[key2]
            try:
                cur_mic = compute_mic(array1,array2)
            except:
                continue
            mic_list.append(cur_mic)
            key2_list.append(key2)
        mic_array = np.array(mic_list)
        key2_array = np.array(key2_list).astype(np.string_)
        write_hdf(save_path,mic_array,[],key1+'_mic')
        write_hdf(save_path,key2_array,[],key1+'_XName')

if __name__ == '__main__':
    date = '20220701'
    file_re = '/STSS/FY3E_STSS/dev/AIWarning/Data/FY4B/GIIRS/20220701/FY4B_GIIRS_2022*_*_DT.h5'
    out_path = '/STSS/FY3E_STSS/dev/AIWarning/MIC/GIIRS/GIIRS_MIC.h5'
    # file_re = '/FY4BPDSPULL/OPER/FY4B/HDF/GIIRS/20220701/FY4B-_GIIRS-_N_*_00001.HDF'
    # out_path = '/FY4BPDSPULL/OPER/FY4B/HDF/OUTPUT/GIIRS_MIC.HDF'
    os.makedirs(os.path.dirname(out_path),exist_ok=True)
    filelist = sorted(glob.glob(file_re))

    # part 0 将所有数据集均存放在字典中
    main(file_re,out_path)