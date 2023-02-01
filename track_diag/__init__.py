# coding=utf8
# -*- coding: utf-8 -*-
import collections
import numpy
import yaml
import glob
import os
import datetime, time
import bottle
import json
import numpy
import h5py
import sys
import re
import math

# import ujson
reload(sys)
sys.setdefaultencoding('utf-8')
from PIL import Image

'''
from netCDF4 import Dataset
import matplotlib.ticker as mticker
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
# import matplotlib.pyplot as plt
# 查看matplotlib所在位置
# print matplotlib.matplotlib_fname()
# 查看matplotlib包含字体
# print(matplotlib.font_manager.fontManager.ttflist)  # 输出所有的字体名
# 配置之后便可使用
matplotlib.rcParams['font.family'] = 'FZFangSong-Z02_GB18030'
matplotlib.rcParams['font.sans-serif'] = ['FZFangSong-Z02_GB18030']
matplotlib.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.sans-serif'] = ['FZFangSong-Z02_GB18030']
plt.rcParams['axes.unicode_minus'] = False
'''

LEV_MAP = {'一级': 1, '二级': 2, '三级': 3, '四级': 4}
DEFAULT = {'level': '-', 'msg': '-', 'time': '-', 'iscur': False}


# 获取根据时间返回各个仪器的名称[目前没有用]
def get_device(request, response, **k):
    # 运行执行文件返回其结果
    # 发送请求的json数据,返回选中的仪器名称FY3E-GNOS
    cfg = request.params
    t = cfg['time']
    # 截取20221123
    t = t[0:4] + t[5:7] + t[8:10]
    filenames = []
    # bn就是'/STSS/FY3E_STSS/dev/system/diag/data/'路径
    bn = os.path.basename
    # print(bn)
    ttt = time.time()
    print("get_device")
    for i in glob.glob('/STSS/FY3E_STSS/system/diag/data/*' + t + '.txt'):
        # bn(i)就只保存到各个告警的文件名称，进行判断是不是3段（3段是各个仪器不带OMB）
        # 判断该告警txt是否为空
        if os.path.getsize(i) != 0:
            a = bn(i).split('_')
            if len(a) == 3:
                filenames.append(bn(i)[:-13])
    # print(filenames)
    print("get_device", time.time() - ttt)
    # 将返回数据进行json序列化
    result = json.dumps(filenames)
    # 通过json格式返回数据
    response.content_type = 'application/json'
    return result


# 获取根据各仪器文件参数决定的各仪器参数名称[目前没有用]
def get_para(request, response, **k):
    # 运行执行文件返回其结果
    # 发送请求的json数据,返回选中的仪器名称FY3E-GNOS
    cfg = request.params.device
    # print(cfg)
    file = '/STSS/FY3E_STSS/dev/system/diag/' + cfg + '.py'
    # file = '/STSS/FY3E_STSS/dev/system/diag/FY3E_SEM.py'
    # print(file)
    # 运行选中文件，获得其生成的信息
    with open(file, 'r') as f:
        line = f.read()
        # print(line)
        # 提取指定字符 提取name=之后的字符,并去除了‘’
        # name = re.findall(r'''name='(.+?)',.+?err_info=diag_core.ErrInfo\(\s+(.+?)\s+\)''',
        name = re.findall(
            r'''name='(.+?)',.+?err_info=diag_core.ErrInfo\((\s*?msg_l(\d)='(.+?)',?|)(\s*?msg_l(\d)='(.+?)',?|)(\s*?msg_l(\d)='(.+?)',?|)\s*?\)''',
            line, flags=re.DOTALL)
    result = []
    for v in name:
        # ('GNOS数字+5V电压遥测', "msg_l1='GNOS数字+5V电压遥测故障',")
        if 'msg' in v[7]:
            result.append(numpy.array([v[0], v[2], v[3], v[5], v[6], v[8], v[9]]).tolist())
        elif 'msg' in v[4]:
            result.append(numpy.array([v[0], v[2], v[3], v[5], v[6]]).tolist())
        else:
            result.append(numpy.array([v[0], v[2], v[3]]).tolist())

    # 将返回数据进行json序列化
    result = json.dumps(result)
    # 通过json格式返回数据
    response.content_type = 'application/json'
    return result


