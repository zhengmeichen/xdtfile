# page toolkit
from __future__ import unicode_literals, print_function, with_statement
import datetime
import math, os
import sys


def top5(it, n=5):
    k = 0
    while k < n:
        try:
            yield it[k]
            k += 1
        except:
            break


def format_bit(bit):
    lst = [None, 'KB', 'MB', 'GB', 'TB', 'PB']
    if bit > 1024:
        i = int(math.log(bit, 1024))
        if i > 3: i = 3  # len(lst) - 1
        return "%.3f %s" % (round(float(bit) / 1024 ** i, 3), lst[i])
    else:
        return "%d B" % bit


def format_t(t, fmt='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.utcfromtimestamp(t).strftime(fmt)


def delta_t(**kw):
    return datetime.timedelta(**kw)


_nav = None
_navt = 0

PY2 = sys.version_info.major == 2
if PY2:
    import codecs

    open = codecs.open
import yaml


def nav(fn='nav.yml'):
    global _navt, _nav
    if os.stat(fn).st_mtime > _navt:
        _navt = os.stat(fn).st_mtime
        _nav = yaml_loadf(fn)
    return _nav


def yaml_loadf(fn):
    with open(fn, 'r', encoding='utf8') as f:
        d = yaml.safe_load(f)
    return d


if __name__ == '__main__':
    print((nav()))
