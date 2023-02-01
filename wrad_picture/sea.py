# coding=utf-8
path = 'data/wrad/sea/noc/FY3E_WindRad_{s1}_{s2}_{s6}_{s4}_{s3}_{s5}.bin'
import numpy
import _plots
import time

WVCSIZE = {
  '10km': 140, '20km': 70, '2.5km': 561
}
import glob, os


def listfiles(request, response, **kw):
  files = glob.glob("data/wrad/sea/NOC/FY3E_WindRad_*%s*" % request.params.mask)
  bn = os.path.basename
  # pars = collections.defaultdict()
  # for i in files:
  #     bn(i)[:-4].split()
  return dict(files=files)


def SEA_DATA(s4='', s6='', **kwargs):
  if 'wvc' in s6:
    size = WVCSIZE[s4]
  return numpy.dtype([('t', 'f8'), ('d', 'f4', size)])


class SeaData():
  def __init__(self, filename):
    size = 61
    sat, ins, a, b, c, d, e, f = os.path.basename(filename[:-4]).split('_')
    if 'wvc' in filename:
      size = WVCSIZE[d]
      self.data = self.wcv_data
    else:
      self.data = self.agl_data
    dtype = numpy.dtype([('t', 'f8'), ('d', 'f4', size)])
    d = numpy.fromfile(filename, dtype)
    t = d['t']
    mask = t > 10
    self.d = d[mask]['d']
    self.t = t[mask]


  def agl_data(self, s, e, start=None, end=None, **kw):
    m = numpy.ones_like(self.t, dtype=bool)
    # print start
    # print type(start)
    start=time.strptime(start, '%Y-%m-%d')
    start=time.mktime(start)

    end = time.strptime(end, '%Y-%m-%d')
    end=time.mktime(end)
    # print start,end
    # print type(start),type(end)
    if start: m &= self.t > start
    if end: m &= self.t <= end
    return self.d[:, s - 10:e - 10][m], s, e, self.t[m]

  def wcv_data(self, s, e, start=None, end=None, **kw):
    m = numpy.ones_like(self.t, dtype=bool)
    start = time.strptime(start, '%Y-%m-%d')
    start = time.mktime(start)

    end = time.strptime(end, '%Y-%m-%d')
    end = time.mktime(end)
    # print start, end
    # print type(start), type(end)
    if start: m &= self.t >= start
    if end: m &= self.t <= end
    return self.d[m, s:e], s, e, self.t[m]


def get_seatime(request, response, **k):
  data = SeaData(request.params.filename)
  return dict(data=[[i, 1] for i in (data.t * 1000).tolist()])


def get_sea_agl(request, response, **k):
  d, s, e, t = sea_data(request, response)
  return dict(
    legend=[i.strftime('%Y%m%d') for i in t.astype('M8[s]').tolist()],
    series=d.tolist(),
    x=range(s, e)
  )


def get_sea_time(request, response, **k):
  d, s, e, t = sea_data(request, response)

  return dict(
    legend=[u'%d°' % (i) for i in range(s, e)],
    series=d.T.tolist(),
    x=(t * 1e3).tolist()
  )


def sea_data(request, response):
  cf = request.json
  data = SeaData(cf['filename'])
  d, s, e, t = data.data(**cf)
  return d, s, e, t


# Echart转死图片
def get_sea_time_img(request, response, **k):
  d, s, e, t = sea_data(request, response)
  # print d,t
  req = request.json
  # print req
  from collections import namedtuple
  import _stat

  D = namedtuple('Data', 'x,mean,dx,squeeze')
  # data = [D(_stat._plots.s2num(t), i) for i in d.T]
  data = [D(_stat._plots.s2num(t), i, 1, lambda: None) for i in d.T]
  # print data

  # D = namedtuple('Data', 'x,mean')
  # data = [D(_stat._plots.s2num(t), i) for i in d.T]

  if 'wvc' in req['filename']:
    legend = [u'%d' % (i) for i in range(s, e)]
  else:
    legend = [u'%d°' % (i) for i in range(s, e)]
  # print legend--随入射角变化分布图标


  fig = _plots.N_LinesFig(1, 'Time Series of Sigma0 difference (NOC)', rl=0.6, dh=0.6, sh=2, rw=5.1)
  ax = fig.axes[0]
  # 决定绘制线的个数
  dim = e - s
  # print dim
  # print len(data[0][1]),data[0][1][1]

  # 去除data数据里为填充值的时间数据
  line = []
  for i in range(dim):
    for j in range(len(data[i][1])):
      if data[i][1][j] == -999:
         data[i][1][j] = numpy.nan
    line.extend(ax.plot(data[i][0], data[i][1], linestyle='-', marker='o',ms=1.5))

  # 绘制图标
  ax.legend(line, legend)
  # 将x轴绘制显示时间为日期格式
  ax.x_datetime_ticks()

  ax.title(req['subtext'], loc='left')
  ax.xlabel('Time(day)', fontsize=10)
  ax.ylabel('Diff(dB)', fontsize=10)

  title = req['subtext'].split(' ')

  # 返回图像格式
  response.content_type = 'image/png'
  response.download = 'Time Series of Sigma0 difference (NOC)'+'_'+title[0]
  return fig.save_png()


