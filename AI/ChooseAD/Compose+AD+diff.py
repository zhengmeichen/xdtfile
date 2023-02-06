# coding=utf-8
import pickle
import glob
import math
import sys
import pandas as pd
import numpy as np

dicA = {}
dicD = {}
'''WRAD'''
# outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/WRAD/WRADK/202*WRAD_A.pkl'))
# outputfileD = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/WRAD/WRADK/202*WRAD_D.pkl'))
# outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/WRAD/WRADC/202*WRAD_A.pkl'))
# outputfileD = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/WRAD/WRADC/202*WRAD_D.pkl'))
'''GNOS'''
# outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/GNOS/202*GNOS_A.pkl'))
# outputfileD = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/GNOS/202*GNOS_D.pkl'))
'''MWHS'''
# outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/MWHS/202*MWHS_A.pkl'))
# outputfileD = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/MWHS/202*MWHS_D.pkl'))
'''MWTS'''
# outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/MWTS/202*MWTS_A.pkl'))
# outputfileD = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/MWTS/202*MWTS_D.pkl'))
'''SIM'''
# outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/SIM/202*SIM_A.pkl'))
# outputfileD = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/SIM/202*SIM_D.pkl'))
'''SSIM'''
# outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/SSIM/SSIMOBCSL/202*SSIMOBCSL_A.pkl'))
# outputfileD = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/SSIM/SSIMOBCSL/202*SSIMOBCSL_D.pkl'))
'''TRIPM'''
# outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/TRIPM/202*TRIPM_A.pkl'))
# outputfileD = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/TRIPM/202*TRIPM_D.pkl'))
'''XEUVI'''
# outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/XEUVI/202*XEUVI_A.pkl'))
# outputfileD = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/XEUVI/202*XEUVI_D.pkl'))
'''SEM-HP'''
# outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/SEM/202*_SEM_HP_Analog.pkl'))
# outputfileD = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/SEM/202*_SEM_HP_Digital.pkl'))
'''SEM-ME'''
# outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/SEM/202*_SEM_ME_Analog.pkl'))
# outputfileD = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/SEM/202*_SEM_ME_Digital.pkl'))
'''SEM-MF'''
# outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/SEM/202*_SEM_MF_Analog.pkl'))
# outputfileD = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/SEM/202*_SEM_MF_Digital.pkl'))
'''SEM-MP'''
outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/SEM/202*_SEM_MP_Analog.pkl'))
outputfileD = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/SEM/202*_SEM_MP_Digital.pkl'))
'''SEM-SP'''
# outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/SEM/202*_SEM_SP_Analog.pkl'))
# outputfileD = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/SEM/202*_SEM_SP_Digital.pkl'))
'''MERSI'''
# outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/MERSI/202*MERSI_A.pkl'))
# outputfileD = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/MERSI/202*MERSI_D.pkl'))
'''HIRAS'''
# outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/HIRAS/202*HIRAS_A.pkl'))
# outputfileD = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/HIRAS/202*HIRAS_D.pkl'))
'''AGRI'''
# outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/AGRI/202*AGRI_A.pkl'))
# outputfileD = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/AGRI/202*AGRI_D.pkl'))
'''GHI'''
# outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/GHI/202*GHI_A.pkl'))
# outputfileD = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/GHI/202*GHI_D.pkl'))
'''GIIRS'''
# outputfileA = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/GIIRS/202*GIIRS_A.pkl'))
# outputfileD = sorted(glob.glob('/STSS/FY3E_STSS/dev/AIWarning/Param/GIIRS/202*GIIRS_D.pkl'))
# 读取模拟量全部数据
for i in outputfileA:
    # print(i)
    pkl_file = open(i, 'rb')
    data1 = pickle.load(pkl_file)
    for key, value in data1.items():
        # print(key, value)
        if key in dicA.keys():
            dicA[key].append(value)
        else:
            dicA[key] = [value]

# 读取离散量全部数据
for j in outputfileD:
    pkl_file1 = open(j, 'rb')
    data2 = pickle.load(pkl_file1)
    # print data2
    for key, value in data2.items():
        # value = np.array(value)
        # print key, value
        if key in dicD.keys():
            dicD[key].extend(value)
        else:
            dicD[key] = value


# 双方去重，保证一个数据只出现在一个类型里
for keyA, valueA in list(dicA.items()):
    for keyD, valueD in list(dicD.items()):
        if keyA == keyD:
            if len(valueA) < len(valueD):
                # 从字典中删除该键值对
                dicA.pop(keyA)
            else:
                dicD.pop(keyD)


