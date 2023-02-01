# coding=utf-8

try:
    from importlib import import_module, reload
except:
    from importlib import import_module

import inspect
import os

_split = os.path.splitext
_MT = {}


def _get_m(name):
    m = import_module('views.' + name)
    f = inspect.getsourcefile(m)
    t0 = os.stat(f).st_mtime
    t = _MT.setdefault(name, t0)
    if t != t0:
        reload(m)
        _MT[name] = t0
    return m


def func_list(name):
    m = _get_m(name)
    d = []
    for n, o in inspect.getmembers(m):
        if inspect.isfunction(o):
            d.append([inspect.getdoc(o), n, inspect.getargs(o)])
    return d


def getfunc(func):
    m, fn = func.rsplit('.', 1)
    return getattr(_get_m(m), fn)