def get_sea_picture(request, response, **k):
  # d, s, e, t = sea_data(request, response)
  # d是数据，s是起始，e是结束，t是时间
  # print d,s,e,t
  req = request.json
  # print req

  fig = _plots.N_LinesFig(1, 'Incidence Angle Distribute of Sigma0 difference (NOC)', rl=0.6, dh=0.6, sh=2, rw=5.1)
  ax = fig.axes[0]

  # 网格数据直接画出，该数据就是已经14天出一次的数据了
  if 'wvc' in req['filename']:
    d, s, e, t = sea_data(request, response)
    # d是数据，s是起始，e是结束，t是时间
    # print d,s,e,t
    # req = request.json
    # print req
    legend = [i.strftime('%Y%m%d') for i in t.astype('M8[s]').tolist()]
    # print legend
    # series为所有入射开始至结束的数据
    series = d.tolist()
    # print series
    # print len(series[0])
    # print len(series), series

    # print req['filename']
    # 横坐标范围
    x = range(s, e)

    line = []
    for i in range(len(series)):
      line.extend(ax.plot(x, series[i], linestyle='-', marker='o',ms=1.5))


    ax.legend(line, legend)
    # ax.x_datetime_ticks()
    ax.title(req['subtext'], loc='left')
    ax.xlabel(req['clslabel'], fontsize=10)
    ax.ylabel('Diff(dB)', fontsize=10)
    title = req['subtext'].split(' ')

  # 入射角数据，间隔自定义，间隔x天画一条线
  else:
    d, s, e, t = sea_data(request, response)
    # d是数据，s是起始，e是结束，t是时间
    # print d,s,e,t

    # 不存在空缺值
    legend = [i.strftime('%Y%m%d') for i in t.astype('M8[s]').tolist()]
    # print legend
    # series为所有入射开始至结束的数据
    series = d.tolist()
    # print series
    # print len(series[0])
    # print len(series), series

    # 获取间隔时间
    space = int(req['space'])
    # 设置成根据输入的间隔时间画图
    series_count = series[::space]
    # print series_count, len(series_count)
    legend_count = legend[::space]

    # print len(series), series
    # print len(series_count), series_count

    # 横坐标范围
    x = range(s, e)
    # print x

    # 去除填充值
    for i in range(len(series_count)):
      for j in range(len(x)):
        if series_count[i][j] == -999:
          series_count[i][j] = numpy.nan

    # print series_count

    # 开始时间
    start = req['start']
    # print start
    # print type(start)
    import time
    start = time.strptime(start, '%Y-%m-%d')
    start = time.mktime(start)
    # print start
    # print type(start)
    # 距离开始的时间间隔
    time = t - start
    # print time, len(time)
    # 转换成天数，距离开始多少天
    day = time / 86400
    # print day
    # print len(day)
    # 根据时间间隔划分出，len(count)有几条记录,与series_count一样
    count = day / space
    # print count
    # 取第几个，根据sel进行是否存在跳跃绘制的筛选
    sel = day % space
    # print sel


    # 存在空缺数据，直接跳过，根据sel里边是否有1，来进行判断是连续绘制还是跳跃绘制
    if 1 in sel:
      # 绘图
      line = []
      leg=[]

      # 去除填充值
      for i in range(len(sel)):
        for j in range(len(x)):
          if series[i][j] == -999:
            series[i][j] = numpy.nan


      # 相当于跳过空缺值
      for i in range(len(sel)):
        if sel[i] == 1:
          line.extend(ax.plot(x, series[i], linestyle='-', marker='o',ms=1.5))
          leg.append(legend[i])

      # 绘制线与图标匹配
      for i in range(len(sel)):
        if sel[i] == 1:
          ax.legend(line, leg)



      # ax.x_datetime_ticks()
      ax.title(req['subtext'], loc='left')
      ax.xlabel(req['clslabel'], fontsize=10)
      ax.ylabel('Diff(dB)', fontsize=10)
      title = req['subtext'].split(' ')



    else:
      # 绘图
      line = []
      for i in range(len(series_count)):
        line.extend(ax.plot(x, series_count[i], linestyle='-', marker='o',ms=1.5))

      ax.legend(line, legend_count)
      # ax.x_datetime_ticks()
      ax.title(req['subtext'], loc='left')
      ax.xlabel(req['clslabel'], fontsize=10)
      ax.ylabel('Diff(dB)', fontsize=10)
      title = req['subtext'].split(' ')

  # 返回图片格式
  response.content_type = 'image/png'
  response.download = 'Incidence Angle Distribute of Sigma0 difference(NOC)'+'_'+title[0]
  return fig.save_png()


#
#  todo  ： 多选数据绘图的问题
# todo  ： WCV 网格 数据结构动态变化的问题
# todo ： 高分辨率 分类项目减少的问题
# todo : 切片 重采样前的
# todo : MPT
