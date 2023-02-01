# coding=utf-8
"""
  实时子图组件 管理 与 生成
"""
import io

import matplotlib
import numpy

print __file__
matplotlib.rc_file('xlib/matplotlibrc')

from matplotlib import cm, dates, colors, pyplot as plt, ticker

try:
  from mpl_toolkits import basemap
except:
  basemap = None

######################
# 自动时间标注位置和样式
_loc_params = dict(
  minticks=2,
  maxticks={
    dates.YEARLY: 5, dates.MONTHLY: 5, dates.DAILY: 5, dates.HOURLY: 5,
    dates.MINUTELY: 5, dates.SECONDLY: 5, dates.MICROSECONDLY: 5
  },
  interval_multiples=True
)

# def _dates_loc():
#   loc = dates.AutoDateLocator(
#     minticks=4,
#     maxticks={
#       dates.YEARLY: 6, dates.MONTHLY: 6, dates.DAILY: 7, dates.HOURLY: 7,
#       dates.MINUTELY: 7, dates.SECONDLY: 7, dates.MICROSECONDLY: 7
#     },
#     interval_multiples=True
#   )
#
#   fmt = dates.AutoDateFormatter(loc)
#   return loc, fmt


x_month_loc = lambda: ticker.MaxNLocator(nbins=7, steps=(1, 2, 3, 4, 6), min_n_ticks=4, prune=None, integer=True)


@ticker.FuncFormatter
def x_mouth_fmt(a, b):
  return '%04d-%02d' % _month_date(a)


def _month_date(a):
  y, m = divmod(a + 2, 12)
  return (y, m + 1)


import datetime

x_month_date = lambda x: date2num([datetime.datetime(*_month_date(i), day=1) for i in x])

##############################

lognorm = colors.LogNorm()
# 时间转换实用方法
date2num = dates.date2num
num_delta = date2num(datetime.datetime(1970, 1, 1, 0, 0, 0))
num_delta_fy = date2num(datetime.datetime(2000, 1, 1, 12, 0, 0))


def s2num(seconds): return numpy.array(seconds) / 86400. + num_delta


def num2s(num): return (numpy.array(num) - num_delta) * 86400.


def fys2num(day, ms): return day + ms / 86400e3 + num_delta_fy


def parse_time(t): return numpy.datetime64(t).astype('M8[s]').astype('f8')


###############################
# 数据自动拉伸方法
def _3std_minmax(data, nstd=1):
  m = numpy.nanmean(data)
  s = numpy.nanstd(data) * nstd
  return m - s, m + s


# 传入参数指定范围 解析
def _vx(v):
  if isinstance(v, basestring):
    if v:
      return [float(x) if x else None for x in v.split(',')]
  else:
    return v


