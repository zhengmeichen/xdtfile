# coding=utf-8
import json
import binascii
import urllib
import hashlib


def update(request, dbo, tob, **kwargs):
  # 获取传入数据,params后面接data里边的参数名称
  r = request.params.msg
  # base64解密json序列
  r = binascii.a2b_base64(r)
  # 解码encodeURI
  r = urllib.unquote(r)
  # print r
  r = json.loads(r)
  print r

  # 之前查询是为了获得user里边的密码,对密码进行验证
  user = dbo.get_user(uid=r['id'])
  print 'user', user, user.passwd

  # 更改用户名,在数据库中查重
  # 用户名不一致
  if r['user'] != user.user:
    # 用户名查重
    c = dbo.check_user(uid=r['user'])
    if c.user != None:
      print 'already have user'
      return dict(status=0, msg="already have user")
    else:
      # 旧密码验证,md5加密对比
      if 'passwd' in r:
        # 传入密码才进行比对
        key = request.params.key
        if hashlib.md5(tob(request.remote_addr + ':' + user.passwd + ':')).hexdigest() == key:
          # 将更新的所有数据写回数据库
          dbo.set_user(**r)
        # 更新session信息
        request.session['user'] = dbo.get_user(uid=r['id'])
        return dict(status=1)
      else:
        # 更新除密码以外内容,将密码设置为原数据库密码
        dbo.set_user(passwd=user.passwd, **r)
        # 更新session信息
        request.session['user'] = dbo.get_user(uid=r['id'])
        return dict(status=1)

  else:
    # 旧密码验证,md5加密对比
    if 'passwd' in r:
      # 传入密码才进行比对
      key = request.params.key
      if hashlib.md5(tob(request.remote_addr + ':' + user.passwd + ':')).hexdigest() == key:
        # 将更新的所有数据写回数据库
        dbo.set_user(**r)
      # 更新session信息
      request.session['user'] = dbo.get_user(uid=r['id'])
      return dict(status=1)
    else:
      # 更新除密码以外内容,将密码设置为原数据库密码
      dbo.set_user(passwd=user.passwd, **r)
      # 更新session信息
      request.session['user'] = dbo.get_user(uid=r['id'])
      return dict(status=1)
