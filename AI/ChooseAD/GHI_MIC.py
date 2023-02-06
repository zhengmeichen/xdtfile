# -*- coding: utf-8 -*-
# @Time : 2022/11/3 10:37
# @Author : ANDA
# @Site : 
# @File : GHI_MIC.py
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
                            data = data[:,:,0]
                            dims = data.ndim
                            if dims == 1 :
                                if group + '_' + k + '_' + l not in dict.keys():
                                    # 去除数据中的填充值在放入字典
                                    databool = data[:].flatten() != fillvalue
                                    dict[group + '_' + k + '_' + l] = data[:].flatten()[databool]

                                else:
                                    databool = data[:].flatten() != fillvalue
                                    if use_mean:
                                        dict[group + '_' + k + '_' + l] = (dict[group + '_' + k + '_' + l] + data[:].flatten()[databool]) / 2
                                    else:
                                        dict[group + '_' + k + '_' + l] = np.concatenate([dict[group + '_' + k + '_' + l], data[:].flatten()[databool]])

                            elif dims == 2:
                                if data.shape[0] < data.shape[1]:
                                    data = data.T
                                for i in range(data.shape[1]):
                                    if group + '_' + k + '_' + l + str(i) not in dict.keys():
                                        databool = data[:, i].flatten() != fillvalue
                                        dict[group + '_' + k + '_' + l + str(i)] = data[:, i].flatten()[databool]
                                    else:
                                        databool = data[:, i].flatten() != fillvalue

                                        if use_mean:
                                            dict[group + '_' + k + '_' + l + str(i)] = (dict[group + '_' + k + '_' + l + str(i)] + data[:].flatten()[databool]) / 2
                                        else:
                                            dict[group + '_' + k + '_' + l + str(i)] = np.concatenate([dict[group + '_' + k + '_' + l + str(i)], data[:, i].flatten()[databool]])


                            elif dims == 3:
                                shape = data.shape
                                px = np.argsort(shape)[::-1]
                                data = data.transpose(px)
                                for i in range(data.shape[1]):
                                    for j in range(data.shape[2]):
                                        if group + '_' + k + '_' + l + str(j) not in dict.keys():
                                            databool = data[:, i, j].flatten() != fillvalue
                                            dict[group + '_' + k + '_' + l + str(j)] = data[:, i, j].flatten()[databool]
                                        else:
                                            databool = data[:, i, j].flatten() != fillvalue

                                            if use_mean:
                                                dict[group + '_' + k + '_' + l + str(j)] = (dict[group + '_' + k + '_' + l + str(j)] + data[:, i, j].flatten()[databool]) / 2
                                            else:
                                                dict[group + '_' + k + '_' + l + str(j)] = np.concatenate([dict[group + '_' + k + '_' + l + str(j)], data[:, i, j].flatten()[databool]])


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
    date = '20220601'
    file_re = '/STSS/FY3E_STSS/dev/AIWarning/Data/FY4B/GHI/20220601/FY4B_GHI_2022*_*_DT.h5'
    out_path = '/STSS/FY3E_STSS/dev/AIWarning/MIC/GHI/GHI_MIC.h5'
    os.makedirs(os.path.dirname(out_path),exist_ok=True)
    filelist = sorted(glob.glob(file_re))

    # part 0 将所有数据集均存放在字典中
    main(file_re,out_path)