# 用于前台获取时间，并在时间条上进行显示
def get_time(request, **kw):
    times = []
    t0 = datetime.datetime(1970, 1, 1, 0)
    device = request.params.data
    if '单粒子' in device:
        # 通过grep语句进行筛选（出现单粒子的，去掉OK行，进行排序，将文件日期都取出来）
        with os.popen(
                r"grep 单粒子 /STSS/FY3E_STSS/system/diag/data/*txt | grep -v ok | sort | sed -r 's=.+_([0-9]{8}).txt.+=\1=g' | uniq -c") as f:
            for i in f:
                n, t = i.strip().split()
                t = datetime.datetime.strptime(t, '%Y%m%d')
                s = int(n)
                times.append([(t - t0).total_seconds() * 1000, s])
    else:
        for i in sorted(glob.glob(('/STSS/FY3E_STSS/system/diag/data/%s_????????.txt' % device))):
            t = datetime.datetime.strptime(i.split('_')[-1], '%Y%m%d.txt')
            s = 1 if os.path.getsize(i) else 0
            times.append([(t - t0).total_seconds() * 1000, s])

    return dict(time=times)


# 对大量数据进行动态抽样（轨道数据抽样和绘制线段告警数据抽样）
def chour(r, maxlen=200):
    s = r.shape[0]
    # v = int(math.ceil(s / maxlen))
    # return r[::v].tolist()
    pp = (numpy.linspace(0, s - 1, maxlen)).astype('i4') if s > maxlen else slice(None, None)
    return r[pp].tolist()


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


# 读取根据日期决定的数据文件，并返回{[lon,lat,mask,sec]....}格式的数据给前端
def get_files(request, response, **k):
    '''
    # 直接找到对应的二进制文件
    filename = '/ENGIN/ORBIT/IFLSubPointCover%s_FY3E' % t
    # 找到对应时间的二进制文件
    # 各个字段的类型，与结构体对应
    dtype = numpy.dtype([
        ('orbit', '>i4'),
        ('year', '>i4'),
        ('mon', '>i4'),
        ('day', '>i4'),
        ('hour', '>i4'),
        ('min', '>i4'),
        ('info', [('sec', '>f4'),
                  ('lat', '>f4'),
                  ('lon', '>f4'),
                  ('height', '>f4')]),
        ('sol_zen', '>f4'),
        ('lat_l', '>f4'),
        ('lon_l', '>f4'),
        ('lat_r', '>f4'),
        ('lon_r', '>f4')
    ])
    # 读取文件
    with open(filename, 'rb') as f:
        # 跳过前72个字符(文件头)
        f.read(72)
        oo = numpy.fromfile(f, dtype=dtype)

    # 只获取当天的所有数据
    day = oo['day']
    oo = oo[day == int(t[-2:], base=10)]
    # 将sec,lon,lat,height输出
    out = oo['info']
    # 时间进行叠加
    out['sec'] += (oo['hour'] * 3600 + oo['min'] * 60)
    # 将返回数据进行json序列化
    finalfile = json.dumps(out.tolist())
    '''
    # 发送请求的json数据
    cfg = request.params
    # s_time开始时间e_time结束时间,传过来的就是字符串类型，2022-11-23
    s_t = cfg['s_time']
    e_t = cfg['e_time']

    # 读取高发区信息图片数据
    # 利用 img = Image.open(ImgPath) 打开的图片是PIL类型的，需要进行PIL类型到numpy类型转换
    img = Image.open('/STSS/FY3E_STSS/dev/system/stweb/static/img/AREA_CHECK.png')
    # [[[  0   0   0 255],[  0   0   0 255],0为黑色而255是白色
    # convert('L')去除了通道，只保留了[0,255]
    table1 = numpy.array(img.convert('L')) > 128
    # 对应一像素对应几个经纬度信息
    pix_per_deg = 2048 / 360.
    # 数据输出结果保存
    out = []
    # 返回时间条选中的所有时间信息
    time_list = getDatesByTimes(s_t, e_t)
    for u in time_list:
        # 截取20221123
        t = u.replace('-', '')
        filepath = '/FY3E/SEM/L1/HEP/2022/%s/*.HDF' % t
        # print('filepath', filepath)
        filelist = sorted(glob.glob(filepath))
        # print('filelist', filelist)
        # exit()
        for i in filelist:
            with h5py.File(i, 'r') as f:
                # 时间
                hour = f['/Time/Hour'][:]
                minute = f['/Time/Minute'][:]
                second = f['/Time/Second'][:]
                # 经纬度
                lat = f['/Geo/GLAT'][:]
                long = f['/Geo/GLONG'][:]

            # 时间转换为时间戳
            sec = hour * 3600.0 + minute * 60.0 + second
            # mask对应一个像素对应几个经纬度，返回0、1
            mask = table1[((90 - lat) * pix_per_deg).astype('i2'), ((180 + long) * pix_per_deg).astype('i2')]
            # 转置过后就是[long,lat,mask,sec]一样一个，读取一条信息对应四个数值

            # 轨道数据抽样
            data = numpy.array([long, lat, mask, sec], dtype='f4').T
            # 每轨返回的数据包括1200个经纬度信息
            out.append(dict(name=i[-17:-13], data=chour(data, 1200)))

    # 将返回数据进行json序列化
    finalfile = json.dumps(out)
    # 通过json格式返回数据
    response.content_type = 'application/json'
    # print('finalfile', finalfile)
    # json返回只能返回一个参数
    return finalfile


