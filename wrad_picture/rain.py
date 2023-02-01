# coding=utf-8
import datetime
import glob
import os

import h5py
import numpy

import _funcx
import _plots
from _wrad import dB2val, val2dB, _stat, XStat, TimeSpaceA, GeoMapA

import sys
reload(sys)
sys.setdefaultencoding('utf8')


class Data:
  def __init__(self, pat, data, fname='',
               filters=None, start=None, end=None, datasets=(), **kv):
    self.datasets = datasets
    self.pat = pat
    self.fname = fname,
    self.start = start
    self.end = end
    self.filters = filters or []
    self.data = data
    self.is_dif = self.data == 'Sigma_Dif'
    self.kv = kv

  def get(self, item, default):
    return self.kv.get(item, getattr(self, item, default))

  def files(self):
    s = datetime.datetime.strptime(self.start, '%Y-%m-%d')
    e = datetime.datetime.strptime(self.end, '%Y-%m-%d')
    _1d = datetime.timedelta(1)
    while s <= e:
      pat = os.path.join(s.strftime(RAIN), self.pat)
      s += _1d
      for i in glob.glob(pat): yield i

  def __call__(self, fn, return_db=False):
    with h5py.File(fn, 'r') as g:
      if self.is_dif:
        v = [g['Sigma_Obs'][()], g['Sigma_Ref'][()]]
        q = v[0] > -1000  # 去掉填充值
        q &= v[0] < 1000  # 去掉填充值
        q &= v[1] > -1000  # 去掉填充值
        q &= v[1] < 1000  # 去掉填充值
      else:
        v = [g[self.data][()], ]
        q = v[0] > -1000  # 去掉填充值
        q &= v[0] < 1000  # 去掉填充值
      q_is_1d = q.ndim == 1
      h = q.shape[0]
      try:
        for i in self.filters:
          q1 = apply_filter(g, v, **i)
          if q_is_1d:
            q = q & q1
          else:
            q = q & q1.reshape(h, -1)
      except Exception, e:
        # raise Exception(str([g.keys(),i]))
        # return None, e.message
        raise
      if q_is_1d:
        l, = numpy.where(q)
        p = 0
        ret = [[i[l] if return_db else dB2val(i[l]) for i in v]]
      else:
        l, p = numpy.where(q)
        ret = [[i[l, p] if return_db else dB2val(i[l, p]) for i in v]]
      for i in self.datasets:
        d = g[i][...]
        if d.ndim == 1:
          ret.append(d[l])
        elif d.ndim == 2:
          ret.append(d[l, p])
      return ret, fn[-18:-4]


def apply_filter(grp, vals, dataset, chkfunc):
  if isinstance(dataset, dict):
    ds = dataset.copy()
    e = ds.pop('_')
    d = {i: grp[j][...].reshape(-1, 1) for i, j in ds.items()}
    if 'x' in e: return numpy.all([eval(e, d, {'x': x, 'v': chkfunc}) for x in vals], 0)
    return eval(e, d, {'v': chkfunc})
  else:
    d = grp[dataset][...]
    return _funcx.apply_filter(chkfunc, d)


RAIN = 'data/wrad/rain/%Y%m%d/'


def get_time(request, response, **kw):
  import glob, time
  v = []
  for i in glob.glob('data/wrad/rain/20??????'):
    t = time.mktime(time.strptime(i, 'data/wrad/rain/%Y%m%d')) * 1000
    v.append([t, 1])
  v.sort()
  return dict(data=v)


def makeVal(data):
  info = []
  a0, a1, a2 = data.get('area_azi', [0, 360, 10])
  y = numpy.arange(a0, a1, a2)
  z0, z1, z2 = data.get('area_zen', [0, 67, 1])
  x = numpy.arange(z0, z1, z2)

  grid = XStat(diff=data.is_dif, h=y.size, w=x.size)
  for i in data.files():
    info.append(i)
    (v, azi, zen), r = data(i)
    z = (numpy.floor((zen - z0) / z2))
    a = (numpy.floor(((azi - a0) % 360) / a2))
    info.append('%s: %d' % (r, v[0].size))
    info.append(str(zen))
    grid(x=z, y=a, v=v)
  grid.update(
    extent=[z0, z1, a0, a1],
    xlim=[z0, z1],
    ylim=[a0, a1],
    x=x, y=y, info=info
  )
  return grid