# 重新划定模拟量阈值范围
newdicA = {}
for k, v in dicA.items():

    v = np.array(v)
    # 将所有value的值都写到一起，直接进行范围划分
    max_min = []
    for i in range(v.shape[0]):
        max_min.append(v[i][0])
        max_min.append(v[i][1])

    max_min_set = sorted(list(set(max_min)))

    # pont = 0.05
    # if len(max_min_set) == 2:
    #     vmin_c = 0
    #     vmax_c = -1
    # else:
    #     vmin_c = int(math.ceil(pont * len(max_min_set)))
    #     vmax_c = int(math.floor((1 - pont) * len(max_min_set)))
    #
    # newdicA[k] = [max_min_set[vmin_c], max_min_set[vmax_c]]
    newdicA[k] = [max_min_set[0], max_min_set[-1]]

print(newdicA)

# aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/WRADC_A.pkl'
'''WRAD'''
# aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/After_WRADC_A.pkl'
'''GNOS'''
# aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/GNOS_A.pkl'
'''MWHS'''
# aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/MWHS_A.pkl'
'''MWHS'''
# aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/MWTS_A.pkl'
'''SIM'''
# aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/SIM_A.pkl'
'''SSIM'''
# aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/SSIMOBCSL_A.pkl'
'''TRIPM'''
# aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/TRIPM_A.pkl'
'''XEUVI'''
# aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/XEUVI_A.pkl'
'''SEM-HP'''
# aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/SEM_HP_A.pkl'
'''SEM-ME'''
# aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/SEM_ME_A.pkl'
'''SEM-MF'''
# aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/SEM_MF_A.pkl'
'''SEM-MP'''
aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/SEM_MP_A.pkl'
'''SEM-SP'''
# aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/SEM_SP_A.pkl'
'''MERSI'''
# aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/MERSI_A.pkl'
'''HIRAS'''
# aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/HIRAS_A.pkl'
'''AGRI'''
# aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/AGRI_A.pkl'
'''GHI'''
# aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/GHI_A.pkl'
'''GIIRS'''
# aa = '/STSS/FY3E_STSS/dev/AIWarning/YAML/GIIRS_A.pkl'

fA = open(aa, 'wb')
pickle.dump(newdicA, fA, -1)
fA.close()

# 离散数据去重
newdicD = {}
for k, v in dicD.items():
    # print(k)
    v1 = list(set(v))
    # print k, v1
    newdicD[k] = v1
    # print(k, newdic1[k])
print('------------------------------------------')
print(newdicD)

# dd = '/STSS/FY3E_STSS/dev/AIWarning/YAML/WRADC_D.pkl'
'''WRAD'''
# dd = '/STSS/FY3E_STSS/dev/AIWarning/YAML/After_WRADC_D.pkl'
'''GNOS'''
# dd = '/STSS/FY3E_STSS/dev/AIWarning/YAML/GNOS_D.pkl'
'''MWHS'''
# dd = '/STSS/FY3E_STSS/dev/AIWarning/YAML/MWHS_D.pkl'
'''MWHS'''
# dd = '/STSS/FY3E_STSS/dev/AIWarning/YAML/MWTS_D.pkl'
'''SIM'''
# dd = '/STSS/FY3E_STSS/dev/AIWarning/YAML/SIM_D.pkl'
'''SSIM'''
# dd = '/STSS/FY3E_STSS/dev/AIWarning/YAML/SSIMOBCSL_D.pkl'
'''TRIPM'''
# dd = '/STSS/FY3E_STSS/dev/AIWarning/YAML/TRIPM_D.pkl'
'''XEUVI'''
# dd = '/STSS/FY3E_STSS/dev/AIWarning/YAML/XEUVI_D.pkl'
'''SEM-HP'''
# dd = '/STSS/FY3E_STSS/dev/AIWarning/YAML/SEM_HP_D.pkl'
'''SEM-ME'''
# dd = '/STSS/FY3E_STSS/dev/AIWarning/YAML/SEM_ME_D.pkl'
'''SEM-MF'''
# dd = '/STSS/FY3E_STSS/dev/AIWarning/YAML/SEM_MF_D.pkl'
'''SEM-MP'''
dd = '/STSS/FY3E_STSS/dev/AIWarning/YAML/SEM_MP_D.pkl'
'''SEM-SP'''
# dd = '/STSS/FY3E_STSS/dev/AIWarning/YAML/SEM_SP_D.pkl'
'''MERSI'''
# dd = '/STSS/FY3E_STSS/dev/AIWarning/YAML/MERSI_D.pkl'
'''HIRAS'''
# dd = '/STSS/FY3E_STSS/dev/AIWarning/YAML/HIRAS_D.pkl'
'''AGRI'''
# dd = '/STSS/FY3E_STSS/dev/AIWarning/YAML/AGRI_D.pkl'
'''GHI'''
# dd = '/STSS/FY3E_STSS/dev/AIWarning/YAML/GHI_D.pkl'
'''GIIRS'''
# dd = '/STSS/FY3E_STSS/dev/AIWarning/YAML/GIIRS_D.pkl'
fD = open(dd, 'wb')
pickle.dump(newdicD, fD, -1)
fD.close()
