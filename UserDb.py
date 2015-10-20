# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime

class User:
  db_file = 'users.db'

  def __init__(self, usrname, password,
              nickname='guest', desc='', role='', regts=''):
    self._usrname = usrname
    self._password = password
    self._nickname = nickname
    self._desc = desc
    self.regtime = regts
    self.role = role

  @property
  def usrname(self):
    return self._usrname

  @usrname.setter
  def usrname(self, name):
    self._usrname = name

  @property
  def password(self):
    return self._password

  @password.setter
  def password(self, passwd):
    self._password = passwd

  @property
  def nickname(self):
    return self._nickname

  @nickname.setter
  def nickname(self, nickname):
    self._nickname = nickname

  @property
  def email(self):
    return self._email

  @email.setter
  def email(self, email):
    self._email = email

  @property
  def desc(self):
    return self._desc

  def put(self):
    conn =  sqlite3.connect(User.db_file)
    conn.text_factory = str
    cur = conn.cursor()
    if cur.execute('SELECT * FROM users WHERE name=?', (self.usrname,)).fetchone() is None:
      ts = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
      cur.execute('INSERT INTO users VALUES (?,?,?,?,?,?)',
        (self.usrname, self.password, self.nickname, self.role, self.desc, ts)
      )
    conn.commit()
    cur.close()
    conn.close()

def create_user_table():
  conn =  sqlite3.connect(User.db_file)
  conn.text_factory = str
  cur = conn.cursor()
  try:
    cur.execute('CREATE TABLE users (name text primary key, passwd text, nickname text, role text, des text, regtime text)')
    conn.commit()
  except:
    print 'table users already existing'
  cur.close()
  conn.close()

def del_user(usrname):
 conn =  sqlite3.connect(User.db_file)
 conn.text_factory = str
 cur = conn.cursor()
 cur.execute('DELETE FROM users WHERE name=?', (usrname,))
 conn.commit()
 cur.close()
 conn.close()

def put_admin():
  user = User('admin', '000000', nickname='管理员', role='超级管理员',
              regts='startup', desc="超级管理员（请勿删除）")
  user.put()

def get(usrname):
  conn =  sqlite3.connect(User.db_file)
  conn.text_factory = str
  cur = conn.cursor()
  userinfo = cur.execute('SELECT * FROM users WHERE name=?', (usrname,)).fetchone()
  if userinfo is not None:
    #print userinfo
    username, passwd, nickname, role, desc, regts = userinfo
    return User(username, passwd, nickname=nickname, desc=desc, role=role, regts=regts)
  else:
    return None

def fetch_users():
  "get all users from database"
  conn =  sqlite3.connect(User.db_file)
  conn.text_factory = str
  cur = conn.cursor()
  userinfo = cur.execute('SELECT * FROM users').fetchall()
  cur.close()
  conn.close()
  users = []
  for u in userinfo:
    username, passwd, nickname, role, desc, regts = u
    users.append(User(username, passwd, nickname, desc, role, regts))
  return users

def change_user_info(usr, desc, role, nickname):
  conn =  sqlite3.connect(User.db_file)
  conn.text_factory = str
  cur = conn.cursor()
  userinfo = cur.execute('UPDATE users SET des=?,role=?,nickname=? WHERE name=?',
                         (desc, role, nickname, usr))
  conn.commit()
  cur.close()
  conn.close()

def change_passwd(u, p):
  conn =  sqlite3.connect(User.db_file)
  conn.text_factory = str
  cur = conn.cursor()
  userinfo = cur.execute('UPDATE users SET passwd=? WHERE name=?', (p, u))
  conn.commit()
  cur.close()
  conn.close()

class Role():
  dbfile = 'role.db'
  def __init__(self, rolename='', privileges=[], desc=''):
    self.rolename = rolename
    self.privileges = privileges
    self.desc = desc

  def put(self):
    conn =  sqlite3.connect(Role.dbfile)
    conn.text_factory = str
    cur = conn.cursor()
    try:
      cur.execute('INSERT INTO roles VALUES (?,?,?)',
          (self.rolename, ' '.join(self.privileges), self.desc,))
      conn.commit()
    except Exception as e:
      print e
    finally:
      cur.close()
      conn.close()

