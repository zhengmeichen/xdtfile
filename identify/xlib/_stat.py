# coding=utf-8
"""
实时统计组合图 构建/ 数据准备和制图

"""
import imlib
import numpy

import _plots


def cache_property(func):
  def wapper(self):
    r = 'cache_' + func.__name__
    if hasattr(self, r):
      return getattr(self, r)
    value = func(self)
    setattr(self, r, value)
    return value

  return property(wapper)


class Data:
  def __init__(self, name, grid):
    self.name = name
    self.grid = grid

  @cache_property
  def mean(self):
    return self.grid['sum'] / self.grid['count']

  @cache_property
  def prms(self):
    return self.grid['ssum'] / self.grid['count']

  @cache_property
  def rms(self):
    return self.prms ** .5

  @cache_property
  def var(self):
    return self.prms - self.mean ** 2

  @cache_property
  def std(self):
    return self.var ** .5

  @cache_property
  def count(self):
    c = self.grid['count'].astype('f4')
    c[c == 0] = numpy.nan
    return c


class TimeSpace(Data):
  def __init__(self, name, data, y, t, H, rx, yticks, **kw):
    W, start, end, x = _plots.time_to_x(float(rx), t)
    grid = imlib.statgrid((H, W))
    qc = numpy.ones_like(x, dtype='u1')
    imlib.statproj(data, qc, x, y, grid)
    self.yticks = yticks
    if end:
      self.extent = start, end, yticks[0], yticks[-1]
    else:
      self.extent = start, start + W, yticks[0], yticks[-1]
    self.tick_se = start, end
    self.x = numpy.arange(start, end, rx)
    Data.__init__(self, name, grid)


class TimeLine(Data):
  def __init__(self, name, rx, t, d):
    dW = float(rx)
    W, start, end, x = _plots.time_to_x(dW, t)
    y = numpy.zeros_like(x, dtype='u2')
    grid = imlib.statgrid((1, W))
    m = numpy.mean(d)
    s = numpy.std(d)
    n = 2
    qc = d < (m + n * s)
    qc &= d > (m - n * s)
    imlib.statproj(d.astype('f4'), qc, x, y, grid)
    if end:
      self.x = numpy.arange(start, end, dW)
    else:
      self.x = _plots.x_month_date(numpy.arange(start, start + W))
    f = grid['count'] > 0
    Data.__init__(self, name, grid[f])
    self.tick_se = start, end


import math


class GeoMap(Data):
  def __init__(self, name, d, lat, lon, extent=(-180, 180, -90, 90), resu=0.1):
    l, r, b, t = extent
    w = ((r - l) % 360) or 360
    r = l + w
    self.extent = l, r, b, t
    h = (t - b)
    y = numpy.floor((t - lat) / resu).astype('u2')
    x = numpy.floor(((lon - l) % 360) / resu).astype('u2')
    grid = imlib.statgrid((int(math.ceil(h / resu)), int(math.ceil(w / resu))))
    qc = lat > b
    qc &= lat <= t
    qc &= x < w
    imlib.statproj(d.astype('f4'), qc, x, y, grid)
    Data.__init__(self, name, grid)
    self.height = h
    self.width = w


def time_space(data, subplots, title, ylabel, unit, yticks, is_diff=False, lim_m=None, lim_s=None, lim_r=None, **k):
  fig = _plots.N_LinesFig(len(subplots), title=title, **k)
  get_ax = iter(fig).next
  sbpn = subpnames(is_diff)
  if 'mean' in subplots:
    get_ax().ximshow(sbpn[0], data, extent=data.extent, yticks=yticks,
                     ylabel=ylabel, vlim=lim_m, clabel=unit).x_imshow_ticks(*data.tick_se).minor()
  if 'std' in subplots:
    get_ax().ximshow(sbpn[1], data ** .5, extent=data.extent, yticks=yticks,
                     ylabel=ylabel, vlim=lim_s, clabel=unit).x_imshow_ticks(*data.tick_se).minor()
  if 'rms' in subplots:
    get_ax().ximshow(sbpn[2], data ** .5, extent=data.extent, yticks=yticks,
                     ylabel=ylabel, vlim=lim_r, clabel=unit).x_imshow_ticks(*data.tick_se).minor()
  if 'count' in subplots:
    c = data['count'].astype('f4')
    c[c == 0] = numpy.nan
    get_ax().ximshow(sbpn[3], c, extent=data.extent, yticks=data.yticks,
                     ylabel=ylabel, clabel='Num', vlim=(0, None)).x_imshow_ticks(*data.tick_se).minor()
  return fig


