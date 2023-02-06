# -*- coding: utf-8 -*-
# @Time : 2022/11/2 15:48
# @Author : ANDA
# @Site : 
# @File : ShowPKL.py
# @Software: PyCharm
import pprint
import pickle
def show_pkl(pkl_file):
    pkl_file = open(pkl_file,'rb')
    data2 = pickle.load(pkl_file)
    pprint.pprint(data2)

if __name__ == '__main__':
    pkl_file = '/STSS/FY3E_STSS/dev/AIWarning/YAML/AGRI_A.pkl'
    show_pkl(pkl_file)