def create_role_table():
  conn =  sqlite3.connect(Role.dbfile)
  conn.text_factory = str
  cur = conn.cursor()
  try:
    cur.execute('CREATE TABLE roles (rolename text primary key, priv text, des text)')
    conn.commit()
  except:
    print 'table roles already existing'
  cur.close()
  conn.close()

def add_role(role):
  conn =  sqlite3.connect(Role.dbfile)
  conn.text_factory = str
  cur = conn.cursor()
  try:
    cur.execute('INSERT INTO roles VALUES (?,?,?)',
        (role.rolename, ' '.join(role.privileges), role.desc,))
    conn.commit()
  except Exception as e:
    print e
  finally:
    cur.close()
    conn.close()

def add_root():
  root = Role('超级管理员',
              ['超限处理', '处理审核', '超限处理登记', '超限处理登记审核', '黑名单增删', '黑名单审核', '用户增删'])
  root.put()

def add_default_roles():
  r = Role('管理员', ['处理审核', '登记审核', '黑名单审核'])
  r.put()
  r = Role('操作员', ['超限处理', '超限处理登记', '黑名单增删'])
  r.put()
  r = Role('来宾', [])
  r.put()

def update_privilege(rn, priv):
  conn =  sqlite3.connect(Role.dbfile)
  conn.text_factory = str
  cur = conn.cursor()
  cur.execute('UPDATE roles SET priv=? WHERE rolename=?', (' '.join(priv), rn,))
  conn.commit()
  cur.close()
  conn.close()

def update_role_status_desc(rn, status, desc):
  conn =  sqlite3.connect(Role.dbfile)
  conn.text_factory = str
  cur = conn.cursor()
  cur.execute('UPDATE roles SET status=?, des=? WHERE rolename=?', (status, desc, rn,))
  conn.commit()
  cur.close()
  conn.close()

def get_privilege(rn):
  conn =  sqlite3.connect(Role.dbfile)
  conn.text_factory = str
  cur = conn.cursor()
  p = cur.execute('SELECT * FROM roles WHERE rolename=?', (rn,)).fetchone()

  if p: return p[1].split()
  else: return []

def get_roles():
  conn =  sqlite3.connect(Role.dbfile)
  conn.text_factory = str
  cur = conn.cursor()
  res = cur.execute('SELECT * FROM roles').fetchall()
  cur.close()
  conn.close()
  return res

def del_role(rn):
  conn =  sqlite3.connect(Role.dbfile)
  conn.text_factory = str
  cur = conn.cursor()
  res = cur.execute('DELETE FROM roles WHERE rolename=?', (rn,))
  conn.commit()
  cur.close()
  conn.close()


class Record(object):
  TAB_HDR = ('序号', '站点', '时间', '车牌号', '状态', '轴数', 
            '车速', '车重(吨)', '车道', '限载(吨)', '超限率(%)', '处理登记时间')
  TAB_BRF_HDR = ('序号', '站点', '时间', '车牌号', '车重(吨)', '超限率', '处理状态')

  def __init__(self, seq, recid, siteid, ts, plate, state, wheels, speed, weight, 
               roadnum, wlimit, wlpercent, frntpic, bckpic):
    self.seq = seq
    self.recid = recid
    self.siteid = siteid
    self.ts = ts
    self.plate = plate
    self.state = state
    self.wheels = wheels
    self.speed = speed
    self.weight = weight
    self.roadnum = roadnum
    self.wlimit = wlimit
    self.wlpercent = wlpercent
    self.frntpic = frntpic
    self.bckpic = bckpic


  def put():
    pass


class ProceedState:
  APPROVING = 1
  APPROVED = 2
  REGISTERING = 3
  REGISTERED = 4

  def __init__(self):
    pass

class BlackList:
  REQUESTING = 0
  DELETING = 1
  APPROVED = 2

  def __init__(self): pass