def agls_dtbt(request, response, touni, **kw):
  cfg = request.json
  data = Data(datasets=['SensorAzimuth', 'SensorZenith'], **cfg)
  v = makeVal(data)

  v.o.grid = v.o.grid[::-1]
  if v.is_dif:
    v.b.grid = v.b.grid[::-1]
  fig = _stat.distribute(data=(v), subplots=cfg['subplots'],
                         title='Satellite Azimuth-Zenith Distribute for {name}\n{fname} {subtext}'.format(
                           **cfg),

                         ylabel='Sensor Azimuth', unit='dB', sh=2.4, rl=.6, yticks=None, )
  # [0, 90, 180, 270, 360]
  for i in fig.axes:
    i.set_xlabel('Sensor Zenith')
    i.xlim(v.xlim)
    i.ylim(v.ylim)

  response.info = '|'.join(v.info)
  response.content_type = 'image/png'
  response.download = 'Satellite_Azimuth-Zenith _{name}_{fname}_{subtext}'.format(**cfg)
  return fig.save_png()


def agls2(request, response, touni, **kw):
  cfg, v, data = _angles_distribute(request, response)
  fig = _plots.N_LinesFig(2, 'tt', sh=2)
  ax = fig.axes[0]
  print len(v.y), v.mean.shape
  mean = v.mean
  s = cfg['dwazi'] or None
  l = ax._.plot(v.x, mean.T[..., s])
  ax.xlim(v.xlim)
  ax.legend(l, ['%d~%d$\degree$' % (i, i + 10) for i in v.y[s]])
  ax.title('a)', loc='left')
  ax.ylabel(cfg['name'])
  ax.xlabel('Sensor Zenith')
  ax = fig.axes[1]
  ax.title('b)', loc='left')
  ax.ylabel(cfg['name'])
  ax.xlabel('Sensor Azimuth')
  s = cfg['dszen'] or None
  l = ax._.plot(v.y, mean[..., s])
  ax.xlim(v.ylim)
  ax.legend(l, ['%d~%d$\degree$' % (i, i + 1) for i in v.x[s]])
  response.info = '|'.join(v.info)
  response.content_type = 'image/png'
  response.download = 'Satellite_Azimuth-Zenith _{name}_{fname}_{subtext}'.format(**cfg)
  return fig.save_png()


def dwazi(request, response, touni, **kw):
  cfg, v, data = _angles_distribute(request, response)
  s = cfg['dwazi']
  if s:
    names = ['%d~%d°' % (i, i + 1) for i in v.y[s]]
    g = v.make(index=s, transpose=False, summary=False)
  else:
    g = v.make(index=None, transpose=False, summary=True)
    names = ['ALL']
  mean = g.mean
  mean[numpy.isnan(mean)] = -2e10
  return dict(
    x=v.x.tolist(), y=mean.tolist(),
    xlim=v.xlim, names=names,
    ylabel=cfg['name'],
    xlabel='Sensor Zenith'
  )


def dszen(request, response, touni, **kw):
  cfg, v, data = _angles_distribute(request, response)
  s = cfg['dszen']
  if s:
    names = ['%d~%d°' % (i, i + 1) for i in v.x[s]]
    g = v.make(index=s, transpose=True, summary=False)
  else:
    g = v.make(index=None, transpose=True, summary=True)
    names = ['ALL']
  mean = g.mean
  mean[numpy.isnan(mean)] = -2e10

  return dict(
    x=v.y.tolist(), y=mean.tolist(),
    xlim=v.ylim, names=names,
    ylabel=cfg['name'],
    xlabel='Sensor Azimuth'
  )


def _angles_distribute(request, response):
  cfg = request.json
  data = Data(datasets=['SensorAzimuth', 'SensorZenith'], **cfg)
  v = makeVal(data)
  print len(v.y), v.shape
  response.info = ''.join(data.files())
  # response.info = '|'.join(v.info)
  return cfg, v, data


def gbal(request, response, touni, **kw):
  cfg = request.json
  # grid = _stat.GeoMapA(cfg['name'], resu=cfg['resu'], extent=cfg['extent'])

  data = Data(datasets=['Latitude', 'Longitude'], **cfg)
  grid = GeoMapA(isdif=data.is_dif, **cfg)
  cfg.pop('data')
  info = []
  for i in data.files():
    d, r = data(i)
    try:
      (v, lat, lon) = d
    except:
      info.append(i + r)
      continue
    info.append('%s: %d' % (r, v[0].size))
    grid(v, lat, lon)
  fig = _stat.geo_map((grid),
                      figtitle='Geo-Map for {name}\n{fname} {subtext}'.format(
                        **cfg),
                      unit='dB',
                      is_diff='Dif' in data.data, rl=.6, **cfg)
  response.info = '|'.join(info)
  response.content_type = 'image/png'
  response.download = 'Geo-Map_{name}_{fname}_{subtext}'.format(**cfg)
  return fig.save_png()


