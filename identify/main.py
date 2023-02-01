# coding=utf-8
# WebCore-V3.0

import os
import sys

os.environ['TZ'] = 'UTC'
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, 'xlib')
sys.path.insert(0, 'xlib.zip')
import x_web
import x_log, threading

x_web.debug()
app = x_web.app
g = x_web.page_globals
x_log.logger('root', 'INFO')


def main(_f_, server='wsgiref', port=7001, host='127.0.0.1', *args):
  """ 程序入口函数
  :param _f_:   程序名称
  :param host:  主机IP
  :param port:  端口号
  :param server: 适配器
  :param args: 其他参数
  """
  print(os.getcwd())
  try:
    g.update(threading=threading)
    x_web.run(
      server=server,
      app=x_web.app, host=host, port=port, quiet=False, debug=True)
  finally:
    pass


if __name__ == '__main__':
  try:
    import setproctitle

    setproctitle.setproctitle('CTRL CENTER')
  except:
    pass
  main(*sys.argv)
