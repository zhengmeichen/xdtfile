# coding=utf-8

import views as api
import x_dbo
import x_session
import x_tool
from bottle import *


def _file_iter_range(fp, offset, bytes, maxread=1024 * 1024):
  fp.seek(offset)
  while bytes > 0:
    part = fp.read(min(bytes, maxread))
    if not part: break
    bytes -= len(part)
    yield part


# class A:
#   def __getattr__(self, item): return item
#
#   __getitem__ = __getattr__
#
#
# user_none = A()
user_none = dict()
Response.download = HeaderProperty('Content-Disposition', writer=lambda n: 'attachment; filename="%s"' % n)
Response.info = HeaderProperty('info', writer=lambda n: json_dumps(n), reader=lambda n: json_loads(n))
Request.user = HeaderProperty('user', reader=lambda x: request.session.get('user', None))
Request.session = {}

app = Bottle()

sss = x_session.SessionPlugin(
  cookie_name="SID",
  host='127.0.0.1',
  # host='10.25.18.28',
  port=7005,
  password='9494cfd0f8c829acd9b1a88f9a0fd2ec',
  max_connections=2,
  cookie_httponly=True,
  cookie_secure=True,
)
sss.setup(app)


# dbo =  database operation
class AuthError(Exception): pass


page_globals = dict(
  AuthError=AuthError,
  dbo=x_dbo, tool=x_tool, touni=touni, tob=tob, tonat=tonat,
  datetime=datetime, timedelta=timedelta,
  json_dumps=json_dumps, json_loads=json_loads,
  html_quote=html_quote, html_escape=html_escape,
  abort=abort, request=request, response=response,
  format_exc=format_exc, print_exc=print_exc,
  mako_template=mako_template, BytesIO=BytesIO,
  static_file=static_file, local=local, guess_type=mimetypes.guess_type
)

app.route('/static/<path:path>')(lambda path: static_file(path, root='static'))
## app.config['SECRET_KEY'] = '!@#$%^&*()_+<>?:"'
CROS_HEADERS = {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*',
                'Access-Control-Allow-Headers': 'x-requested-with,content-type'}


@app.route('/favicon.ico')
def favicon():
  return static_file('favicon.png', root='static')


def auth(func):
  def wrapper(*a, **ka):
    if request.user:
      return func(*a, **ka)
    return mako_template('login.mako', page_globals)

  return wrapper


@app.route('/admin/<path:path>', method=('POST', 'GET'))
@auth
def admin(path):
  return mako_template('admin/' + path + '.mako', page_globals, format_exceptions=True)


@app.route('/api.admin.<func>', method=('POST', 'GET'))
def admin_api(func):
  if not request.user:
    return abort(401, 'Admin Login required')
  return runapi('admin.%s' % func)


@app.route('/api.<func>', method=('POST', 'GET'))
def norm_api(func):
  return runapi(func)


def runapi(func):
  response.headers.update(CROS_HEADERS)
  try:
    f = api.getfunc(func)
  except ImportError:
    abort(404, u'您访问的 Api-Model 搬冥王星去了，我们无法联系到它')
  except AttributeError:
    abort(404, u'您访问的 Api-Function 搬冥王星去了，我们无法联系到它')
  else:
    return f(**page_globals)


@app.route('/', method=('POST', 'GET'))
def m():
  redirect('/main')


@app.route('/<path:path>', method=('POST', 'GET'))
def auto(path):
  if os.path.exists('views/' + path + '.mako'):
    try:
      return mako_template(path + '.mako', page_globals, format_exceptions=True)
    except AuthError:
      return mako_template('login.mako', page_globals, format_exceptions=True)
  else:
    abort(404, u'您访问的页面搬冥王星去了，我们无法联系到它')


@app.error(404)
def _error_404(error_handler): return mako_template(
  '404.mako', page_globals, error_handler=error_handler, format_exceptions=True)


@app.hook('after_request')
def _enable_cors():  response.set_header('Access-Ctrl-Allow-Origin', '*')


if __name__ == '__main__':
  app.run(port=4000, debug=True)