class ExtendAxes:
  """
  扩展的坐标系类, 是对matplotlib的坐标系的封装
  提供针对常用子图类别的高级自定义设定
  """

  def __init__(self, ax):
    self._ = ax

  def x_datetime_ticks(self):
    xaxis = self._.xaxis
    self._.xaxis_date()
    xaxis.get_major_locator().__dict__.update(**_loc_params)
    xaxis.set_minor_locator(dates.YearLocator())
    lim = self.get_xlim()
    l = self.get_xticks()
    v = numpy.empty_like(l)
    v[:-1] = l[1:] - l[:-1]
    v[-1] = m = v[:-1].max()
    m = m * 0.9
    xt = l[v >= m]
    self.set_xticks(xt)
    self.set_xlim(lim)

  def x_datetime_ticks2(self):
    xaxis = self._.xaxis
    self._.xaxis_date()
    xaxis.get_major_locator()
    lim = self.get_xlim()
    l = self.get_xticks()
    v = numpy.empty_like(l)
    v[:-1] = l[1:] - l[:-1]
    v[-1] = m = v[:-1].max()
    m = m * 0.9
    xt = l[v >= m]
    self.set_xticks(xt, )
    self.set_xlim(lim)
    self._.xaxis.set_tick_params(labelrotation=14, labelsize=8)
    self._.yaxis.set_tick_params(labelsize=8)

  def title(self, name, loc='center', **kw):
    self._.set_title(name, loc=loc, **kw)

  def ylim(self, vlim=None, **kw):
    self._.set_ylim(_vx(vlim), **kw)

  def xlim(self, vlim=None, **kw):
    self._.set_xlim(_vx(vlim), **kw)

  def clim(self, vlim=None, **kw):
    if hasattr(self, 'cax'):
      self.cax.set_xlim(_vx(vlim), **kw)

  def ylabel(self, txt, **kw):
    self._.set_ylabel(txt, **kw)

  def minor(self, on=True):
    if on:
      self._.minorticks_on()
    else:
      self._.minorticks_off()

  def xmap(self, title, data, extent, ticks, norm=None, vlim=None, clabel=None,
           lut=None, alpha=1, nstd=3,fontsize=7):
    vmin, vmax = _vx(vlim) or _3std_minmax(data, nstd=nstd)
    self.title(title, loc='center')
    m = self.imshow(data, cmap=cm.get_cmap('jet', lut=lut), norm=norm, vmin=vmin, vmax=vmax, alpha=alpha,
                    interpolation='nearest', extent=extent)
    p = self.get_position()
    self.cax = self.get_figure().add_axes([p.x1 + 0.009, p.y0, 0.025, p.y1 - p.y0])
    self.get_figure().colorbar(m, extend='both', cax=self.cax, label=clabel)
    if basemap:
      # loc = ticker.MaxNLocator(nbins='auto', steps=[1, 2, 3, 5, 10])
      # ticks_lng = loc.tick_values(*extent[:2])
      # ticks_lat = loc.tick_values(*extent[2:])
      m = basemap.Basemap(ax=self, llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1])
      m.drawcoastlines(linewidth=.5, linestyle='-.', color='k')
      m.drawparallels(ticks, linewidth=0.4, labels=[1, 0, 0, 1], fontsize=fontsize)
      m.drawmeridians(ticks, linewidth=0.4, labels=[1, 0, 0, 1], fontsize=fontsize)
    self.set_xlim(extent[:2])
    self.set_ylim(extent[2:])
    return self

  def ximshow(self, title, data, extent, yticks=None, ylabel='', xlabel='',
              norm=None, vlim=None, clabel=None, xticks=None, extend='both', alpha=1, nstd=3):
    vmin, vmax = _vx(vlim) or _3std_minmax(data, nstd=nstd)
    self.title(title, loc='center')
    m = self._.imshow(data, cmap='jet', norm=norm, aspect='auto', vmin=vmin, vmax=vmax,
                      interpolation='nearest', extent=extent, alpha=alpha)
    p = self.get_position()
    self.cax = self.get_figure().add_axes([p.x1 + 0.008, p.y0, 0.022, p.y1 - p.y0])
    self.get_figure().colorbar(m, extend=extend, cax=self.cax, label=clabel)
    if yticks and len(yticks) > 2: self.set_yticks(yticks)
    if xticks: self.set_xticks(xticks)
    self.set_ylabel(ylabel, )
    self.set_xlabel(xlabel, )
    return self

  def x_imshow_ticks(self, s, e):
    ax = self._
    if e is None:
      ax.xaxis.set_major_locator(x_month_loc)
      ax.xaxis.set_major_formatter(x_mouth_fmt)
    else:
      self.x_datetime_ticks()
    return self

  def time_imshow(self, title, data, extent, yticks=None, ylabel=None,
                  norm=None, vlim=None, clabel=None):
    self.ximshow(title, data, extent, yticks, ylabel, norm, vlim, clabel)
    self.x_datetime_ticks()
    return self

  def xline(self, x, y, style='o-', color=None, xlim=None, ylim=None, lw=.2, ms=2, title=None, ylabel=None, title_loc='center'):
    self.plot(x, y, style, ms=ms, lw=lw, color=color)
    if ylim: self.ylim(ylim)
    if title: self.title(title, loc=title_loc)
    if ylabel: self.ylabel(ylabel)
    self.yaxis.set_major_locator(ticker.MaxNLocator(nbins=6, min_n_ticks=3))
    self._xline_ms = ms
    return self

  def legend(self, lines, names, markerscale=2, **kw):
    ms = getattr(self, '_xline_ms', 2)
    if ms * markerscale < 6: markerscale = 6. / ms
    self._.legend(lines, names, markerscale=markerscale, **kw)
    return self

  def time_line(self, *args, **kwargs):
    self.xline(*args, **kwargs)
    self.x_datetime_ticks()
    return self

  def __getattr__(self, item):
    return getattr(self._, item)


