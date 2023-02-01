# coding=utf-8
import requests
import datetime
import glob
import os
from datetime import timedelta
import datetime
from datetime import date, timedelta
import json
import sys
import io
import math
import random

"""全局变量"""
# STARTTIME，ENDTIME是charData的开始和结束时间，ENDTIME选取当前时间，STARTTIME为ENDTIME前15天时间
# STARTTIME = (datetime.datetime.now() - datetime.timedelta(days=15)).strftime("%Y-%m-%d")
# ENDTIME = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
STARTTIME = (datetime.datetime.now() - datetime.timedelta(days=14)).strftime("%Y-%m-%d")
ENDTIME = (datetime.datetime.now()).strftime("%Y-%m-%d")
# print(STARTTIME, ENDTIME)
# UPDATETIME是"qcBusiness"的更新时间，目前写入系统当前时间
UPDATETIME = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# prodList显示不同仪器
prodList = [
    "MWTS-III",
    "MWHS-II",
    "WindRAD",
    "HIRAS-II",
    "MERSI-LL",
    "GNOS-II",
    "TrilPM",
    "X-EUVI",
    "SEM",
    "SIM",
    "SSIM"
]
lOC_PIC_NUM = 2
CAL1_PIC_NUM = 2
CAL2_PIC_NUM = 1
NAME = "FY-3E L1产品精度"
# 可能会存在改变
METHOD = '模拟参考源检验'
SIZE = '14轨'

# URL_loc定标精度图片11个列表，每个列表包含2个url图片路径,目前没有定位图的位置填了空列表，有可直接添加
URL_loc = [["/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E MWTS-III沿轨方向偏差.png",
            "/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E MWTS-III跨轨方向偏差.png"
            ],
           ["/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E MWHS-II沿轨方向偏差.png",
            "/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E MWHS-II跨轨方向偏差.png"
            ],
           [''],
           [''],
           ["/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E MERSI-LL沿轨方向偏差.png",
            "/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E MERSI-LL跨轨方向偏差.png"
            ],
           [''],
           [''],
           [''],
           [''],
           [''],
           ['']]

# URL_cal定位精度图片11个列表，每个列表包含2个url图片路径,分别是柱状图和四小图
URL_cal1 = [["/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E MWTS-III定标精度统计图.png",
             "/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E MWTS-III通道定标精度时间序列图BIAS.png"
             ],
            ["/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E MWHS-II定标精度统计图.png",
             "/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E MWHS-II第11通道定标精度时间序列图STD.png"
             ],
            ["/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E WindRAD定标精度统计图.png",
             "/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E WindRAD C波段和Ku波段升轨定标偏差图.png"
             ],
            ["/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E HIRAS-II定标精度统计图.png",
             "/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E HIRAS-II辐射定标精度.png"
             ],
            ["/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E MERSI-LL 定标精度统计图.png",
             "/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E MERSI-LL 10.8μm通道辐射定标精度图.png"
             ],
            ["/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E GNOS-II大气掩星事件数量逐日变化.png",
             "/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E GNOS-II电离层掩星事件数量逐日变化.png"
             ],
            ["/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E Tri-IPM定标精度统计图.png",
             "/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E Tri-IPM A探头LBH通道定标精度图.png"
             ],
            ["/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E X-EUVI天与月衰减率监测图.png",
             "/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E X-EUVI年衰减率监测图.png"
             ],
            ["/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E SEM-II定标精度统计图.png",
             "/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E SEM-II磁场总量精度图.png"
             ],
            ["/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E SIM-II定标精度统计图（TIM）.png",
             "/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E SIM-II定标精度时间序列图.png"
             ],
            ["/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E SSIM定标精度统计图.png",
             "/home/shk401/shinetekview-data/fyhn/YFS/QC/2023.31 SSIM与TSIS交叉比对结果原始观测.png"
             ]]