# --------------------------------------------------------todo高发区和全部的告警个数的统计,加在返回result里
# 返回用于绘制线段的告警信息，进行了抽样和分段处理
def get_diag_line(request, response, **k):
    '''
        for fl in filelist:
        with h5py.File(fl, 'r') as f:
            # 时间
            hour = f['/Time/Hour'][:]
            minute = f['/Time/Minute'][:]
            second = f['/Time/Second'][:]
            # 经纬度
            lat = f['/Geo/GLAT'][:]
            long = f['/Geo/GLONG'][:]

            # 时间转换为时间戳
            sec = hour * 3600.0 + minute * 60.0 + second
            # print(sec)
            # 告警信息
            for i in info:
                # 判断该条告警信息有无结束时间,没有结束时间为‘-’,一直返回告警数据
                st = int(i['start']['time'][-8:-6]) * 3600.0 + int(i['start']['time'][-5:-3]) * 60.0 + \
                     int(i['start']['time'][-2:])
                # 有无结束时间
                if len(i['end']['time']) != 1:
                    et = int(i['end']['time'][-8:-6]) * 3600.0 + int(i['end']['time'][-5:-3]) * 60.0 + \
                         int(i['end']['time'][-2:])
                else:
                    et = sec

                print('time', st, et)

                # 时间对应经纬度,返回下标，if是符合开始结束都在范围内
                if st in sec:
                    # 开始结束时间都在sec可找到
                    if et in sec:
                        st_index, = numpy.where(sec == st)
                        et_index, = numpy.where(sec == et)
                        # et_index[0]索引的后一位才是好的数据
                        # print('st_index', st_index, et_index, st_index[0],type(st_index[0]))

                        long1 = long[st_index[0]:(et_index[0] + 1)]
                        lat1 = lat[st_index[0]:(et_index[0] + 1)]
                        # print(long1, lat1)
                        # exit()
                        result.append(dict(name=i['name'], st_time=i['start']['time'].replace('T', ' '),
                                           et_time=i['end']['time'].replace('T', ' '),
                                           msg=i['start']['msg'], level=i['start']['level'],
                                           data=numpy.array([long1, lat1], dtype='f4').T.tolist()))

                    # 类似风场，结束时间不是奇数
                    elif (et - 1) or (et + 1) in sec:
                        st_index, = numpy.where(sec == st)
                        et_index, = numpy.where(sec == (et - 1))
                        # print('st_index', st_index, et_index, st_index[0][0])
                        long1 = long[st_index[0]:(et_index[0] + 1)]
                        lat1 = lat[st_index[0]:(et_index[0] + 1)]
                        # print(long1, lat1)
                        # exit()
                        result.append(dict(name=i['name'], st_time=i['start']['time'].replace('T', ' '),
                                           et_time=i['end']['time'].replace('T', ' '),
                                           msg=i['start']['msg'], level=i['start']['level'],
                                           data=numpy.array([long1, lat1], dtype='f4').T.tolist()))

                    else:
                        st_index, = numpy.where(sec == st)
                        # print('st_index', st_index, et_index, st_index[0][0])
                        long1 = long[st_index[0]:]
                        lat1 = lat[st_index[0]:]
                        # print(long1, lat1)
                        # exit()
                        result.append(dict(name=i['name'], st_time=i['start']['time'].replace('T', ' '),
                                           et_time=i['end']['time'].replace('T', ' '),
                                           msg=i['start']['msg'], level=i['start']['level'],
                                           data=numpy.array([long1, lat1], dtype='f4').T.tolist()))

                # 附近点
                elif (st + 1) or (st - 1) in sec:
                    # 开始结束时间都在sec可找到
                    if et in sec:
                        st_index, = numpy.where(sec == (st + 1))
                        et_index, = numpy.where(sec == et)
                        # et_index[0]索引的后一位才是好的数据
                        # print('st_index', st_index, et_index, st_index[0],type(st_index[0]))

                        long1 = long[st_index[0]:(et_index[0] + 1)]
                        lat1 = lat[st_index[0]:(et_index[0] + 1)]
                        # print(long1, lat1)
                        # exit()
                        result.append(dict(name=i['name'], st_time=i['start']['time'].replace('T', ' '),
                                           et_time=i['end']['time'].replace('T', ' '),
                                           msg=i['start']['msg'], level=i['start']['level'],
                                           data=numpy.array([long1, lat1], dtype='f4').T.tolist()))

                    # 类似风场，结束时间不是奇数
                    elif (et - 1) or (et + 1) in sec:
                        st_index, = numpy.where(sec == (st + 1))
                        et_index, = numpy.where(sec == (et - 1))
                        print('st_index', st_index, et_index)
                        exit()
                        long1 = long[st_index[0]:(et_index[0] + 1)]
                        lat1 = lat[st_index[0]:(et_index[0] + 1)]
                        # print(long1, lat1)
                        # exit()
                        result.append(dict(name=i['name'], st_time=i['start']['time'].replace('T', ' '),
                                           et_time=i['end']['time'].replace('T', ' '),
                                           msg=i['start']['msg'], level=i['start']['level'],
                                           data=numpy.array([long1, lat1], dtype='f4').T.tolist()))

                    else:
                        st_index, = numpy.where(sec == (st + 1))
                        # print('st_index', st_index, et_index, st_index[0][0])
                        long1 = long[st_index[0]:]
                        lat1 = lat[st_index[0]:]
                        # print(long1, lat1)
                        # exit()
                        result.append(dict(name=i['name'], st_time=i['start']['time'].replace('T', ' '),
                                           et_time=i['end']['time'].replace('T', ' '),
                                           msg=i['start']['msg'], level=i['start']['level'],
                                           data=numpy.array([long1, lat1], dtype='f4').T.tolist()))
                else:
                    # 开始结束时间都在sec可找到
                    if et in sec:
                        et_index, = numpy.where(sec == et)
                        # et_index[0]索引的后一位才是好的数据
                        # print('st_index', st_index, et_index, st_index[0],type(st_index[0]))

                        long1 = long[:(et_index[0] + 1)]
                        lat1 = lat[:(et_index[0] + 1)]
                        # print(long1, lat1)
                        # exit()
                        result.append(dict(name=i['name'], st_time=i['start']['time'].replace('T', ' '),
                                           et_time=i['end']['time'].replace('T', ' '),
                                           msg=i['start']['msg'], level=i['start']['level'],
                                           data=numpy.array([long1, lat1], dtype='f4').T.tolist()))

                    # 类似风场，结束时间不是奇数
                    elif (et - 1) or (et + 1) in sec:
                        # st_index, = numpy.where(sec == (st + 1))
                        et_index, = numpy.where(sec == (et - 1))
                        # print('st_index', st_index, et_index, st_index[0][0])
                        long1 = long[:(et_index[0] + 1)]
                        lat1 = lat[:(et_index[0] + 1)]
                        # print(long1, lat1)
                        # exit()
                        result.append(dict(name=i['name'], st_time=i['start']['time'].replace('T', ' '),
                                           et_time=i['end']['time'].replace('T', ' '),
                                           msg=i['start']['msg'], level=i['start']['level'],
                                           data=numpy.array([long1, lat1], dtype='f4').T.tolist()))

                    else:
                        # st_index, = numpy.where(sec == (st + 1))
                        # print('st_index', st_index, et_index, st_index[0][0])
                        long1 = long[:]
                        lat1 = lat[:]
                        # print(long1, lat1)
                        # exit()
                        result.append(dict(name=i['name'], st_time=i['start']['time'].replace('T', ' '),
                                           et_time=i['end']['time'].replace('T', ' '),
                                           msg=i['start']['msg'], level=i['start']['level'],
                                           data=numpy.array([long1, lat1], dtype='f4').T.tolist()))

        '''
    # 获取仪器报警信息
    # 发送请求的json数据
    cfg = request.params
    # device是前端选中告警仪器
    device = cfg['device']
    # time时间,传过来的就是字符串类型，2022-11-23
    s_time = cfg['s_time']
    e_time = cfg['e_time']
    # 获取告警级别(一级、二级、三级)
    diag_level = cfg['diag'].split(',')
    # print(device,s_time,e_time)
    # SEM二进制文件,各个字段的类型，与结构体对应,结构格式
    dtype = numpy.dtype([
        ('orbit', '>i4'),
        ('year', '>i4'),
        ('mon', '>i4'),
        ('day', '>i4'),
        ('hour', '>i4'),
        ('min', '>i4'),
        ('info', [('sec', '>f4'),
                  ('lat', '>f4'),
                  ('lon', '>f4'),
                  ('height', '>f4')]),
        ('sol_zen', '>f4'),
        ('lat_l', '>f4'),
        ('lon_l', '>f4'),
        ('lat_r', '>f4'),
        ('lon_r', '>f4')
    ])
    # 返回时间条选中的所有时间信息
    time_list = getDatesByTimes(s_time, e_time)
    # 保存返回结果
    result = []
    # count用返回选择事件内的告警的个数，初始化
    count = collections.Counter()
    for u in time_list:
        # 截取20221123
        t = u.replace('-', '')
        # filename是告警文件信息
        filename = '/STSS/FY3E_STSS/system/diag/data/' + device + '_' + t + '.txt'
        # print('device', device, filename)
        info = L(filename)
        # print(filename, info)
        # 直接找到对应时间的SEM二进制文件(包含每一秒的经纬度时间等信息)
        filename = '/ENGIN/ORBIT/IFLSubPointCover%s_FY3E' % t
        if not os.path.exists(filename): continue
        # 读取文件
        with open(filename, 'rb') as f:
            # 跳过前72个字符(文件头)
            f.read(72)
            oo = numpy.fromfile(f, dtype=dtype)

        # 只获取当天的所有数据
        day = oo['day']
        oo = oo[day == int(t[-2:], base=10)]
        # 将sec,lon,lat信息输出
        out = oo['info']
        # 时间进行叠加
        sec = out['sec'] + (oo['hour'] * 3600 + oo['min'] * 60)
        long = out['lon']
        lat = out['lat']

        # 告警信息，mask用于累计在相同时间内有哪几个报警故障
        s = int(math.ceil((len(info)) / 8.))
        # print("SSS", math.ceil((len(info)) / 8.))
        mask = numpy.zeros((long.size, s), dtype='u1')
        # 对返回的告警信息循环遍历
        for n, i in enumerate(info):
            # print(i)
            # 告警级别选择
            if str(i['start']['level']) in diag_level:
                # 判断该条告警信息有无结束时间,没有结束时间为‘-’,一直返回告警数据
                tmp_t = i['start']['time']
                # 小于当天时间
                if tmp_t.split('T')[0] < s_time:
                    stindex = 0
                else:
                    stindex = int(tmp_t[-8:-6]) * 3600 + int(tmp_t[-5:-3]) * 60 + int(tmp_t[-2:])
                # 有无结束时间
                if len(i['end']['time']) != 1:
                    tmp_t = i['end']['time']
                    if tmp_t.split('T')[0] > e_time:
                        etindex = None
                    else:
                        etindex = int(tmp_t[-8:-6]) * 3600 + int(tmp_t[-5:-3]) * 60 + int(tmp_t[-2:])
                        if etindex == stindex: etindex += 1
                else:
                    etindex = None
                # divmod--Return the tuple (x//y, x%y)
                ss, nn = divmod(n, 8)
                # print(mask.shape, ss, nn, slice(stindex, etindex))
                mask[slice(stindex, etindex), ss] |= 1 << nn
            else:
                continue

        # 多个告警的位置下标
        point_index = numpy.where((mask[1:] != mask[:-1]).any(1))[0] + 1
        # print(v0, mask[v0])
        start_point = 0
        # print "MASK>0", (mask>0).sum()
        for end_point in point_index.tolist() + [None]:
            maskss = mask[start_point]
            # print(maskss, start_point, end_point)
            now_point = slice(start_point, end_point)
            start_point = end_point  # 下一次循环用的
            if maskss.sum() == 0: continue
            long1 = long[now_point]
            lat1 = lat[now_point]
            sec1 = sec[now_point]

            lnglat = numpy.array([lat1, long1, sec1], dtype='f4').T
            lnglat2 = []
            s = 0
            # 当经纬度距离相差较大时，分成两个点进行绘制（不同轨道）
            for e, in numpy.argwhere(long1[:-1] * long1[1:] < -1000) + 1:
                # print(lat1.size, long1.size, s, e, )
                r = lnglat[s:e]
                # 一个点的时候，构造一个距离极其近的虚假结束位置经纬度坐标
                if r.shape[0] == 1:
                    r = r.repeat(2, 0)
                    r[1, 1] += 0.0001
                lnglat2.append(chour(r))
                s = e
            # 没有结束位置下标，绘制全部数据
            r = lnglat[s:]
            # 一个点的时候，构造一个距离极其近的虚假结束位置经纬度坐标（相同轨道）
            if r.shape[0] == 1:
                r = r.repeat(2, 0)
                r[1, 1] += 0.0001
            lnglat2.append(chour(r))

            # 在相同时间段内将累加告警返回至diags里
            diags = []
            n = -1
            for v in maskss:
                for j in xrange(8):
                    n += 1
                    if v & (1 << j):
                        i = info[n]
                        diags.append(dict(
                            name=i['name'], st_time=i['start']['time'].replace('T', ' '),
                            et_time=i['end']['time'].replace('T', ' '),
                            msg=i['start']['msg'], level=i['start']['level']
                        ))
            for diag_statistic in diags:
                # 字符串化level，因为整数不能作为返回的字典的key
                count.update(str(diag_statistic["level"]))

            result.append(dict(
                data=lnglat2,
                diags=diags,
                count=count
            ))
            # print(result)

    # 将返回数据进行json序列化
    t = time.time()
    print(result)
    diag_info = json.dumps(result)
    print("JSON-DUMPS", time.time() - t)
    # print(diag_info)
    # 通过json格式返回数据
    response.content_type = 'application/json'
    # json返回只能返回一个参数
    return diag_info