import gc


class ExFig:
  def __init__(self, fig):
    self.fig = fig

  def __getattr__(self, item):
    # legend
    # align_xlabels
    # autofmt_xdate
    return getattr(self.fig, item)

  def save_png(self, dpi=300, fmt='png', water_mark=None):
    buf = io.BytesIO()
    if water_mark:
      pass
      # todo 此处可以给图加水印 标识
    self.fig.savefig(buf, facecolor=(1, 1, 1, 1), format=fmt, dpi=dpi)
    plt.close(self.fig)
    return buf.getvalue()

  def __del__(self):
    try:
      plt.close(self.fig)
    except:
      pass

  def __getitem__(self, item):
    return self.axes[item]

  def __iter__(self):
    return iter(self.axes)


class N_LinesFig(ExFig):
  def __init__(self, N, title, rl=0.8, dh=0.4, th=.6, rw=4.5, sh=1.2, fig_w=6, **k):
    gc.collect()
    dsh = sh + dh
    fig_h = N * dsh + th
    fig = plt.figure(figsize=[fig_w, fig_h])
    ExFig.__init__(self, fig)
    fig.suptitle(title, y=1 - 0.05 / fig_h)
    self.axes = [ExtendAxes(fig.add_axes([rl / fig_w, ((N - j) * dsh - sh) / fig_h, rw / fig_w, sh / fig_h])) for j in xrange(N)]


import collections

StatRet = collections.namedtuple('StatRet', 'name,x,mean,std,rms,count,all')


def Stat(name, data, x, y, rx, ry):
  m, s, r, c, a = '01234'
  return StatRet(name, x, m, s, r, c, a)


# =================================
import math


