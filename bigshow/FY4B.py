# coding=utf-8
import datetime
import glob
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
STARTTIME = (datetime.datetime.now() - datetime.timedelta(days=14)).strftime("%Y-%m-%d")
# ENDTIME = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime("%Y-%m-%d")
ENDTIME = (datetime.datetime.now()).strftime("%Y-%m-%d")
# UPDATETIME是"qcBusiness"的更新时间，目前写入系统当前时间
UPDATETIME = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# prodList显示不同仪器
prodList = [
    "AGRI",
    "GHI",
    "GIIRS"
]
# 定位图片数量
lOC_PIC_NUM = 2
# 定标图片数量（柱状图，四小图）
CAL1_PIC_NUM = 2
# 定标图片长时间序列图数量
CAL2_PIC_NUM = 1
NAME = "FY-4B L1产品精度"
# 可能以后会改变
SROUCE = "GRAPES"
METHOD = '模拟参考源检验'
SIZE = '83幅全圆盘'

# URL_loc定位精度图片3个列表，每个列表包含2个url图片路径,分别是东西和南北定位图
# AGRI,GHI,GIIRS
URL_loc = [["/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-4B AGRI东西方向偏差.png",
            "/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-4B AGRI南北方向偏差.png"
            ],
           ["/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-4B GHI东西方向偏差.png",
            "/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-4B GHI南北方向偏差.png"
            ],
           ["/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-4B GIIRS东西方向偏差.png",
            "/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-4B GIIRS南北方向偏差.png"
            ]]

# URL_cal定标精度图片3个列表，每个列表包含2个url图片路径,分别是柱状图和四小图（目前GIIRS只显示光谱图）
# AGRI,GHI,GIIRS
URL_cal1 = [["/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-4B AGRI定标精度统计图.png",
             "/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-4B AGRI 第14通道定标精度图.png"
             ],
            ["/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-4B GHI定标精度统计图.png",
             "/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-4B GHI 第3通道定标精度图.png"
             ],
            ["/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-4B GIIRS中波光谱定标精度偏差及标准差.png",
             "/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-4B GIIRS长波光谱定标精度偏差及标准差.png"
             ]]