# 返回用于绘制开始时间点的告警信息，无需抽样和分段处理，只要开始时间所在位置的经纬度信息
def get_diag_point(request, response, **k):
    # 获取仪器报警信息
    # 发送请求的json数据
    cfg = request.params
    # device是前端选中告警仪器
    device = cfg['device']
    # time时间,传过来的就是字符串类型，2022-11-23
    s_time = cfg['s_time']
    e_time = cfg['e_time']
    # 获取告警级别(一级、二级、三级)
    diag_level = cfg['diag'].split(',')
    # print(device,s_time,e_time)
    # print(diag_level, type(diag_level))
    # SEM二进制文件,各个字段的类型，与结构体对应,结构格式
    dtype = numpy.dtype([
        ('orbit', '>i4'),
        ('year', '>i4'),
        ('mon', '>i4'),
        ('day', '>i4'),
        ('hour', '>i4'),
        ('min', '>i4'),
        ('info', [('sec', '>f4'),
                  ('lat', '>f4'),
                  ('lon', '>f4'),
                  ('height', '>f4')]),
        ('sol_zen', '>f4'),
        ('lat_l', '>f4'),
        ('lon_l', '>f4'),
        ('lat_r', '>f4'),
        ('lon_r', '>f4')
    ])
    # 返回时间条选中的所有时间信息
    time_list = getDatesByTimes(s_time, e_time)
    # 保存返回结果
    result = []
    # count用返回选择事件内的告警的个数,初始化
    count = collections.Counter()
    if '单粒子' in device:
        for u in time_list:
            # 截取20221123
            t = u.replace('-', '')
            # 直接找到对应时间的SEM二进制文件(包含每一秒的经纬度时间等信息)
            filename = '/ENGIN/ORBIT/IFLSubPointCover%s_FY3E' % t
            if not os.path.exists(filename): continue
            # 读取文件
            with open(filename, 'rb') as f:
                # 跳过前72个字符(文件头)
                f.read(72)
                oo = numpy.fromfile(f, dtype=dtype)
            # 只获取当天的所有数据
            day = oo['day']
            oo = oo[day == int(t[-2:], base=10)]
            # 将sec,lon,lat信息输出
            out = oo['info']
            # 时间进行叠加
            # sec = out['sec'] + (oo['hour'] * 3600 + oo['min'] * 60)
            long = out['lon'].tolist()
            lat = out['lat'].tolist()
            with os.popen(r"grep 单粒子 /STSS/FY3E_STSS/system/diag/data/*" + t + ".txt | grep -v ok | sort") as f:
                for m in f:
                    # os.popen文件读出之后转为decode编码前端才能接受
                    m = m.decode('utf-8')
                    yiqi = m.split(':')[0].split('/')[-1][:-13]
                    name = m.split(':')[1][:-14]
                    starttime = m.split(':')[1][-13:] + ':' + m.split(':')[2] + ':' + m.split(':')[3][:2]
                    level = m.split(':')[3][4:]
                    msg = m.split(':')[4][:-2]
                    # print(yiqi, name, starttime, level, msg)
                    # print(type(yiqi), type(name), type(starttime), type(level), type(msg),'unicode')
                    # 告警级别选择
                    if '一' in level:
                        llll = '1'
                    elif '二' in level:
                        llll = '2'
                    else:
                        llll = '3'
                    # print(llll)
                    if llll in diag_level:
                        # 判断该条告警信息有无结束时间,没有结束时间为‘-’,一直返回告警数据
                        # 小于当天时间
                        if starttime.split('T')[0] < s_time:
                            stindex = 0
                        else:
                            stindex = int(starttime[-8:-6]) * 3600 + int(starttime[-5:-3]) * 60 + int(starttime[-2:])
                        diags = dict(name=name, st_time=starttime.replace('T', ' '),
                                     et_time=starttime.replace('T', ' '),
                                     msg=msg, data=[lat[stindex], long[stindex], stindex],
                                     level=llll, yiqi=yiqi)
                        result.append(diags)
                    else:
                        continue
        # --------------------------------------------todo 全部，非高发区统计个数
        for diag_statistic in result:
            # print(diag_statistic)
            # 字符串化level，因为整数不能作为返回的字典的key
            count.update(str(diag_statistic["level"]))
        for eachone in result:
            eachone['count'] = count
        # print(result)
    # 所有仪器单点绘制（全部告警事件，包含单粒子与非单粒子）
    else:
        for u in time_list:
            # 截取20221123
            t = u.replace('-', '')
            # filename是告警文件信息
            filename = '/STSS/FY3E_STSS/system/diag/data/' + device + '_' + t + '.txt'
            # print('device', device, filename)
            info = L(filename)
            # print(filename, info)
            # 直接找到对应时间的SEM二进制文件(包含每一秒的经纬度时间等信息)
            filename = '/ENGIN/ORBIT/IFLSubPointCover%s_FY3E' % t
            if not os.path.exists(filename): continue
            # 读取文件
            with open(filename, 'rb') as f:
                # 跳过前72个字符(文件头)
                f.read(72)
                oo = numpy.fromfile(f, dtype=dtype)

            # 只获取当天的所有数据
            day = oo['day']
            oo = oo[day == int(t[-2:], base=10)]
            # 将sec,lon,lat信息输出
            out = oo['info']
            # 时间进行叠加
            # sec = out['sec'] + (oo['hour'] * 3600 + oo['min'] * 60)
            long = out['lon'].tolist()
            lat = out['lat'].tolist()
            # 告警信息，设置与long等规格是0数组
            # mask = numpy.zeros_like(long, dtype='u8')
            # 对返回的告警信息循环遍历
            for n, i in enumerate(info):
                # print(i)
                # 告警级别选择
                if str(i['start']['level']) in diag_level:
                    # 判断该条告警信息有无结束时间,没有结束时间为‘-’,一直返回告警数据
                    tmp_t = i['start']['time']
                    # 小于当天时间
                    if tmp_t.split('T')[0] < s_time:
                        stindex = 0
                    else:
                        stindex = int(tmp_t[-8:-6]) * 3600 + int(tmp_t[-5:-3]) * 60 + int(tmp_t[-2:])
                    # 不管结束时间
                    etindex = stindex
                    # print('time', stindex, etindex)
                else:
                    continue
                    # for n in range(int(math.log(maskss,2))):
                    #     print(maskss, (1 << n), maskss, type(maskss)(1 << n))
                diags = dict(name=i['name'], st_time=i['start']['time'].replace('T', ' '),
                             et_time=i['end']['time'].replace('T', ' '),
                             msg=i['start']['msg'], data=[lat[stindex], long[stindex], stindex],
                             level=i['start']['level'])
                # 每个点循环append进result
                result.append(diags)

        for diag_statistic in result:
            # print(diag_statistic)
            # 字符串化level，因为整数不能作为返回的字典的key
            count.update(str(diag_statistic["level"]))
        for eachone in result:
            eachone['count'] = count
        # print(result)
    # 将返回数据进行json序列化
    diag_info = json.dumps(result)
    # print(diag_info)
    # 通过json格式返回数据
    response.content_type = 'application/json'
    # json返回只能返回一个参数
    return diag_info