def timesrs(request, response, touni, **kw):
  # 时间序列图
  cfg = request.json
  datasets = ['Timestamp']
  data = Data(datasets=datasets, **cfg)
  stt = _plots.parse_time(cfg['start'])
  end = _plots.parse_time(cfg['end']) + 86400
  v = TimeSpaceA('1', stt, end, cfg['rx'], 1, data.is_dif, yticks=None)
  info = []
  for i in data.files():
    (d, t), r = data(i)
    v(d, t)
    info.append('%s: %d' % (r, d[0].size))
  response.info = info
  x = v.x
  # 转时间戳 1970 毫秒数，echarts 绘图用的时间
  t = (_plots.num2s(x) * 1e3).tolist()
  v = v.make(0, False, False)
  return dict(
    t=t,
    stt=stt, end=end,
    mean=numpy.round(v.mean, 3).tolist(),
    std=numpy.round(v.std, 3).tolist(),
    count=v.count.tolist(),
    # rms=numpy.round(v.rms, 3).tolist()
  )


# Echart转死图片
def timesrs_picture(request, response, *a, **k):
  # 时间序列图
  cfg = request.json
  print cfg
  datasets = ['Timestamp']
  data = Data(datasets=datasets, **cfg)
  # print data
  stt = _plots.parse_time(cfg['start'])
  end = _plots.parse_time(cfg['end']) + 86400
  # print stt,end
  v = TimeSpaceA('1', stt, end, cfg['rx'], 1, data.is_dif, yticks=None)
  info = []
  for i in data.files():
    (d, t), r = data(i)
    v(d, t)
    info.append('%s: %d' % (r, d[0].size))

  response.info = info

  x = v.x
  # 转时间戳 1970 毫秒数，echarts 绘图用的时间
  # t = (_plots.num2s(x) * 1e3).tolist()
  # print x, t
  v = v.make(0, False, False)
  # 平均值，标准差，计数
  val = getattr(v, cfg.get('subplots', 'mean'))
  val[val < -2000000] = numpy.nan

  # rl=0.6图片距离左边界, sh=2图片高度, rw=5.2图片宽度,dh=0.6图片距离底部距离
  fig = _plots.N_LinesFig(1, cfg['title'].decode('utf-8'), rl=0.7, dh=0.6, sh=2, rw=5.1)
  ax = fig[0]
  # 固定为mean，subplots里边选择绘画类型
  ax.plot(x, val)
  ax.x_datetime_ticks()
  ax.xlim(v.xlim)
  # ax.legend(l, ['%d~%d$\degree$' % (i, i + 10) for i in v.x[s]])
  ax.title(cfg['title']+' '+ cfg['subtext'], loc='left')
  ax.tick_params(axis='y',direction='out',labelsize=8)
  ax.ylabel(cfg['name'], fontsize=10)
  ax.xlabel('Date', fontsize=10)

  # 设值返回的格式
  response.content_type = 'image/png'
  response.download = '{subplots}_{title}_{subtext}'.format(**cfg)
  return fig.save_png()