def time_line(data, figname, legend_data, subplots, unit=None, lim_r=None, lim_s=None, lim_m=None, is_diff=False, **k):
  fig = _plots.N_LinesFig(len(subplots), figname, **k)
  sbpn = subpnames(is_diff)
  get_ax = iter(fig).next
  if 'mean' in subplots:
    ax = get_ax()
    for i in data:
      ax.xline(i.x, i.mean, title=sbpn[0], ylabel=unit, xlim=',')
      ax.fill_between(i.x, i.mean - i.std, i.mean + i.std, facecolor=ax.get_lines()[-1].get_color(), lw=0, alpha=0.2)
    ax.ylim(lim_m)
    ax.x_datetime_ticks()
    if len(data) > 1:
      ax.legend(ax.get_lines(), legend_data, ncol=4)
    ax.minor()
  if 'std' in subplots:
    ax = get_ax()
    ax.minor()
    for i in data:
      ax.xline(i.x, i.std, title=sbpn[1], ylabel=unit, xlim=',')
    ax.x_datetime_ticks()
    ax.ylim(lim_s)
    if len(data) > 1:
      ax.legend(ax.get_lines(), legend_data, ncol=4)
  if 'rms' in subplots:
    ax = get_ax()
    ax.minor()
    for i in data:
      ax.xline(i.x, i.rms, title=sbpn[2], ylabel=unit, xlim=',')
    ax.x_datetime_ticks()
    ax.ylim(lim_r)
    if len(data) > 1:
      ax.legend(ax.get_lines(), legend_data, ncol=4)
    if len(data) == 1:
      i = data[0]
      m = numpy.nanmean(i.rms)
      s = numpy.nanstd(i.rms)
      sbm = (s * 100 / m)
      a = ax.get_ylim()
      b = ax.get_xlim()
      ax.text(b[0] * .97 + b[1] * .03, a[0] * .05 + a[1] * .95, 'Mean:{m:.4f} Std:{s:.4f} Stability:{sbm:.2f}%'.format(s=s, m=m, sbm=sbm), fontsize=8, verticalalignment='top')
    else:
      ax.legend(ax.get_lines(), legend_data, ncol=4)
  if 'count' in subplots:
    ax = get_ax()
    ax.minor()
    for i in data:
      ax.xline(i.x, i.c, title=sbpn[3], ylabel=unit[3], xlim=',')
    ax.x_datetime_ticks()
    ax.ylim([0, None])
    if len(legend_data) > 1:
      ax.legend(ax.get_lines(), legend_data, ncol=4)
  return fig


def geo_map(data, figtitle, subplots, unit, lim_m=None, lim_s=None, lim_r=None, is_diff=False, **kw):
  rw = kw.get('rw', 4.5)
  sh = kw.get('sh', data.height * rw / data.width)
  fig = _plots.N_LinesFig(len(subplots), figtitle, sh=sh, **kw)
  get_ax = iter(fig).next
  sbpn = subpnames(is_diff)
  x1, x2 = data.extent[:2]
  w = x2 - x1
  for delta in [1, 2, 5, 10, 15, 20, 30, 45]:
    if w / delta <= 12: break
  ticks = range(-180, 181, delta)
  if 'mean' in subplots:
    get_ax().xmap(sbpn[0], data.mean,  ticks=ticks, extent=data.extent, vlim=lim_m, clabel=unit).minor()
  if 'std' in subplots:
    get_ax().xmap(sbpn[1], data.std,   ticks=ticks, extent=data.extent, vlim=lim_s, clabel=unit).minor()
  if 'rms' in subplots:
    get_ax().xmap(sbpn[2], data.rms,   ticks=ticks, extent=data.extent, vlim=lim_r, clabel=unit).minor()
  if 'count' in subplots:
    get_ax().xmap(sbpn[3], data.count, ticks=ticks, extent=data.extent, clabel='Num', vlim=(0, None)).minor()
  return fig


def legend_it(datas, sep_legend='-', sep_title=' '):
  same = None
  for i in datas:
    cc = set(i.name)
    if same is None:
      same = cc
    else:
      same &= cc
  return [sep_legend.join(p for p in i.name if not p in same) or 'Origin' for i in datas], sep_title.join(p for p in datas[0])


subpnames = lambda is_diff: ('BIAS,STDE,RMSE,COUNT,COUNT/ALL' if is_diff else 'MEAN,STD,RMS,COUNT,COUNT/ALL').split(',')
