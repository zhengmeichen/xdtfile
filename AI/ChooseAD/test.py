# coding=utf-8
import pickle
import glob
import math
import sys
import pandas as pd
import numpy as np

'''SEM'''
# outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/Param/'+date+'HIRAS_A.pkl'
# outputfileD = '/STSS/FY3E_STSS/dev/AIWarning/Param/'+date+'HIRAS_D.pkl'


# for kind in ['MF','HP','SP','ME']:
#     for ADFlag in ['Analog','Digital']:
#         outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/SEM/*_SEM'+'_'+kind+'_%s.pkl'%ADFlag))
#         dic={}
#
#         for i in outputfileA:
#             pkl_file = open(i,'rb')
#             data1 = pickle.load(pkl_file)
#             for key,value in data1.items():
#                 if key in dic.keys():
#                     dic[key].append(value)
#                 else:
#                     dic[key] = [value]
#
#         df = pd.DataFrame(dic)
#         df.to_csv('/STSS/FY3E_STSS/dev/AIWarning/tmpfiles/SEM_'+kind+'_%s.csv'%ADFlag)


'''HIRAS 按天存'''
# dic={}
# outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/HIRAS/2022*HIRAS_D.pkl'))
# for i in outputfileA:
#
#     pkl_file = open(i,'rb')
#     data1 = pickle.load(pkl_file)
#     for key,value in data1.items():
#         if key in dic.keys():
#             dic[key].append(value)
#         else:
#             dic[key] = [value]
# # print(dic)
#
# # df = pd.DataFrame(dic)
# df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in dic.items()]))
# df.to_csv('/STSS/FY3E_STSS/dev/AIWarning/tmpfiles/HIRAS_D.csv')

# dic = {}
# outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/HIRAS/2022*HIRAS_D.pkl'))
# for i in outputfileA:
#
#     pkl_file = open(i, 'rb')
#     data1 = pickle.load(pkl_file)
#     for key, value in data1.items():
#         if key in dic.keys():
#             dic[key].append(value)
#         else:
#             dic[key] = [value]
# newdic = {}
# for k,v in dic.items():
#     print(k)
#     v = np.array(v)
#     vmin = np.min(v)
#     vmax = np.max(v)
#     newdic[k] = [vmin,vmax]
#     print(newdic[k])
#     # newdic[k]
#
#
# outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/YAML/HIRAS_D.pkl'
# fA = open(outputfileA,'wb')
# data = pickle.dump(newdic,fA,-1)
# fA.close()


'''仪器验证'''
# outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/Param/GNOS/20211101GNOS_A.pkl'
# outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/Param/GNOS/20211101GNOS_D.pkl'
# outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/Param/HIRAS/20211101HIRAS_A.pkl'
# outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/Param/HIRAS/20211101HIRAS_D.pkl'
# outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/Param/MERSI/20211101MERSI_A.pkl'
# outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/Param/MERSI/20211101MERSI_D.pkl'
# outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/Param/MWHS/20211101MWHS_A.pkl'
# outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/Param/MWHS/20211101MWHS_D.pkl'
# outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/Param/MWTS/20211101MWTS_A.pkl'
# outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/Param/MWTS/20211101MWTS_D.pkl'
# outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/Param/SEM/20211101_SEM_HP_Analog.pkl'
# outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/Param/SEM/20211101_SEM_HP_Digital.pkl'
# outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/Param/SEM/20211101_SEM_SP_Analog.pkl'
# outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/Param/SEM/20211101_SEM_SP_Digital.pkl'
# outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/Param/SIM/20211101SIM_A.pkl'
# outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/Param/SIM/20211101SIM_D.pkl'
# outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/Param/SSIM/SSIMOBCSL/20211101SSIMOBCSL_A.pkl'
# outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/Param/SSIM/SSIMOBCSL/20211101SSIMOBCSL_D.pkl'
# outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/Param/TRIPM/20211101TRIPM_A.pkl'
# outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/Param/TRIPM/20211101TRIPM_D.pkl'
# outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/Param/WRAD/20211101_WindRAD_A.pkl'
# outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/Param/WRAD/20211101_WindRAD_D.pkl'
# outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/Param/XEUVI/20211101XEUVI_A.pkl'
# outputfileA = '/STSS/FY3E_STSS/dev/AIWarning/Param/XEUVI/20211101XEUVI_D.pkl'
# pkl_file = open(outputfileA, 'rb')
# data1 = pickle.load(pkl_file)
# import pprint
# pprint.pprint(data1)
# pkl_file.close()