def dwazi_picture(request, response, *a, **k):
  # 入射角分布图
  cfg = request.json
  data = Data(datasets=['SensorAzimuth', 'SensorZenith'], **cfg)
  v = makeVal(data)
  # print len(v.y), v.shape
  response.info = ''.join(data.files())
  # response.info = '|'.join(v.info)
  print cfg
  # print data

  # s是方位角分类数据
  s = cfg['dwazi']
  print '方位角数',s
  # --选择的方位角数据

  if s:
    names = [u'%d~%d°' % (i, i + 1) for i in v.y[s]]
    g = v.make(index=s, transpose=False, summary=False)
  else:
    g = v.make(index=None, transpose=False, summary=True)
    names = ['ALL']
  mean = g.mean
  # mean[numpy.isnan(mean)] = -2e10
  mean[mean < -2000000] = numpy.nan

  x = v.x.tolist()
  # print 'x',x--[20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47]横坐标范围
  y = mean.tolist()
  # print len(y),len(y[1])

  xlim = v.xlim
  # print 'xlim',xlim--[20, 48]入射区间

  # 图标名称
  names = names
  # print 'names',names

  # rl=0.6图片距离左边界, sh=2图片高度, rw=5.2图片宽度,dh=0.6图片距离底部距离
  # print type(cfg['title'])
  title = cfg['title']
  # fig = _plots.N_LinesFig(1, cfg['title'], rl=0.6, dh=0.6, sh=2, rw=5.1)
  fig = _plots.N_LinesFig(1, title, rl=0.6, dh=0.6, sh=2, rw=5.1)
  ax = fig[0]

  l = []
  for i in range(len(y)):
    # x与y[i]的值一一对应
    l.extend(ax.plot(x, y[i]))

  # print l
  # xlim就是x轴能够显示的范围
  ax.xlim(xlim)
  ax.legend(l, names)
  ax.title(cfg['subtext'], loc='left')
  ax.ylabel(cfg['ylabel'], fontsize=10)
  ax.xlabel('Sensor Zenith', fontsize=10)

  # 设值返回的格式
  response.content_type = 'image/png'
  response.download = '{title}_{subtext}'.format(**cfg)
  return fig.save_png()


def dszen_picture(request, response, *a, **k):
  # 方位角分布图
  cfg = request.json
  data = Data(datasets=['SensorAzimuth', 'SensorZenith'], **cfg)
  v = makeVal(data)
  # print len(v.y), v.shape
  response.info = ''.join(data.files())
  # response.info = '|'.join(v.info)
  print cfg
  # print data

  # s是天顶角分类数据
  s = cfg['dszen']
  # print s--选择的天顶角数据

  if s:
    names = [u'%d~%d°' % (i, i + 1) for i in v.x[s]]
    g = v.make(index=s, transpose=True, summary=False)
  else:
    g = v.make(index=None, transpose=True, summary=True)
    names = ['ALL']
  mean = g.mean
  print mean
  # mean[numpy.isnan(mean)] = -2e10
  mean[mean < -2000000] = numpy.nan
  print mean

  x=v.y.tolist()
  # print x
  y=mean.tolist()
  # print len(y)

  xlim=v.ylim
  # print xlim

  # 图标名称
  names=names
  # print names

  # rl=0.6图片距离左边界, sh=2图片高度, rw=5.2图片宽度,dh=0.6图片距离底部距离
  # print type(cfg['title'])
  title = cfg['title']
  # fig = _plots.N_LinesFig(1, cfg['title'], rl=0.6, dh=0.6, sh=2, rw=5.1)
  fig = _plots.N_LinesFig(1, title, rl=0.6, dh=0.6, sh=2, rw=5.1)
  ax = fig[0]

  l=[]
  for i in range(len(y)):
    # x与y[i]的值一一对应
    l.extend(ax.plot(x,y[i]))

  # print l
  # xlim就是x轴能够显示的范围
  ax.xlim(xlim)

  ax.legend(l, names)
  ax.title(cfg['subtext'], loc='left')
  ax.ylabel(cfg['ylabel'], fontsize=10)
  ax.xlabel('Sensor Azimuth', fontsize=10)

  # 设值返回的格式
  response.content_type = 'image/png'
  response.download = '{title}_{subtext}'.format(**cfg)
  return fig.save_png()


