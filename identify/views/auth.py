# coding=utf-8
import hashlib


def login(request, dbo, tob, **kwargs):
  c = request.session.get('AuthKey', '')
  r = request.params
  user = r.user
  key = r.key
  try:
    user = dbo.get_user(uid=user)
  except:
    import traceback
    traceback.print_exc()
    return dict(isok=False, msg='用户错误')

  if hashlib.md5(tob(request.remote_addr + ':' + user.passwd + ':' + c)).hexdigest() == key:
    request.user = user
    request.session['user'] = user
    del request.session['AuthKey']
    return dict(isok=True)
  else:
    return dict(isok=False, c=c, h=request.session.session_hash)


def logout(request, **k):
  request.session.destroy()
  return dict(isok=True)


def test(request, **k):
  return dict(r=dir(request),
              is_ajax=request.is_ajax,
              is_xhr=request.is_xhr,
              remote_addr=request.remote_addr,
              remote_route=request.remote_route)
