# coding=utf-8
import logging
import sys
import traceback
from threading import *

if sys.version_info.major == 2:
    class ThreadEx(Thread):
        is_killed = False

        def stop(self):
            self.is_killed = True
            if self.started:
                self._Thread__stop()

        def __init__(self, *args, **kwargs):
            Thread.__init__(self, *args, **kwargs)
            self.successful = None

        def run(self):
            try:
                self.ret = self._Thread__target(*self._Thread__args, **self._Thread__kwargs)
            except:
                self.ret = traceback.format_exc()
                self.successful = False
            else:
                self.successful = True

        @property
        def ready(self):
            return self._Thread__stopped

        @property
        def started(self):
            return self._Thread__started.is_set()

        def start(self):
            Thread.start(self)
elif sys.version_info.major == 3:
    class ThreadEx(Thread):  # 线程类
        is_killed = False

        def stop(self):  # 线程停止
            self.is_killed = True
            lock = getattr(self, '_tstate_lock', None)
            if lock and lock.locked(): lock.release()
            self._stop()

        def __init__(self, *args, **kwargs):
            # 线程初始化
            Thread.__init__(self, *args, **kwargs)
            self.successful = None

        def run(self):
            # 重写run方法
            try:
                self.ret = self._target(*self._args, **self._kwargs)
            except:
                self.ret = traceback.format_exc()
                self.successful = False
            else:
                self.successful = True

        @property
        def ready(self):
            # 取线程状态
            return self._is_stopped

        @property
        def started(self):
            return self._started.is_set()

        def start(self):
            # 线程启动
            Thread.start(self)
else:
    raise NotImplementedError('Only for python2 and python3')


class ThreadR:
    """Restore Thread Class Stop and restart many times"""

    def __init__(self, target, name=None, *args, **kw):
        self.target = target
        self.name = name or target.__name__
        self._kw = kw
        self._args = args
        self.th = None

    def start(self):
        if self.th and self.th.is_alive(): self.th.stop()
        self.th = ThreadEx(target=self.target, name=self.name, args=self._args, kwargs=self._kw)
        self.th.start()

    def stop(self):
        self.th.stop()

    def __getattr__(self, item):
        return getattr(self.th, item)


def tryr(func, logger=logging):
    def wapper(*a, **k):
        try:
            return func(*a, **k)
        except:
            wapper.lasterr = traceback.format_exc()
            logger.exception('%s()%s,%s' % (func, str(a), str(k)))

    wapper.lasterr = None
    return wapper

