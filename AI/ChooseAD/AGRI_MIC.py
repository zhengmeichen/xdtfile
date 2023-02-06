# -*- coding: utf-8 -*-
# @Time : 2022/10/28 11:25
# @Author : ANDA
# @Site : 
# @File : AGRI_MIC.py
# @Software: PyCharm
import os
import glob
import h5py
import numpy as np
from minepy import MINE
def ReadData(filelist,use_mean=True):
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
                        data = data[:,:,0]
                        dims = data.ndim
                        if dims == 1 :
                            if group + '_' + k not in dict.keys():
                                # 去除数据中的填充值在放入字典
                                databool = data[:].flatten() != fillvalue
                                dict[group + '_' + k] = data[:].flatten()[databool]

                            else:
                                databool = data[:].flatten() != fillvalue

                                if use_mean:
                                    dict[group + '_' + k] = (dict[group + '_' + k]+ data[:].flatten()[databool])/2
                                else:
                                    dict[group + '_' + k] = np.concatenate([dict[group + '_' + k], data[:].flatten()[databool]])
                        elif dims == 2:
                            if data.shape[0] < data.shape[1]:
                                data = data.T
                            for i in range(data.shape[1]):
                                if group + '_' + k + str(i) not in dict.keys():
                                    databool = data[:, i].flatten() != fillvalue
                                    dict[group + '_' + k + str(i)] = data[:, i].flatten()[databool]
                                else:
                                    databool = data[:, i].flatten() != fillvalue
                                    if use_mean:
                                        dict[group + '_' + k + str(i)] = (dict[group + '_' + k + str(i)]+ data[:, i].flatten()[databool])/2
                                    else:
                                        dict[group + '_' + k + str(i)] = np.concatenate([dict[group + '_' + k + str(i)], data[:, i].flatten()[databool]])
                        elif dims == 3:
                            shape = data.shape
                            px = np.argsort(shape)[::-1]
                            data = data.transpose(px)
                            for i in range(data.shape[1]):
                                for j in range(data.shape[2]):
                                    if group + '_' + k + str(j) not in dict.keys():
                                        databool = data[:, i, j].flatten() != fillvalue
                                        dict[group + '_' + k + str(j)] = data[:, i, j].flatten()[databool]
                                    else:
                                        databool = data[:, i, j].flatten() != fillvalue
                                        if use_mean:
                                            dict[group + '_' + k + str(j)] = (dict[group + '_' + k + str(j)]+ data[:, i, j].flatten()[databool])/2
                                        else:
                                            dict[group + '_' + k + str(j)] = np.concatenate([dict[group + '_' + k + str(j)], data[:, i, j].flatten()[databool]])
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
    file_dict = ReadData(filelist)
    keys = file_dict.keys()
    if os.path.exists(save_path):
        os.remove(save_path)
    array_list = []
    key_list = []
    for key1 in keys:
        print(key1)
        key_list.append('_'.join([key1.split('_')[0][0]] + key1.split('_')[1:]))
        array1 = file_dict[key1]
        mic_list = []
        for key2 in keys:
            if key1 == key2:
                mic_list.append(1)
                continue
            array2 = file_dict[key2]
            try:
                cur_mic = compute_mic(array1, array2)
            except:
                continue
            mic_list.append(cur_mic)

        mic_array = np.array(mic_list)[:, np.newaxis]
        array_list.append(mic_array)

    save_array = np.concatenate(array_list, axis=1)
    write_hdf(save_path, save_array, [], 'mic')
    write_hdf(save_path, np.array(key_list).astype(np.string_), [], 'XName')

if __name__ == '__main__':
    date = '20220701'
    file_re = '/STSS/FY3E_STSS/dev/AIWarning/Data/FY4B/AGRI/20220701/FY4B_AGRI_2022*_*_DT.h5'
    out_root = '/STSS/FY3E_STSS/dev/AIWarning/MIC/AGRI/AGRI_MIC.h5'
    # file_re = '/FY4BPDSPULL/OPER/FY4B/HDF/AGRI/20220701/FY4B-_AGRI--_N_*_00001.HDF'
    # out_root = '/FY4BPDSPULL/OPER/FY4B/HDF/OUTPUT/AGRI_MIC.HDF'
    os.makedirs(os.path.dirname(out_root),exist_ok=True)
    filelist = sorted(glob.glob(file_re))

    # part 0 将所有数据集均存放在字典中
    main(file_re,out_root)