'''仪器数据合并数据'''
# 模拟量合并
# dic = {}
# outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/GNOS/202*GNOS_A.pkl'))
# outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/TRIPM/202*TRIPM_A.pkl'))
# outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/SSIM/SSIMOBCSL/202*SSIMOBCSL_A.pkl'))
# outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/MWHS/202*MWHS_A.pkl'))
# outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/MWTS/202*MWTS_A.pkl'))
# outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/SIM/202*SIM_A.pkl'))
# outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/XEUVI/202*XEUVI_A.pkl'))

# outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/HIRAS/202*HIRAS_A.pkl'))
# outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/SEM/202*_SEM_ME_Analog.pkl'))

# outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/WRAD/202[1-2]*_WindRAD_A.pkl'))
# outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/MERSI/202*MERSI_A.pkl'))
# for i in outputfileA:
#     # print(i)
#     pkl_file = open(i, 'rb')
#     data1 = pickle.load(pkl_file)
#     for key, value in data1.items():
#         # print(key, value)
#         if key in dic.keys():
#             dic[key].append(value)
#         else:
#             dic[key] = [value]
#
# newdic = {}
# for k, v in dic.items():
#     # print(k)
#     v = np.array(v)
#     vmin = np.min(v)
#     vmax = np.max(v)
#     newdic[k] = [vmin, vmax]
#     print(k, newdic[k])
#     # newdic[k]

# aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/GNOS_A.pkl'
# aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/TRIPM_A.pkl'
# aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/SSIMOBCSL_A.pkl'
# aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/MWHS_A.pkl'
# aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/MWTS_A.pkl'
# aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/SIM_A.pkl'
# aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/XEUVI_A.pkl'

# aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/HIRAS_A.pkl'
# aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/SEM_ME_A.pkl'

# aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/202107WRAD_A.pkl'
# aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/MERSI_A.pkl'

# fA = open(aa, 'wb')
# pickle.dump(newdic, fA, -1)
# fA.close()

# 离散变量合并
# dic1 = {}
# # outputfileD = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/GNOS/202*GNOS_D.pkl'))
# # outputfileD = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/TRIPM/202*TRIPM_D.pkl'))
# # outputfileD = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/SSIM/SSIMOBCSL/202*SSIMOBCSL_D.pkl'))
# # outputfileD = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/MWHS/202*MWHS_D.pkl'))
# # outputfileD = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/MWTS/202*MWTS_D.pkl'))
# # outputfileD = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/SIM/202*SIM_D.pkl'))
# # outputfileD = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/XEUVI/202*XEUVI_D.pkl'))
#
# # outputfileD = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/HIRAS/202*HIRAS_D.pkl'))
# # outputfileD = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/SEM/202*_SEM_SP_D*.pkl'))
#
# outputfileD = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/WRAD/2021*_WindRAD_D.pkl'))
# # outputfileD = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/MERSI/202*MERSI_D.pkl'))
# for i in outputfileD:
#     pkl_file1 = open(i, 'rb')
#     data2 = pickle.load(pkl_file1)
#     # print data2
#     for key, value in data2.items():
#         # value = np.array(value)
#         print key, value
#         if key in dic1.keys():
#             dic1[key].extend(value)
#         else:
#             dic1[key] = value
# # print dic1
#
# newdic1 = {}
# for k, v in dic1.items():
#     # print(k)
#     v1 = list(set(v))
#     # print k, v1
#     newdic1[k] = v1
#     # print(k, newdic1[k])
#
#
# # aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/GNOS_D.pkl'
# # aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/TRIPM_D.pkl'
# # aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/SSIMOBCSL_D.pkl'
# # aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/MWHS_D.pkl'
# # aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/MWTS_D.pkl'
# # aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/SIM_D.pkl'
# # aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/XEUVI_D.pkl'
#
# # aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/HIRAS_D.pkl'
# # aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/SEM_SP_D.pkl'
#
# aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/202107WRAD_D.pkl'
# # aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/MERSI_D.pkl'
# fA = open(aa, 'wb')
# pickle.dump(newdic1, fA, -1)
# fA.close()