# URL_cal2定位精度图片3个列表，每个列表包含1/2个url图片路径,时间序列图
# AGRI,GHI,GIIRS（AGRI有两个时间序列图（轮播）,GIIRS没有时间序列图）
URL_cal2 = [
    [
        [
            "/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-4B AGRI 第14通道定标精度当月时间序列图.png",
            "/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-4B AGRI 第14通道定标精度长时间序列图.png",
        ]
    ],
    [
        "/home/shk401/shinetekview-data/fyhn/YFS/QC/FY-4B GHI 第3通道定标精度时间序列图.png"
    ],
    [
        ''
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
    # 传参：仪器名称，开始时间，结束时间
    if name == 'GIIRS':
        st = (datetime.datetime.now() - datetime.timedelta(days=15)).strftime("%Y-%m-%d")
        et = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        time = getDatesByTimes(st, et)
    else:
        time = getDatesByTimes(st, et)
    # print(time)
    cd = []
    # planQuantity应到达 actualQuantity实际到达 successRate成功率
    planQuantity = 0
    actualQuantity = 0
    successRate = 0
    # 柱状图的数值
    chardata_value = []

    # todo 各仪器计划到达文件数量与实际到达文件数量路径不一样，分类讨论
    if name == 'GIIRS':
        # 2022-07-01
        #  todo GIIRS当天有pq数据,aq没有数据，记录前一天数据
        # st = (datetime.datetime.now() - datetime.timedelta(days=15)).strftime("%Y-%m-%d")
        et = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        select_time = et.split('-')
        # print(select_time)
        # 20220701
        path_time = select_time[0] + select_time[1] + select_time[2]
        pq = '/FY4B_DATA/%s/L1/IRDO/REGC/%s/%s/*' % (name, path_time[:4], path_time)
        aq = '/fy4_ads_data/data/FY4B/%s/GRAPES/convert/%s/%s/*' % (name, path_time[:4], path_time)
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

        # 绘制柱状图
        for i in time:
            # 2022-07-01
            select_time = i.split('-')
            # 20220701
            path_time = select_time[0] + select_time[1] + select_time[2]
            aq = '/fy4_ads_data/data/FY4B/%s/GRAPES/convert/%s/%s/*' % (name, path_time[:4], path_time)
            # actualQuantity读取所有.h5文件个数,即为chardata每天的value的值
            actualQuantity = (len(glob.glob(aq)))
            data_value = str(actualQuantity)
            chardata_value.append(data_value)

    elif name == 'AGRI':
        # 2022-07-01
        #  todo AGRI当天有pq,aq数据
        select_time = et.split('-')
        # 20220701
        path_time = select_time[0] + select_time[1] + select_time[2]
        pq = '/FY4B_DATA/%s/L1/FDI/DISK/4000M/%s/%s/*' % (name, path_time[:4], path_time)
        aq = '/fy4_ads_data/data/FY4B/%s/GRAPES/%s/%s/*' % (name, path_time[:4], path_time)
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

        for i in time:
            # 2022-07-01
            select_time = i.split('-')
            # 20220701
            path_time = select_time[0] + select_time[1] + select_time[2]
            aq = '/fy4_ads_data/data/FY4B/%s/GRAPES/%s/%s/*' % (name, path_time[:4], path_time)
            # actualQuantity读取所有.h5文件个数,即为chardata每天的value的值
            actualQuantity = (len(glob.glob(aq)))
            data_value = str(actualQuantity)
            chardata_value.append(data_value)

    else:
        # GHI仪器
        # todo GHI当天有pq,aq数据
        # 2022-07-01
        select_time = et.split('-')
        # 20220701
        path_time = select_time[0] + select_time[1] + select_time[2]
        pq = '/FY4B_DATA/%s/L1/FDI/REGX/2000M/%s/%s/*' % (name, path_time[:4], path_time)
        aq = '/fy4_ads_data/data/FY4B/%s/GRAPES/%s/%s/*' % (name, path_time[:4], path_time)
        # planQuantity读取所有hdf文件个数，actualQuantity读取所有.h5文件个数
        for i in glob.glob(pq):
            # 计划文件只要每个小时前四分钟的文件
            if (('0100_' in i) or ('0200_' in i) or ('0300_' in i) or ('0400_' in i)):
                planQuantity += 1

        # planQuantity = (len(glob.glob(pq)))
        actualQuantity = (len(glob.glob(aq)))
        if planQuantity == 0:
            successRate = str(0) + '%'
        else:
            successRate = float(actualQuantity) / float(planQuantity) * 100
            successRate = str(round(successRate, 2)) + '%'
        planQuantity = str(planQuantity)
        actualQuantity = str(actualQuantity)

        for i in time:
            # 2022-07-01
            select_time = i.split('-')
            # 20220701
            path_time = select_time[0] + select_time[1] + select_time[2]
            aq = '/fy4_ads_data/data/FY4B/%s/GRAPES/%s/%s/*' % (name, path_time[:4], path_time)
            # actualQuantity读取所有.h5文件个数,即为chardata每天的value的值
            actualQuantity = (len(glob.glob(aq)))
            data_value = str(actualQuantity)
            chardata_value.append(data_value)

    for i in range(len(time)):
        cd.append({'name': time[i], 'value': chardata_value[i]})
    #     todo 目前仪器已完成写死100%，'successRate': successRate,实际应到写成plan'actualQuantity': actualQuantity,
    parameters = {'planQuantity': planQuantity, 'actualQuantity': planQuantity,
                  'successRate': '100%',
                  'chartData': cd}
    return parameters


# qcBusiness返回包含所有信息的字典，填写到content-prodList-qcBusiness字段
def qcBusiness(name, uptm):
    # todo 饼状图完成率显示与左图完成率目前一致
    # 调用businessStatistics函数返回的字典，successRate，planQuantity，actualQuantity值与businessStatistics里相同
    parameters = businessStatistics(name, STARTTIME, ENDTIME)
    successRate = parameters['successRate']
    planQuantity = parameters['planQuantity']
    actualQuantity = parameters['actualQuantity']

    # 各个仪器检验时间
    # ENDTIME是当前时间的前一天，如今天2022-07-02，ENDTIME就为2022-07-01
    # 2022-07-01
    # select_time = ENDTIME.split('-')
    # print select_time, name, successRate, planQuantity, actualQuantity
    # 20220701
    # path_time = select_time[0] + select_time[1] + select_time[2]
    # todo GIIRS统计每天convert下边的文件数量，其他仪器统计每天GRAPES文件数量
    if name == 'GIIRS':
        # todo GIIRS只有前一天的文件数据
        et = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        select_time = et.split('-')
        path_time = select_time[0] + select_time[1] + select_time[2]
        file_num = '/fy4_ads_data/data/FY4B/%s/GRAPES/convert/%s/%s/*' % (name, path_time[:4], path_time)
    else:
        select_time = ENDTIME.split('-')
        path_time = select_time[0] + select_time[1] + select_time[2]
        file_num = '/fy4_ads_data/data/FY4B/%s/GRAPES/%s/%s/*' % (name, path_time[:4], path_time)
    # 读取所有file_num路径.h5文件个数
    filelist = (sorted(glob.glob(file_num)))
    # startfile存有文件开始时间，endfile存有文件结束时间
    startfile = filelist[0]
    endfile = filelist[-1]

    # 4B所有仪器的检验源和检验方法都是固定值
    # bTime"qcBusiness"的统计第一个的hdf开始时间，eTime"qcBusiness"的统计的最后一个hdf时间
    if name == 'AGRI':
        bTime = datetime.datetime.strptime(
            startfile.split('/')[-1].split('_')[-3], '%Y%m%d%H%M%S')
        eTime = datetime.datetime.strptime(
            endfile.split('/')[-1].split('_')[-3], '%Y%m%d%H%M%S')
        bTime = str(bTime)
        eTime = str(eTime)

    elif name == 'GIIRS':
        bTime = datetime.datetime.strptime(
            startfile.split('/')[-1].split('_')[-2], '%Y%m%d%H%M%S')
        eTime = datetime.datetime.strptime(
            endfile.split('/')[-1].split('_')[-2], '%Y%m%d%H%M%S')
        bTime = str(bTime)
        eTime = str(eTime)

    else:
        bTime = datetime.datetime.strptime(
            startfile.split('/')[-1].split('_')[-2], '%Y%m%d%H%M%S')
        eTime = datetime.datetime.strptime(
            endfile.split('/')[-1].split('_')[-2], '%Y%m%d%H%M%S')
        bTime = str(bTime)
        eTime = str(eTime)
    # BTIME"qcBusiness"的统计第一个的hdf开始时间，ETIME"qcBusiness"的统计的最后一个hdf时间
    parameters = {'successRate': successRate,
                  "srouce": SROUCE,
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
            # 图片名称要是带.  在使用split无法将名称显示完全，故直接进行截取，舍掉.png
            # name = URL_loc[index][i].split('/')[-1].split('.')[0]
            name = URL_loc[index][i].split('/')[-1][:-4]
            # name = URL_loc[index][i].split('/')[-1].split('.')[0]
            parameters.append({'name': name,
                               "url": URL_loc[index][i]})
    elif picture_name == 'calibration1':
        # 每个仪器的定标图片目前只有3个
        for i in range(CAL1_PIC_NUM):
            # 拆分url路径以获取定位图图片名称
            # 图片名称要是带.  在使用split无法将名称显示完全，故直接进行截取，舍掉.png
            # name = URL_cal[index][i].split('/')[-1].split('.')[0]
            name = URL_cal1[index][i].split('/')[-1][:-4]
            parameters.append({'name': name,
                               "url": URL_cal1[index][i]})
    elif picture_name == 'calibration2':
        # 每个仪器的定标图片目前只有3个
        for i in range(CAL2_PIC_NUM):
            # 拆分url路径以获取定位图图片名称
            # 图片名称要是带.  在使用split无法将名称显示完全，故直接进行截取，舍掉.png
            # name = URL_cal[index][i].split('/')[-1].split('.')[0]
            # 如果时间序列图是个列表，进行判断
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
def picture(index):
    parameters = {
        # 定位和定标分开显示
        'location': picListinfo("location", index),
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
                           'imageList': picture(index),
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
    "page": "研发室-质检展示",
    "content": allinfo(STARTTIME, ENDTIME, UPDATETIME)
})

print(payload)
print(json.loads(payload))