def draw_tspc(request, response, touni, **kw):
  cfg = request.json
  var_y = cfg['vy']
  a, b, c = cfg['range']
  y = numpy.arange(a, b, c)
  h = y.size
  ticks = _plots.loc.tick_values(a, b).tolist()
  # dt = (ticks[1] - ticks[0]) * 0.8
  ticks[0] = max(ticks[0], a)
  ticks[-1] = min(ticks[-1], b)
  # if (ticks[1] - ticks[0] < dt): ticks[1] = ticks[0]
  # if (ticks[-1] - ticks[-2] < dt): ticks[-2] = ticks[-1]
  # ticks = numpy.unique(ticks)

  data = Data(datasets=['Timestamp', var_y], **cfg)
  stt = _plots.parse_time(cfg['start'])
  end = _plots.parse_time(cfg['end']) + 86400
  #
  v = TimeSpaceA('my', start=stt, end=end, is_dif=data.is_dif,
                 dx=cfg['rx'], H=h, yticks=ticks)
  v.extent = v.xlim + [a, b]
  info = []
  for i in data.files():
    (d, t, p), r = data(i)
    # assert 0, p
    p = (b - p)
    p = numpy.ceil(p / c)
    qc = p < h
    qc &= p >= 0
    v(d, t, p, qc)
    # info.append('%s: %d' % (r, t.size))
    info.append('%s: %d' % (r, p.size))
  response.info = info
  cfg.pop('data')

  img = _stat.time_space(
    data=v, title='Time-{vy} Distribute for {name}\n{fname}  {subtext}'.format(
      **cfg),
    ylabel=var_y, yticks=v.yticks, is_diff=v.is_dif, unit=cfg.get('unit', 'dB'), subplots=cfg.get('subplots', None),
    lim_m=cfg.get('lim_m', None), lim_s=cfg.get('lim_s', None), lim_r=cfg.get('lim_r', None), rl=.6
  )
  response.content_type = 'image/png'
  response.download = 'Time-{vy}_{name}_{fname}_{subtext}'.format(**cfg)
  return img.save_png()


def cbins(v, lim_m):
  r = _plots._vx(lim_m)
  if r:
    locs = _plots.loc.tick_values(*r)
  else:
    m = numpy.isinf(v) | numpy.isneginf(v) | numpy.isnan(v)
    v = v[~m]
    v, b = numpy.histogram(v, 1000, normed=True)
    p = numpy.cumsum(v)
    p /= p[-1]
    m = p > 0.01
    m &= p < 0.99
  try:
    s, e = numpy.where(m)[0][(0, -1),]
    locs = _plots.loc.tick_values(b[s], b[e])
  except:
    return None, None
  return locs[(0, -1),].round(2), len(locs) * 8


def hist(request, response, **kw):
  cfg = request.json
  data = Data(**cfg)
  info = []
  d = []
  b = None
  nbins = rr = None
  for i in data.files():
    info.append(i)
    (v,), r = data(i)
    v = val2dB(v)
    if not nbins:
      rr, nbins = cbins(v, cfg.get('lim_m', None))
    if nbins is None: continue
    v, bins = numpy.histogram(v, bins=nbins, range=rr)
    d.append(v)
    info.append('%s: %d' % (r, v.size))
  if nbins is None:
    bins = numpy.arange(5)
    d.append([0] * 5)
  x = (bins[1:] + bins[:-1]) / 2
  n = numpy.sum(d, axis=0)
  p = n / float(sum(n))
  d = p * (bins.size - 1) / (bins[-1] - bins[0])
  ret = dict(
    x=x.tolist(),
    xlim=bins[(0, -1),].tolist(),
    names=['频数', '概率', '概率密度'],
    y=[n.tolist(), p.tolist(), d.tolist()],
    type='bar', selectedMode='single'
  )

  response.info = '|'.join(info)
  return ret


def rel(request, response, **kw):
  cfg = request.json
  data = Data(**cfg)
  info = []
  o = []
  s = []
  r = '11'
  for i in data.files():
    info.append(i)
    # if 1:
    #   with h5py.File(i, 'r') as g:
    #     v = [g['Sigma_Obs'][()], g['Sigma_Ref'][()]]
    # else:
    (v,), r = data(i, return_db=True)
    # if not nbins:
    #   rr, nbins = cbins(v, cfg.get('lim_m', None))
    o.append(v[0])
    s.append(v[1])
    info.append('%s: %d' % (r, v[0].size))
  import views.sno._rel as rel
  a = (numpy.concatenate(o))
  b = (numpy.concatenate(s))
  f = ~numpy.isnan(a + b)
  # f = a > 1e-10
  # f |= b > 1e-10
  a = a[f]
  b = b[f]
  assert len(a)
  vlim = numpy.nanmin([a, b]), numpy.nanmax([a, b])
  assert len(a)
  co_data = rel.co_data(
    a=a, b=b, c=a - b,
    namea='${\sigma}_{WindRAD}$(dB)', nameb='${\sigma}_{RainForest}$(dB)',
    nameab='${\sigma}(dB)$',
    namec='${\Delta}_{\sigma}$(dB)',
    name='',
    value_limit='-40, 10',
    bias_limit='-30, 30',
    size=len(a)
  )
  fig, info1 = rel.correlation(co_data)
  response.info = dict(a=info, b=info1)
  return fig