'''
dic={}
outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/WRAD/WindRAD_C/202[1-2]*_WindRAD_A.pkl'))
for i in outputfileA:
    print(i)
    pkl_file = open(i, 'rb')
    data1 = pickle.load(pkl_file)
    for key, value in data1.items():
        if 'Data_load_state' in key:
            print(value)
        if key in dic.keys():
            dic[key].append(value)
        else:
            dic[key] = [value]
exit()

newdic = {}
for k, v in dic.items():

    v = np.array(v)
    vmin = np.min(v)
    vmax = np.max(v)
    newdic[k] = [vmin, vmax]
    print(k, newdic[k])
    # newdic[k]
'''

'''




# 模拟量合并
dic = {}
outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/WRAD/WRAD_A_DESCEND_C/202109*_WindRAD_A.pkl'))
# outputfileA = ['/STSS/FY3E_STSS/dev/AIWarning/Param/WRAD/WRAD_A_DESCEND_C/20210910_WindRAD_A.pkl','/STSS/FY3E_STSS/dev/AIWarning/Param/WRAD/WRAD_A_DESCEND_C/20210911_WindRAD_A.pkl']

for i in outputfileA:
    # print(i)
    pkl_file = open(i, 'rb')
    data1 = pickle.load(pkl_file)
    for key, value in data1.items():
        # print(key, value)
        if key in dic.keys():
            dic[key].append(value)
        else:
            dic[key] = [value]

# print dic
newdic = {}
for k, v in dic.items():
    # print v
    # print(k,v)
    v = np.array(v)
    # print v.shape
    vmin = []
    vmax = []

    for i in range(v.shape[0]):
        vmin.append(v[i][0])
        vmax.append(v[i][1])
    # print 'kkk',k, vmin, vmax
    vmin = np.sort(vmin)
    vmax = np.sort(vmax)
    # print vmin, vmax
    # print len(vmin), len(vmax)
    if len(vmin) == 1:
        vmin_c = 0
    else:
        vmin_c = int(math.ceil(0.15 * len(vmin)))
    # print vmin_c
    if len(vmax) == 1 or len(vmax) == 2 :
        vmax_c = 0
    else:
        vmax_c = int(math.floor(0.85 * len(vmax)))
    # print vmax_c
    # print vmin[vmin_c], vmax[vmax_c]
    newdic[k] = [vmin[vmin_c], vmax[vmax_c]]
    # print(k, newdic[k])
    # newdic[k]

# print newdic
aa = '/STSS/FY3E_STSS/dev/AIWarning/202109WRAD_A.pkl'

fA = open(aa, 'wb')
pickle.dump(newdic, fA, -1)
fA.close()
'''



# 离散变量合并
dic1 = {}

outputfileD = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/WRAD/WRAD_A_DESCEND_C/202109*_WindRAD_D.pkl'))

for i in outputfileD:
    pkl_file1 = open(i, 'rb')
    data2 = pickle.load(pkl_file1)
    # print data2
    for key, value in data2.items():
        # value = np.array(value)
        print key, value
        if key in dic1.keys():
            dic1[key].extend(value)
        else:
            dic1[key] = value
# print dic1

newdic1 = {}
for k, v in dic1.items():
    # print(k)
    v1 = list(set(v))
    # print k, v1
    newdic1[k] = v1
    # print(k, newdic1[k])

print newdic1

aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/202109WRAD_D.pkl'

fA = open(aa, 'wb')
pickle.dump(newdic1, fA, -1)
fA.close()