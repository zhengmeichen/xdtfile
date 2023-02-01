# coding=utf-8
from sqlite import database

import collections

User = collections.namedtuple('User', 'id,user,name,passwd,role,mask,email,tel,dingding,discription,disable')


# 获取用户信息
def get_user(uid=None):
  with database(True) as cur:
    if id:
      # 可以根据user或id进行用户查询
      cur.execute('select * from user where user=? or id=?', (uid, uid))
      r = cur.fetchone()
      return User(**r)


# 获取所有用户信息
def get_users():
  with database(True) as cur:
    cur.execute('select * from user')
    r = cur.fetchall()
  return r


# main.user.user
# main.user.passwd
# main.user.role
# main.user.id
# main.user.name
# main.user.mask
# main.user.email
# main.user.tel
# main.user.discription
# main.user.disable

# 更新用户信息
def set_user(user=None, passwd=None, role=None, name=None, mask=None, email=None,
             tel=None, discription=None, disable=None, dingding=None, id=None):
  kw = vars()
  k = list(i for i, j in kw.items() if j is not None)
  # 新用户直接插入一条新纪录
  if id is None:
    v = tuple(kw[i] for i in k)
    sql = "replace into user ({keys}) values({values})".format(
      keys=",".join(k), values=",".join("?" for i in k))
  else:
    # 先移除id
    k.remove('id')
    # 更新数据
    sql = 'update user set %s where id=? ;' % ','.join('%s=?' % i for i in k)
    # 最后在绑定id
    v = tuple([kw[i] for i in k] + [id])
  # print sql, v
  with database() as cur:
    cur.execute(sql, v)


# 用户名查重
def check_user(uid):
  with database(True) as cur:
    cur.execute('select * from user group by user=? having count(*) > 1', (uid,))
    r = cur.fetchone()
    # print r
  return User(**r)


if __name__ == '__main__':
  with database() as cur, open('init_db.sql', 'r') as r:
    cur.executescript(r.read())