def time_to_x(dW, t):
  if dW:  # 等间隔时间
    x = s2num(t)
    x /= dW
    start = math.floor(x.min())
    x -= start
    W = int(math.ceil(x.max()))
    if not W:
      W = 1
    start *= dW
    end = start + W * dW
  else:  # 自然月时间
    t = [i.replace(day=1) for i in (t // 86400).astype('M8[D]').tolist()]
    mt = min(t)  # type: datetime.datetime
    mtx = mt.year * 12 + mt.month - 1
    x = [(i.year * 12 + i.month - 1 - mtx) for i in t]
    W = max(x) + 1
    start = mtx - 2
    end = None
    print divmod(start, 12), mt
  return W, start, end, numpy.array(x, 'u2')


class StatGrid:
  def __init__(self, grid):
    self.grid = grid
    self.mean = mean = grid['sum'] / grid['count']
    self.prms = prms = grid['ssum'] / grid['count']
    self.var = prms - (mean ** 2)

  @property
  def rms(self):
    return self.prms ** 0.5

  @property
  def std(self):
    return self.var ** .5

  @property
  def count(self):
    c = self.grid['count'].astype('f4')
    c[c == 0] = numpy.nan
    return c


class Corr3(ExFig):
  def __init__(self, title, dh=0.4, dw=0.8, dw2=0.6, fig_w=6., fig_h=6.5, **k):
    """
    -----------------------------------
    -       h1%  dh
    -    *********************** **
    -dw  *********************** ** dw
    -w1% *********************** ** w1%
    -    ha ******************** **
    -    *********************** **
    -    ********* wa ********** **
    -         h1% dh         h1
    -    *********** w2 ***********
    -dw  hb*********    hb*********
    -w1% *****wb****    *****wb****
    -         h1% dh         h1
    -----------------------------------
    """
    w1 = dw / fig_w  # 横向间距  1
    w2 = dw2 / fig_w  # 横向间距 2
    h1 = dh / fig_h  # 高度1
    wa = 1 - w1 - w1 - 0.03
    ha = wa * fig_w / fig_h
    hb = 1 - (ha + h1 * 3)
    wb = (1 - w1 * 2 - w2) / 2
    fig = plt.figure(figsize=[fig_w, fig_h])
    ExFig.__init__(self, fig)
    fig.suptitle(title, y=1 - 0.05 / fig_h)
    self.a = ExtendAxes(fig.add_axes([w1, hb + 2 * h1, wa, ha]))
    self.b = ExtendAxes(fig.add_axes([w1, h1, wb, hb]))
    self.c = ExtendAxes(fig.add_axes([w1 + w2 + wb, h1, wb, hb]))


class Corr3_scatter(ExFig):
  def __init__(self, title, dh=0.4, dw=0.8, dw2=0.6, fig_w=6., fig_h=6.5, **k):
    """
    -----------------------------------
    -       h1%  dh
    -    *********************** **
    -dw  *********************** ** dw
    -w1% *********************** ** w1%
    -    ha ******************** **
    -    *********************** **
    -    ********* wa ********** **
    -         h1% dh         h1
    -    *********** w2 ***********
    -dw  hb*********    hb*********
    -w1% *****wb****    *****wb****
    -         h1% dh         h1
    -----------------------------------
    """
    w1 = dw / fig_w  # 横向间距  1
    w2 = dw2 / fig_w  # 横向间距 2
    h1 = dh / fig_h  # 高度1
    wa = 1 - w1 - w1
    ha = wa * fig_w / fig_h
    hb = 1 - (ha + h1 * 3)
    wb = (1 - w1 * 2 - w2) / 2
    fig = plt.figure(figsize=[fig_w, fig_h])
    ExFig.__init__(self, fig)
    fig.suptitle(title, y=1 - 0.05 / fig_h)
    self.a = ExtendAxes(fig.add_axes([w1, hb + 2 * h1, wa, ha]))
    self.b = ExtendAxes(fig.add_axes([w1, h1, wb, hb]))
    self.c = ExtendAxes(fig.add_axes([w1 + w2 + wb, h1, wb, hb]))


class Corr4(ExFig):
  def __init__(self, title, dh=0.4, th=.6, fig_w=6, **k):
    fig_h = 5.2
    fig = plt.figure(figsize=[fig_w, fig_h])
    ExFig.__init__(self, fig)
    fig.suptitle(title, y=1 - 0.05 / fig_h)
    h = (fig_h - th) / 2  # 左
    rl = 0.6 / fig_w
    r2 = rl + (h - dh + 1) / fig_w
    vw2 = (fig_w - .4) / fig_w - r2
    self.b = ExtendAxes(fig.add_axes([rl, (dh) / fig_h, (h - dh) / fig_w, (h - dh) / fig_h]))
    self.a = ExtendAxes(fig.add_axes([rl, (h + dh) / fig_h, (h - dh) / fig_w, (h - dh) / fig_h]))
    self.d = ExtendAxes(fig.add_axes([r2, (h + dh) / fig_h, vw2, (h - dh) / fig_h]))
    self.e = ExtendAxes(fig.add_axes([r2, (dh) / fig_h, vw2, (h - dh) / fig_h]))


class Corr4b(ExFig):
  def __init__(self, title, dh=0.4, th=.6, fig_w=6, **k):
    """
    ax-pos
      a  b
      c  d
    :param title:
    :param dh:
    :param th:
    :param fig_w:
    """
    fig_h = 5.2
    fig = plt.figure(figsize=[fig_w, fig_h])
    ExFig.__init__(self, fig)
    fig.suptitle(title, y=1 - 0.05 / fig_h)
    h = (fig_h - th) / 2  # 左
    rl = th / fig_w
    r2 = rl + (h - dh + 1) / fig_w
    vw2 = (fig_w - th) / fig_w - r2
    self.a = ExtendAxes(fig.add_axes([rl, (h + dh) / fig_h, (h - dh) / fig_w, (h - dh) / fig_h]))
    self.b = ExtendAxes(fig.add_axes([r2, (h + dh) / fig_h, vw2, (h - dh) / fig_h]))
    self.c = ExtendAxes(fig.add_axes([rl, (dh) / fig_h, (h - dh) / fig_w, (h - dh) / fig_h]))
    self.d = ExtendAxes(fig.add_axes([r2, (dh) / fig_h, vw2, (h - dh) / fig_h]))
    self.a.title('(a)', loc='right')
    self.b.title('(b)', loc='right')
    self.c.title('(c)', loc='right')
    self.d.title('(d)', loc='right')
    self.d.yaxis.tick_right()
    self.d.yaxis.set_label_position('right')
    self.b.yaxis.tick_right()
    self.b.yaxis.set_label_position('right')