# URL_cal2定位精度图片11个列表，每个列表包含1/2个url图片路径,时间序列图
URL_cal2 = [
    [
        "/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E MWTS-III通道定标精度时间序列图STD.png"
    ],
    [
        "/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E MWHS-II第13通道定标精度时间序列图STD.png"
    ],
    [
        [
            "/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E WindRAD C波段10km升轨定标精度时间序列图.png",
            "/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E WindRAD Ku波段10km升轨定标精度时间序列图.png"
        ]
    ],
    [
        "/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E HIRAS-II辐射定标精度偏差及标准差.png"
    ],
    [
        "/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E MERSI-LL 10.8μm通道定标精度时间序列图(BIAS).png"
    ],
    [
        ""
    ],
    [
        "/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E Tri-IPM A探头LBH通道定标精度时间序列图(BIAS).png"
    ],
    [
        "/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E X-EUVI衰减率时间序列图.png"
    ],
    [
        "/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E SEM-II磁场总量精度时间序列图.png"
    ],
    [
        "/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-3E SIM-II 太阳总辐照度日产品精度时间序列图.png"
    ],
    [
        ""
    ]]


# 根据开始日期、结束日期返回这段时间里所有天的集合
def getDatesByTimes(sDateStr, eDateStr):
    list = []
    datestart = datetime.datetime.strptime(sDateStr, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(eDateStr, '%Y-%m-%d')
    list.append(datestart.strftime('%Y-%m-%d'))
    while datestart < dateend:
        datestart += datetime.timedelta(days=1)
        list.append(datestart.strftime('%Y-%m-%d'))
    # 返回['2022-10-01','2022-10-02'....]
    return list


# businessStatistics返回包含所有信息的字典，填写到content-prodList-businessStatistics字段
def businessStatistics(name, st, et):
    # 通过仪器名称替换查找hdf的路径
    if name == "MWTS-III":
        YQ = "MWTS"
    elif name == "MWHS-II":
        YQ = "MWHS"
    elif name == "WindRAD":
        YQ = "WRAD"
    elif name == "HIRAS-II":
        YQ = "HIRAS"
    elif name == "MERSI-LL":
        YQ = "MERSI"
    elif name == "GNOS-II":
        YQ = "GNOS"
    elif name == "TrilPM":
        YQ = "TRIPM"
    elif name == "X-EUVI":
        YQ = "XEUVI"
    else:
        YQ = name

    # todo 这是各个仪器柱状图时间（SIM,SSIM时间与其他仪器不一样）
    if YQ == 'SIM':
        st = (datetime.datetime.now() - datetime.timedelta(days=16)).strftime("%Y-%m-%d")
        et = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime("%Y-%m-%d")
        time = getDatesByTimes(st, et)
    elif YQ == 'SSIM' or YQ == "TRIPM":
        st = (datetime.datetime.now() - datetime.timedelta(days=15)).strftime("%Y-%m-%d")
        et = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        time = getDatesByTimes(st, et)
    else:
        time = getDatesByTimes(st, et)
    cd = []
    # planQuantity应到达 actualQuantity实际到达 successRate完成率
    planQuantity = 0
    actualQuantity = 0
    successRate = 0
    chardata_value = []

    # todo 每个仪器分类显示计划到达文件数量和实际到达的文件数量
    if YQ == "HIRAS" or YQ == "MERSI":
        # todo "HIRAS" "MERSI"当天存在pq,aq数据文件
        # 2022-07-01
        select_time = et.split('-')
        # 20220701
        path_time = select_time[0] + select_time[1] + select_time[2]
        # 计划应到文件路径：'/FY3E/仪器/1A/OBC/年/年月日',实际到达文件路径：'/STSS/FY3E_STSS/data/FY3E/仪器/GRAPES/年/年月日'
        pq = '/FY3E/%s/1A/OBC/%s/%s/*.HDF' % (YQ, path_time[:4], path_time)
        aq = '/STSS/FY3E_STSS/data/FY3E/%s/GRAPES/%s/%s/*.h5' % (YQ, path_time[:4], path_time)
        # planQuantity读取所有hdf文件个数，actualQuantity读取所有.h5文件个数
        planQuantity = (len(glob.glob(pq)))
        actualQuantity = (len(glob.glob(aq)))

        if planQuantity == 0:
            successRate = str(0) + '%'
        else:
            successRate = float(actualQuantity) / float(planQuantity) * 100
            successRate = str(round(successRate, 2)) + '%'
        # 整型转换成字符串类型
        planQuantity = str(planQuantity)
        actualQuantity = str(actualQuantity)

        # print YQ, planQuantity, actualQuantity, successRate, type(planQuantity), type(actualQuantity)

        # 绘制柱状图数据
        for i in time:
            # 2022-07-01
            select_time = i.split('-')
            # 20220701
            path_time = select_time[0] + select_time[1] + select_time[2]
            # 每日实际到达文件的数量，即为value的值
            aq = '/STSS/FY3E_STSS/data/FY3E/%s/GRAPES/%s/%s/*.h5' % (YQ, path_time[:4], path_time)
            # actualQuantity读取所有.h5文件个数,即为chardata每天的value的值
            actualQuantity = (len(glob.glob(aq)))
            data_value = str(actualQuantity)
            chardata_value.append(data_value)

    elif YQ == "MWHS" or YQ == "MWTS":
        # todo "MWHS" "MWTS"当天存在pq,aq数据文件
        # 2022-07-01
        select_time = et.split('-')
        # 20220701
        path_time = select_time[0] + select_time[1] + select_time[2]
        pq1 = '/FY3E/%s/1A/ASCEND/%s/%s/*.HDF' % (YQ, path_time[:4], path_time)
        pq2 = '/FY3E/%s/1A/DESCEND/%s/%s/*.HDF' % (YQ, path_time[:4], path_time)
        aq = '/STSS/FY3E_STSS/data/FY3E/%s/GRAPES/%s/%s/*.h5' % (YQ, path_time[:4], path_time)
        # planQuantity读取所有hdf文件个数，actualQuantity读取所有.h5文件个数
        planQuantity = (len(glob.glob(pq1)) + len(glob.glob(pq2)))
        actualQuantity = (len(glob.glob(aq)))
        if planQuantity == 0:
            successRate = str(0) + '%'
        else:
            successRate = float(actualQuantity) / float(planQuantity) * 100
            successRate = str(round(successRate, 2)) + '%'
        planQuantity = str(planQuantity)
        actualQuantity = str(actualQuantity)

        # print YQ, planQuantity, actualQuantity, successRate, type(planQuantity), type(actualQuantity)

        for i in time:
            # 2022-07-01
            select_time = i.split('-')
            # 20220701
            path_time = select_time[0] + select_time[1] + select_time[2]
            aq = '/STSS/FY3E_STSS/data/FY3E/%s/GRAPES/%s/%s/*.h5' % (YQ, path_time[:4], path_time)
            # actualQuantity读取所有.h5文件个数,即为chardata每天的value的值
            actualQuantity = (len(glob.glob(aq)))
            data_value = str(actualQuantity)
            chardata_value.append(data_value)

    elif YQ == "GNOS":
        # todo "GNOS" 当天存在pq,aq数据文件
        # 2022-07-01
        select_time = et.split('-')
        # 20220701
        path_time = select_time[0] + select_time[1] + select_time[2]
        pq = '/FY3E/%s/1A/OBC/%s/%s/*.HDF' % (YQ, path_time[:4], path_time)
        aq = '/STSS/FY3E_STSS/system/stweb/data/gcyc/FY3E_%s/%s/*.h5' % (YQ, path_time)
        # planQuantity读取所有hdf文件个数，actualQuantity读取所有.h5文件个数
        planQuantity = (len(glob.glob(pq)))
        actualQuantity = (len(glob.glob(aq)))
        if planQuantity == 0:
            successRate = str(0) + '%'
        else:
            successRate = float(actualQuantity) / float(planQuantity) * 100
            successRate = str(round(successRate, 2)) + '%'
        planQuantity = str(planQuantity)
        actualQuantity = str(actualQuantity)

        # print YQ, planQuantity, actualQuantity, successRate, type(planQuantity), type(actualQuantity)

        for i in time:
            # 2022-07-01
            select_time = i.split('-')
            # 20220701
            path_time = select_time[0] + select_time[1] + select_time[2]
            aq = '/STSS/FY3E_STSS/system/stweb/data/gcyc/FY3E_%s/%s/*.h5' % (YQ, path_time)
            # actualQuantity读取所有.h5文件个数,即为chardata每天的value的值
            actualQuantity = (len(glob.glob(aq)))
            data_value = str(actualQuantity)
            chardata_value.append(data_value)

    elif YQ == "WRAD":
        # todo "WRAD" 当天存在pq,aq数据文件
        # 2022-07-01
        select_time = et.split('-')
        # 20220701
        path_time = select_time[0] + select_time[1] + select_time[2]
        pq = '/FY3E/%s/1A/OBC/*C/%s/%s/*.HDF' % (YQ, path_time[:4], path_time)
        # todo 目前只写了C轨的数据
        aq1 = '/STSS/FY3E_STSS/data/FY3E/%s/SIM/ASCENDC/%s/%s/*.HDF' % (YQ, path_time[:4], path_time)
        aq2 = '/STSS/FY3E_STSS/data/FY3E/%s/SIM/DESCENDC/%s/%s/*.HDF' % (YQ, path_time[:4], path_time)
        # planQuantity读取所有hdf文件个数，actualQuantity读取所有.h5文件个数
        planQuantity = (len(glob.glob(pq)))
        actualQuantity = (len(glob.glob(aq1)) + len(glob.glob(aq2)))
        if planQuantity == 0:
            successRate = str(0) + '%'
        else:
            successRate = float(actualQuantity) / float(planQuantity) * 100
            successRate = str(round(successRate, 2)) + '%'
        planQuantity = str(planQuantity)
        actualQuantity = str(actualQuantity)

        # print YQ, planQuantity, actualQuantity, successRate, type(planQuantity), type(actualQuantity)

        for i in time:
            # 2022-07-01
            select_time = i.split('-')
            # 20220701
            path_time = select_time[0] + select_time[1] + select_time[2]
            # todo
            aq = '/STSS/FY3E_STSS/data/FY3E/%s/SIM/*C/%s/%s/*.HDF' % (YQ, path_time[:4], path_time)
            # actualQuantity读取所有.h5文件个数,即为chardata每天的value的值
            actualQuantity = (len(glob.glob(aq)))
            data_value = str(actualQuantity)
            chardata_value.append(data_value)

    elif YQ == "SEM":
        # todo "SEM" 当天存在pq,aq数据文件
        # 2022-07-01
        select_time = et.split('-')
        # 20220701
        path_time = select_time[0] + select_time[1] + select_time[2]
        pq = '/FY3E/%s/1A/HPOBC/%s/%s/*.HDF' % (YQ, path_time[:4], path_time)
        aq = '/STSS/FY3E_STSS/system/stweb/data/gcyc/FY3E_%s/%s/*.h5' % (YQ, path_time)
        # planQuantity读取所有hdf文件个数，actualQuantity读取所有.h5文件个数
        planQuantity = (len(glob.glob(pq)))
        actualQuantity = (len(glob.glob(aq)))
        if planQuantity == 0:
            successRate = str(0) + '%'
        else:
            successRate = float(actualQuantity) / float(planQuantity) * 100
            successRate = str(round(successRate, 2)) + '%'
        planQuantity = str(planQuantity)
        actualQuantity = str(actualQuantity)

        # print YQ, planQuantity, actualQuantity, successRate, type(planQuantity), type(actualQuantity)

        for i in time:
            # 2022-07-01
            select_time = i.split('-')
            # 20220701
            path_time = select_time[0] + select_time[1] + select_time[2]
            aq = '/STSS/FY3E_STSS/system/stweb/data/gcyc/FY3E_%s/%s/*.h5' % (YQ, path_time)
            # actualQuantity读取所有.h5文件个数,即为chardata每天的value的值
            actualQuantity = (len(glob.glob(aq)))
            data_value = str(actualQuantity)
            chardata_value.append(data_value)

    elif YQ == "SIM":
        # 2022-07-01
        # todo SIM每次只有前天的数据
        et = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime("%Y-%m-%d")
        select_time = et.split('-')
        # 20220701
        path_time = select_time[0] + select_time[1] + select_time[2]
        pq = '/FY3E/%s/1A/%s/%s/*.HDF' % (YQ, path_time[:4], path_time)
        aq = '/STSS/FY3E_STSS/system/stweb/data/gcyc/FY3E_%s/%s/*.h5' % (YQ, path_time)
        # planQuantity读取所有hdf文件个数，actualQuantity读取所有.h5文件个数
        planQuantity = (len(glob.glob(pq)))
        actualQuantity = (len(glob.glob(aq)))
        if planQuantity == 0:
            successRate = str(0) + '%'
        else:
            successRate = float(actualQuantity) / float(planQuantity) * 100
            successRate = str(round(successRate, 2)) + '%'
        planQuantity = str(planQuantity)
        actualQuantity = str(actualQuantity)

        # print YQ, planQuantity, actualQuantity, successRate, type(planQuantity), type(actualQuantity)

        # todo SIM的柱状图time的开始时间和结束时间跟其他仪器不一样
        for i in time:
            # 2022-07-01
            select_time = i.split('-')
            # 20220701
            path_time = select_time[0] + select_time[1] + select_time[2]
            aq = '/STSS/FY3E_STSS/system/stweb/data/gcyc/FY3E_%s/%s/*.h5' % (YQ, path_time)
            # actualQuantity读取所有.h5文件个数,即为chardata每天的value的值
            actualQuantity = (len(glob.glob(aq)))
            data_value = str(actualQuantity)
            chardata_value.append(data_value)

    elif YQ == "SSIM":
        # todo "SSIM" 最近只存在前天存在pq,存在当天aq数据文件
        # 2022-07-01
        et = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        select_time = et.split('-')
        # 20220701
        path_time = select_time[0] + select_time[1] + select_time[2]
        pq = '/FY3E/%s/1A/OBC*/%s/%s/*.HDF' % (YQ, path_time[:4], path_time)
        aq = '/STSS/FY3E_STSS/system/stweb/data/gcyc/FY3E_%s/%s/*.h5' % (YQ, path_time)
        # planQuantity读取所有hdf文件个数，actualQuantity读取所有.h5文件个数
        # planQuantity = (len(glob.glob(pq + '/*.HDF')))
        # actualQuantity = (len(glob.glob(aq + '/*.h5')))

        pq_list = glob.glob(pq)
        aq_list = glob.glob(aq)

        for i in pq_list:
            shijian1 = i.split('/')[-1].split('_')[-3]
            for j in aq_list:
                shijain2 = j.split('/')[-1].split('_')[-2]
                if shijain2 == shijian1:
                    planQuantity += 1
                    actualQuantity += 1
                elif shijain2 == '0000':
                    pass

        # print planQuantity, actualQuantity
        if planQuantity == 0:
            successRate = str(0) + '%'
        else:
            successRate = float(actualQuantity) / float(planQuantity) * 100
            successRate = str(round(successRate, 2)) + '%'
        planQuantity = str(planQuantity)
        actualQuantity = str(actualQuantity)

        # print YQ, planQuantity, actualQuantity, successRate, type(planQuantity), type(actualQuantity)

        for i in time:
            actualQuantity = 0
            # 2022-07-01
            select_time = i.split('-')
            # 20220701
            path_time = select_time[0] + select_time[1] + select_time[2]
            aq = '/STSS/FY3E_STSS/system/stweb/data/gcyc/FY3E_%s/%s/*.h5' % (YQ, path_time)
            # actualQuantity读取所有.h5文件个数,即为chardata每天的value的值
            # actualQuantity = (len(glob.glob(aq + '/*.h5')))
            aq_list = glob.glob(aq)
            for j in aq_list:
                shijain2 = j.split('/')[-1].split('_')[-2]
                if shijain2 == '0000':
                    pass
                else:
                    actualQuantity += 1

            data_value = str(actualQuantity)
            chardata_value.append(data_value)

    elif YQ == "TRIPM":
        # todo "TRIPM" 存在当天pq数据，当前时间的前一天存在aq数据文件
        # 2022-07-01
        et = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        select_time = et.split('-')
        # 20220701
        path_time = select_time[0] + select_time[1] + select_time[2]
        pq = '/FY3E/%s/1A/%s/%s/*.HDF' % (YQ, path_time[:4], path_time)
        aq = '/STSS/FY3E_STSS/system/stweb/data/gcyc/FY3E_%s/%s/*.h5' % (YQ, path_time)
        # planQuantity读取所有hdf文件个数，actualQuantity读取所有.h5文件个数
        planQuantity = (len(glob.glob(pq)))
        actualQuantity = (len(glob.glob(aq)))
        if planQuantity == 0:
            successRate = str(0) + '%'
        else:
            successRate = float(actualQuantity) / float(planQuantity) * 100
            successRate = str(round(successRate, 2)) + '%'
        planQuantity = str(planQuantity)
        actualQuantity = str(actualQuantity)

        # print YQ, planQuantity, actualQuantity, successRate, type(planQuantity), type(actualQuantity)

        for i in time:
            # 2022-07-01
            select_time = i.split('-')
            # 20220701
            path_time = select_time[0] + select_time[1] + select_time[2]
            aq = '/STSS/FY3E_STSS/system/stweb/data/gcyc/FY3E_%s/%s/*.h5' % (YQ, path_time)
            # actualQuantity读取所有.h5文件个数,即为chardata每天的value的值
            actualQuantity = (len(glob.glob(aq)))
            data_value = str(actualQuantity)
            chardata_value.append(data_value)

    elif YQ == "XEUVI":
        # todo "XEUVI" 存在当天pq，aq数据文件
        # 2022-07-01
        select_time = et.split('-')
        # 20220701
        path_time = select_time[0] + select_time[1] + select_time[2]
        pq = '/FY3E/%s/1A/GRAN/%s/%s/*.HDF' % (YQ, path_time[:4], path_time)
        aq = '/STSS/FY3E_STSS/system/stweb/data/gcyc/FY3E_%s/%s/*.h5' % (YQ, path_time)
        # planQuantity读取所有hdf文件个数，actualQuantity读取所有.h5文件个数
        planQuantity = (len(glob.glob(pq)))
        actualQuantity = (len(glob.glob(aq)))

        if planQuantity == 0:
            successRate = str(0) + '%'
        else:
            successRate = float(actualQuantity) / float(planQuantity) * 100
            successRate = str(round(successRate, 2)) + '%'
        planQuantity = str(planQuantity)
        actualQuantity = str(actualQuantity)

        # print YQ, planQuantity, actualQuantity, successRate, type(planQuantity), type(actualQuantity)

        for i in time:
            # 2022-07-01
            select_time = i.split('-')
            # 20220701
            path_time = select_time[0] + select_time[1] + select_time[2]
            aq = '/STSS/FY3E_STSS/system/stweb/data/gcyc/FY3E_%s/%s/*.h5' % (YQ, path_time)
            # actualQuantity读取所有.h5文件个数,即为chardata每天的value的值
            actualQuantity = (len(glob.glob(aq)))
            data_value = str(actualQuantity)
            chardata_value.append(data_value)

    for i in range(len(time)):
        cd.append({'name': time[i], 'value': chardata_value[i]})
    parameters = {'planQuantity': planQuantity, 'actualQuantity': actualQuantity,
                  'successRate': successRate,
                  'chartData': cd}
    return parameters


# print businessStatistics('SSIM', STARTTIME, ENDTIME)


# qcBusiness返回包含所有信息的字典，填写到content-prodList-qcBusiness字段
def qcBusiness(name, uptm):
    # 通过仪器名称替换查找hdf的路径
    if name == "MWTS-III":
        YQ = "MWTS"
    elif name == "MWHS-II":
        YQ = "MWHS"
    elif name == "WindRAD":
        YQ = "WRAD"
    elif name == "HIRAS-II":
        YQ = "HIRAS"
    elif name == "MERSI-LL":
        YQ = "MERSI"
    elif name == "GNOS-II":
        YQ = "GNOS"
    elif name == "TrilPM":
        YQ = "TRIPM"
    elif name == "X-EUVI":
        YQ = "XEUVI"
    else:
        YQ = name
    # 调用businessStatistics函数返回的字典，successRate，planQuantity，actualQuantity值与businessStatistics里相同
    # todo 饼状图里显示完成率与左侧完成率目前一致
    parameters = businessStatistics(YQ, STARTTIME, ENDTIME)
    successRate = parameters['successRate']
    planQuantity = parameters['planQuantity']
    actualQuantity = parameters['actualQuantity']

    # WindRAD和其他仪器检验源不一样进行细分
    if "WindRAD" == name:
        srouce = "EC"
    else:
        srouce = "GRAPES"

    # 各个仪器检验时间
    # ENDTIME是当前时间的前一天，如今天2022-07-02，ENDTIME就为2022-07-01
    # 2022-07-01
    # todo SIM仪器只有前天的文件,SSIM和TRIPM仪器只有昨天文件，其他仪器正常
    if YQ == 'SIM':
        et = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime("%Y-%m-%d")
        select_time = et.split('-')
    elif YQ == 'SSIM' or YQ == "TRIPM":
        et = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        select_time = et.split('-')
    else:
        select_time = ENDTIME.split('-')
    # 20220701
    path_time = select_time[0] + select_time[1] + select_time[2]
    file_num = '/STSS/FY3E_STSS/system/stweb/data/gcyc/FY3E_%s/%s/*.h5' % (YQ, path_time)
    # 读取所有file_num路径.h5文件个数
    filelist = (sorted(glob.glob(file_num)))
    # print filelist
    # startfile存有文件开始时间，endfile存有文件结束时间
    startfile = filelist[0]
    endfile = filelist[-1]

    # 开始文件的年月日startfile.split('/')[-1].split('_')[-3]，时分startfile.split('/')[-1].split('_')[-2]
    # 结束文件的年月日endfile.split('/')[-1].split('_')[-3]，时分endfile.split('/')[-1].split('_')[-2]

    bTime = datetime.datetime.strptime(
        startfile.split('/')[-1].split('_')[-3] + startfile.split('/')[-1].split('_')[-2], '%Y%m%d%H%M')
    eTime = datetime.datetime.strptime(
        endfile.split('/')[-1].split('_')[-3] + endfile.split('/')[-1].split('_')[-2], '%Y%m%d%H%M')
    bTime = str(bTime)
    eTime = str(eTime)
    # BTIME"qcBusiness"的统计第一个的hdf开始时间，ETIME"qcBusiness"的统计的最后一个hdf时间
    parameters = {'successRate': successRate,
                  "srouce": srouce,
                  'planQuantity': planQuantity,
                  'actualQuantity': actualQuantity,
                  "bTime": bTime,
                  "eTime": eTime,
                  'method': METHOD,
                  'updateTime': uptm,
                  'size': SIZE
                  }
    return parameters


# prodListinfo返回包含所有信息的字典到picture，填写到content-prodList-picList字段
def picListinfo(picture_name, index):
    parameters = []
    if picture_name == 'location':
        # 每个仪器的定位图片目前只有2个
        for i in range(lOC_PIC_NUM):
            # 拆分url路径以获取定位图图片名称
            # 10.8通道也会带.，使用split无法将名称显示完全，故直接进行截取，舍掉.png
            # name = URL_loc[index][i].split('/')[-1].split('.')[0]
            name = URL_loc[index][i].split('/')[-1][:-4]
            parameters.append({'name': name,
                               "url": URL_loc[index][i]})
    elif picture_name == 'calibration1':
        # 每个仪器的定标图片目前只有3个
        for i in range(CAL1_PIC_NUM):
            # 拆分url路径以获取定位图图片名称
            # 10.8通道也会带.，使用split无法将名称显示完全，故直接进行截取，舍掉.png
            # name = URL_cal[index][i].split('/')[-1].split('.')[0]
            name = URL_cal1[index][i].split('/')[-1][:-4]
            parameters.append({'name': name,
                               "url": URL_cal1[index][i]})
    elif picture_name == 'calibration2':
        # 每个仪器的定标图片目前只有3个
        for i in range(CAL2_PIC_NUM):
            # 拆分url路径以获取定位图图片名称
            # 10.8通道也会带.，使用split无法将名称显示完全，故直接进行截取，舍掉.png
            # name = URL_cal[index][i].split('/')[-1].split('.')[0]
            if isinstance(URL_cal2[index][i], list):
                for j in range(len(URL_cal2[index][i])):
                    name = URL_cal2[index][i][j].split('/')[-1][:-4]
                    parameters.append({'name': name,
                                       "url": URL_cal2[index][i][j]})
            else:
                name = URL_cal2[index][i].split('/')[-1][:-4]
                parameters.append({'name': name,
                                   "url": URL_cal2[index][i]})
    return parameters


# picture返回包含所有prodListinfo返回信息的字典，填写到content-prodList-picList字段
def picture(name, index):
    # 分仪器讨论，目前只有MWTS-III，MWHS-II，MERSI-LL三个仪器存在定位图
    if "MWTS-III" == name or "MWHS-II" == name or "MERSI-LL" == name:
        parameters = {
            # 定位和定标分开显示
            'location': picListinfo("location", index),
            "calibration1": picListinfo("calibration1", index),
            "calibration2": picListinfo("calibration2", index)
        }
    # 没有定位图的仪器在第二个定位图字段先给了个无用字段
    else:
        parameters = {
            # 定位和定标分开显示
            # location没有就给个空列表
            'location': [],
            "calibration1": picListinfo("calibration1", index),
            "calibration2": picListinfo("calibration2", index)
        }
    return parameters


# 返回content-prodList字段所有内容
def prodListinfo(charstart, charend, uptm):
    parameters = []
    for i in prodList:
        index = prodList.index(i)
        parameters.append({'prod': i,
                           'imageList': picture(i, index),
                           "businessStatistics": businessStatistics(i, charstart, charend),
                           "qcBusiness": qcBusiness(i, uptm)})
    return parameters


# 将全部信息写入字典，填写到json-content字段里面
def allinfo(charstart, charend, uptm):
    dic = {
        'name': NAME,
        "prodList": prodListinfo(charstart, charend, uptm)
    }
    return dic


# 最终大概格式，json绑定
payload = json.dumps({
    "page": "研发室-L1质量检测平台FY3E",
    "content": allinfo(STARTTIME, ENDTIME, UPDATETIME)
})

# print (allinfo(STARTTIME, ENDTIME, UPDATETIME))
print(payload)
print(json.loads(payload))
