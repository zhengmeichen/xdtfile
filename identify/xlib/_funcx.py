# coding=utf-8
import re

import numpy

RUNCREG = re.compile('([&|]?)([>=<!]{1,2})([\d+-]*\.?\d+)')
FUNCMAP = {"<": lambda x, y: x < y, ">": lambda x, y: x > y, '=': lambda x, y: x == y,
           "<=": lambda x, y: x <= y, ">=": lambda x, y: x >= y, "!": lambda x, y: x != y}


def apply_filter(func, d, dtype=None):
  tmp = numpy.ones_like(d, dtype=bool)
  if dtype: d = d.astype(dtype)
  for b, f, v in RUNCREG.findall(func):
    print [b, f, v],
    v = numpy.array(v, dtype=dtype) if dtype else float(v)
    if b == '&':
      tmp &= FUNCMAP[f](d, v)
    elif b == '|':
      tmp |= FUNCMAP[f](d, v)
    elif b == '':
      tmp = FUNCMAP[f](d, v)
    else:
      pass
  return tmp


def xqc(qrr, f, kk, n):
  fc = f.sum()
  if fc < kk:
    return
  test = qrr[f]  # QC过的数据
  tmp = numpy.zeros_like(test, 'u1')
  # 计算和记分：偏移做差和中位数倍数打分
  for k in xrange(1, kk):
    dd = test[k:] - test[:-k]
    absdd = numpy.abs(dd)
    chk = numpy.median(absdd, 0) * n
    score = (absdd > chk)  # bool类型 异常的值 --> True (1)
    tmp[k:] += score  # bool作整数计算
    tmp[:-k] += score
  ec = numpy.arange(kk, dtype='u1') // 2
  tmp[:kk] += ec[::-1]
  tmp[-kk:] += ec
  # f[f] = tmp <= kk
  f[f] = tmp < kk
  if fc - f.sum() > kk:
    xqc(qrr, f, kk, n)

Nan=float('nan')
def polyfit(x, y):
  try:
    p, residuals, rank, singular_values, rcond = numpy.polyfit(x, y, deg=1, full=True)
    return p[0].tolist(), p[1].tolist(), residuals[0].tolist()
  except:
    return Nan, Nan, Nan


def lstsq(x, y):
  try:
    a, residuals, rank, s = numpy.linalg.lstsq(numpy.array(x).reshape(-1, 1), y)
    return a[0].tolist(), 0, residuals[0].tolist()
  except:
    return Nan, Nan, Nan