# 针对告警的信息定义了一个从txt读取并去重生成字典的一个Tdiag类和使用的L方法待调用
class Tdiag():
    def __init__(self):
        self._d = [{'time': '2000-01-01 00:00:00', 'level': 0, 'msg': 'ok'}]

    def append(self, time, msg, iscur=False, level=0, **kw):
        d = dict(time=time, msg=msg, iscur=iscur, level=level, **kw)
        self._d.append(d)
        self.o = []

    def mkdate(self, name):
        # print self._d
        self._d.sort(key=lambda v: v.get('time', '0000'))
        d = self._d if self._d[0]['level'] else self._d[1:]
        self.o = []
        cur = None
        print(d, self._d)
        for i in d:
            if cur is None:
                if i['level']:
                    cur = dict(start=i, end=DEFAULT, name=name, iscur=False)  # 新故障
                    self.o.append(cur)

                # else: 重复正常
            else:
                # cur.update(end=i)
                if i['level']:
                    if i['level'] != cur['start']['level']:  # 故障改变
                        cur.update(end=i)
                        cur = dict(start=i, end=DEFAULT, name=name, iscur=False)
                        self.o.append(cur)

                    else:
                        pass  # cur.update(end=i) # 异常持续
                else:
                    # print cur, i
                    cur.update(end=i)  # 故障恢复
                    if i['iscur']:  # 故障恢复 也是当前新的变化, 需要体现
                        cur['iscur'] = True
                        self._warn = True

                    cur = None
        return self.o


import traceback


def L(filename):
    def load(hist):
        if not os.path.exists(hist): raise StopIteration

        with open(hist, 'r') as f:
            for i in f:
                try:
                    a, b, c = i.strip("\n").split(None, 2)
                    l = LEV_MAP.get(c.split(':')[0], 0)
                    if not l:
                        c = 'ok'
                    else:
                        c = c.split(':', 1)[1]
                    yield a, b, c, l
                except:
                    traceback.print_exc()
                    print("ERRORSTR=", i.strip())

    oo = collections.defaultdict(Tdiag)
    last = None
    for a, b, c, l in load(filename):
        if last == (a, l): continue  # 载入去重 不变的情况下, 保留第一条
        last = a, l
        # 时间转换时间戳
        # oo[a].append(time=b, t=numpy.array(b).astype("M8[s]").astype("int32"), msg=c, level=l, iscur=False)
        oo[a].append(time=b, msg=c, level=l, iscur=False)
    ret = []

    for i, j in oo.items():
        ret.extend(j.mkdate(i))

    return ret
