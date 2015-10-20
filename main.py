#!/bin/python
#-*- coding: utf-8 -*-

"""
  Simple web server for local application management, based on bottle framework
  Author: haitong.chen@gmail.com
"""

import sys

import time, urllib2, sqlite3, re, socket, os, json, httpagentparser
#import time, urllib2, sqlite3
#import SqlCmdHelper
from datetime import datetime
from subprocess import Popen
from multiprocessing import Process
from bottle import route, request, redirect, template,static_file, run, app, hook
from ftplib import FTP
from beaker.middleware import SessionMiddleware

# for py2exe module search
import _mssql
import decimal
# end of py2exe module search

import UserDb
import db_man

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 3600,
    'session.data_dir': './data',
    'session.auto': True
}
app = SessionMiddleware(app(), session_opts)

def set_act_user(usrname):
  request.session['logged_in'] = usrname

def get_act_user():
  if 'logged_in' in request.session:
    return request.session['logged_in']
  else:
    return None

def set_browser(browser):
  request.session['browser_type'] = browser

def get_browser():
  return request.session['browser_type']

def cons_query_where_clause(query_mapping):
  #conds = ['=:'.join([col, col]) for col in query_mapping.keys()]
  readflag_str = ''
  if query_mapping.has_key('ReadFlag=%d') and query_mapping['ReadFlag=%d'] is None:
    readflag_str += ' ReadFlag is NULL '
    query_mapping.pop('ReadFlag=%d')
  cond_str = ' and '.join(query_mapping.keys())
  if cond_str and readflag_str: readflag_str += ' and '
  return readflag_str + cond_str, tuple(query_mapping.values())

def cons_query_interval(dates):
  timefmt = '%Y-%m-%d'
  try:
    [datetime.strptime(t, timefmt) for t in dates]
  except:
    return None
  else:
    return dates[0] + ' 00:00:00', dates[1] + ' 23:59:59'

def validate_from_db(usr, passwd):
  user = UserDb.get(usr)
  if user is not None and user.usrname == usr and user.password == passwd:
    ret = True, user
  else:
    ret = False, user
  return ret

def init_user_db():
  UserDb.create_user_table()
  UserDb.create_role_table()
  UserDb.add_root()
  UserDb.add_default_roles()
  UserDb.put_admin()

@hook('before_request')
def setup_request():
    request.session = request.environ['beaker.session']

@route('/')
def root():
  if get_act_user() is None:
    redirect('/login')
  else:
    redirect('/index')

@route('/login')
def login():
  return template('./view/bsfiles/view/signin.tpl',
                  custom_hdr="./view/bsfiles/view/signin_cus_file.tpl")

@route('/login', method='POST')
def do_login():
  #print request.get('REMOTE_ADDR'), ' connected'
  forgot = None
  usrname = request.forms.get('usrname')
  passwd = request.forms.get('passwd')
  rememberme = request.forms.get('rememberme')

  isvalid, user = validate_from_db(usrname, passwd)
  if isvalid:
    set_act_user(usrname)
    redirect('/index')
  else:
    redirect('/')

@route('/logout')
def logout():
  request.session.delete()
  redirect('/')

@route('/index')
def page_index():
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  try:
    privs = UserDb.get_privilege(UserDb.get(act_user).role)
  except:
    redirect('/login')
  today = datetime.strftime(datetime.now(), '%Y-%m-%d')
  startt = today + ' 00:00:00'
  endt = today + ' 23:59:59'
  results = db_man.period_stat((startt, endt))
  sites = list(results[0].keys())
  numofsite = len(sites)
  # following code for javascript, obsolete now
  #stat = []
  #for res in results:
  #  temp = []
  #  for site in sites:
  #    temp.append(res[site])
  #  stat += temp
  #print numofsite, '|'.join(sites), stat
  return template('./view/bsfiles/view/dashboard.tpl',
                  custom_hdr='./view/bsfiles/view/dashboard_cus_file.tpl',
                  user=act_user, query_results='./view/bsfiles/view/query_rslts.tpl',
                  #results=db_man.fetch_all_bad_brf(30),
                  #stat=json.dumps(stat), sites='|'.join(sites), 
                  numofsite=numofsite, sites=sites, stat=results,
                  siteids=db_man.get_site_ids(), period=today,
                  startdate="2015-06-25", enddate="2015-06-25", siteid=1,
                  privs=privs)

@route('/statdata', method='POST')
def stat():
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  try:
    privs = UserDb.get_privilege(UserDb.get(act_user).role)
  except:
    redirect('/login')
  siteid = request.forms.get('SiteID')
  startdate = request.forms.get('startdate')
  enddate = request.forms.get('enddate')
  period = ''
  if startdate and enddate:
    startt = startdate + ' 00:00:00'
    endt = enddate + ' 23:59:59'
    period = '%s~%s'%(startdate, enddate)
  else:
    today = datetime.strftime(datetime.now(), '%Y-%m-%d')
    startt = today + ' 00:00:00'
    endt = today + ' 23:59:59'
    period = today
  results, percent_results = db_man.period_stat((startt, endt), siteid=siteid, percent=True)
  sites = list(results[0].keys())
  numofsite = len(sites)

  return template('./view/bsfiles/view/dashboard.tpl',
                  custom_hdr='./view/bsfiles/view/dashboard_cus_file.tpl',
                  user=act_user, query_results='./view/bsfiles/view/query_rslts.tpl',
                  numofsite=numofsite, sites=sites, stat=results,
                  siteids=db_man.get_site_ids(), period=period, percent=percent_results,
                  startdate=startdate, enddate=enddate, siteid=siteid, 
                  privs=privs)

@route('/query')
def query():
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  try:
    privs = UserDb.get_privilege(UserDb.get(act_user).role)
  except:
    redirect('/login')
  return template('./view/bsfiles/view/vehicle_query.tpl',
                  custom_hdr='./view/bsfiles/view/dashboard_cus_file.tpl',
                  user=act_user, startdate='2015-06-25',
                  enddate='2015-06-25', ReadFlag="",
                  smState="", smLimitWeightPercent="",
                  VehicheCard="", smTotalWeight="",
                  smWheelCount="",
                  privs=privs, results=None)

@route('/query', method="POST")
def send_query_results():
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  try:
    privs = UserDb.get_privilege(UserDb.get(act_user).role)
  except:
    redirect('/login')

  fields = ('ReadFlag=%d', 'smState=%s', 'smWheelCount=%d', 'SiteID=%d',
            'VehicheCard=%s', 'smLimitWeightPercent>%d', 'smTotalWeight=%d')
  values = {}
  for f in fields:
    value = request.forms.get(re.split('>|=', f)[0])
    try:
      if '.' in value: values[f] = float(value)
      else: values[f] = int(value)
    except:
      if value:
        if value == 'None': values[f] = None
        else: values[f] = value.decode('utf-8')
  cond = cons_query_where_clause(values)
  interval = cons_query_interval(map(request.forms.get, ['startdate', 'enddate']))
  print cond
  results = db_man.fetch_cond_recs(cond, interval)
  #details = db_man.fetch_cond_recs(cond, interval, brf=False)
  return template('./view/bsfiles/view/vehicle_query.tpl',
                  custom_hdr='./view/bsfiles/view/dashboard_cus_file.tpl',
                  user=act_user, privs=privs, startdate=request.forms.get('startdate'),
                  enddate=request.forms.get('enddate'), ReadFlag=request.forms.get('ReadFlag'),
                  smState=request.forms.get('smState'), smLimitWeightPercent=request.forms.get('smLimitWeightPercent'),
                  VehicheCard=request.forms.get('VehicheCard'), smTotalWeight=request.forms.get('smTotalWeight'),
                  smWheelCount=request.forms.get('smWheelCount'),
                  results=results)

@route('/details/<seq>')
def show_detail(seq):
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  try:
    privs = UserDb.get_privilege(UserDb.get(act_user).role)
  except:
    redirect('/login')
  imgpath = ''
  agent = request.environ.get('HTTP_USER_AGENT')
  browser = httpagentparser.simple_detect(agent)[1]
  if 'Microsoft' in browser:
    imgpath = db_man.fpth
  else:
    imgpath = db_man.ftpp
  print imgpath
  detail = db_man.query_detail_by_seq(int(seq))
  panel = "panel-info"
  if detail[1][4] == '1': panel = 'panel-danger'
  isblack, history_recs = db_man.query_history_by_plate(detail[-1][3])
  print isblack, history_recs, imgpath
  return template('./view/bsfiles/view/rec_detail.tpl', 
                   custom_hdr=None, panel_type=panel,
                  detail=detail, length=len(detail[0]),
                  isblack=isblack, history_recs=history_recs, 
                  imgpath=imgpath)

@route('/proceed')
def proceed():
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  try:
    privs = UserDb.get_privilege(UserDb.get(act_user).role)
  except:
    redirect('/login')

  return template('./view/bsfiles/view/rec_proceed.tpl',
                  custom_hdr='./view/bsfiles/view/dashboard_cus_file.tpl',
                  user=act_user, startdate='2015-06-25',
                  enddate='2015-06-25', ReadFlag="",
                  smState="", smLimitWeightPercent="",
                  VehicheCard="", smTotalWeight="",
                  smWheelCount="",
                  privs=privs, results=None)

@route('/proceed/<seq>')
def proceed(seq):
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  try:
    privs = UserDb.get_privilege(UserDb.get(act_user).role)
  except:
    redirect('/login')
  try:
    db_man.update_read_flag(int(seq), UserDb.ProceedState.APPROVING)
  except:
    return '更新失败！纪录不存在！%s'%(seq,)
  #redirect('/proceed')

@route('/proceed_query', method='POST')
def proceed_query():
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  try:
    privs = UserDb.get_privilege(UserDb.get(act_user).role)
  except:
    redirect('/login')

  fields = ('ReadFlag=%d', 'SiteID=%d', 'smWheelCount=%d', 'smState=%s',
            'VehicheCard=%s', 'smLimitWeightPercent>%d', 'smTotalWeight=%d')
  values = {}
  for f in fields:
    value = request.forms.get(re.split('=|>', f)[0])
    try:
      if '.' in value: values[f] = float(value)
      else: values[f] = int(value)
    except:
      if value:
        if value == 'None': values[f] = None
        else: values[f] = value.decode('utf-8')
  cond = cons_query_where_clause(values)
  interval = cons_query_interval(map(request.forms.get, ['startdate', 'enddate']))
  results = db_man.fetch_cond_recs(cond, interval)
  #details = db_man.fetch_cond_recs(cond, interval, brf=False)
  return template('./view/bsfiles/view/rec_proceed.tpl',
                  custom_hdr='./view/bsfiles/view/dashboard_cus_file.tpl',
                  user=act_user, privs=privs,
                  results=results, startdate=request.forms.get('startdate'),
                  enddate=request.forms.get('enddate'), ReadFlag=request.forms.get('ReadFlag'),
                  smState=request.forms.get('smState'), smLimitWeightPercent=request.forms.get('smLimitWeightPercent'),
                  VehicheCard=request.forms.get('VehicheCard'), smTotalWeight=request.forms.get('smTotalWeight'),
                  smWheelCount=request.forms.get('smWheelCount'))

@route('/proceed_approval')
def proc_appr():
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  try:
    privs = UserDb.get_privilege(UserDb.get(act_user).role)
  except:
    redirect('/login')

  return template('./view/bsfiles/view/proc_approval.tpl',
                  custom_hdr='./view/bsfiles/view/dashboard_cus_file.tpl',
                  user=act_user, startdate='2015-06-25',
                  enddate='2015-06-25', ReadFlag="",
                  smLimitWeightPercent="",
                  VehicheCard="", smTotalWeight="",
                  smWheelCount="",
                  privs=privs, results=None)

@route('/proceed_approval', method='POST')
def proc_appr():
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  try:
    privs = UserDb.get_privilege(UserDb.get(act_user).role)
  except:
    redirect('/login')

  fields = ('ReadFlag=%d', 'SiteID=%d', 'smWheelCount=%d', 
            'VehicheCard=%s', 'smLimitWeightPercent>%d', 'smTotalWeight=%d')
  values = {}
  for f in fields:
    value = request.forms.get(re.split('>|=', f)[0])
    try:
      if '.' in value: values[f] = float(value)
      else: values[f] = int(value)
    except:
      if value:
        if value == 'None': values[f] = None
        else: values[f] = value.decode('utf-8')
  cond = cons_query_where_clause(values)
  interval = cons_query_interval(map(request.forms.get, ['startdate', 'enddate']))
  results = db_man.fetch_cond_recs(cond, interval)
  #details = db_man.fetch_cond_recs(cond, interval, brf=False)
  return template('./view/bsfiles/view/proc_approval.tpl',
                  custom_hdr='./view/bsfiles/view/dashboard_cus_file.tpl',
                  user=act_user, privs=privs,
                  results=results, startdate=request.forms.get('startdate'),
                  enddate=request.forms.get('enddate'), ReadFlag=request.forms.get('ReadFlag'),
                  smLimitWeightPercent=request.forms.get('smLimitWeightPercent'),
                  VehicheCard=request.forms.get('VehicheCard'), smTotalWeight=request.forms.get('smTotalWeight'),
                  smWheelCount=request.forms.get('smWheelCount'))

@route('/approved/<seq>')
def approved(seq):
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  try:
    privs = UserDb.get_privilege(UserDb.get(act_user).role)
  except:
    redirect('/login')
  try:
    db_man.update_read_flag(int(seq), UserDb.ProceedState.APPROVED)
  except:
    return '更新失败！纪录不存在！%s'%(seq,)
  #redirect('/proceed_approval')

@route('/disapproved/<seq>')
def approved(seq):
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  try:
    privs = UserDb.get_privilege(UserDb.get(act_user).role)
  except:
    redirect('/login')
  try:
    db_man.update_read_flag(int(seq), None)
  except:
    return '更新失败！纪录不存在！%s'%(seq,)
  redirect('/proceed_approval')

@route('/user_roles')
def role_mng():
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  act_user = UserDb.get(act_user)
  return template('./view/setting.tpl', setting='role_mng',
                  roles=UserDb.get_roles(),
                  privs=UserDb.get_privilege(act_user.role),
                  curr_user=get_act_user())

@route('/register')
def register():
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  try:
    privs = UserDb.get_privilege(UserDb.get(act_user).role)
  except:
    redirect('/login')

  return template('./view/bsfiles/view/proc_rec.tpl',
                  custom_hdr='./view/bsfiles/view/dashboard_cus_file.tpl',
                  user=act_user, startdate='2015-06-25',
                  enddate='2015-06-25', ReadFlag="",
                  smLimitWeightPercent="",
                  VehicheCard="", smTotalWeight="",
                  smWheelCount="",
                  privs=privs, results=None)

@route('/register', method='POST')
def register():
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  try:
    privs = UserDb.get_privilege(UserDb.get(act_user).role)
  except:
    redirect('/login')

  fields = ('ReadFlag=%d', 'SiteID=%d', 'smWheelCount=%d', 
            'VehicheCard=%s', 'smLimitWeightPercent>%d', 'smTotalWeight=%d')
  values = {}
  for f in fields:
    value = request.forms.get(re.split('=|>', f)[0])
    try:
      if '.' in value: values[f] = float(value)
      else: values[f] = int(value)
    except:
      if value:
        if value == 'None': values[f] = None
        else: values[f] = value.decode('utf-8')
  cond = cons_query_where_clause(values)
  interval = cons_query_interval(map(request.forms.get, ['startdate', 'enddate']))
  results = db_man.fetch_cond_recs(cond, interval)
  #details = db_man.fetch_cond_recs(cond, interval, brf=False)
  return template('./view/bsfiles/view/proc_rec.tpl',
                  custom_hdr='./view/bsfiles/view/dashboard_cus_file.tpl',
                  user=act_user, privs=privs,
                  results=results, startdate=request.forms.get('startdate'),
                  enddate=request.forms.get('enddate'), ReadFlag=request.forms.get('ReadFlag'),
                  smLimitWeightPercent=request.forms.get('smLimitWeightPercent'),
                  VehicheCard=request.forms.get('VehicheCard'), smTotalWeight=request.forms.get('smTotalWeight'),
                  smWheelCount=request.forms.get('smWheelCount'))

@route('/register/<seq>', method='POST')
def register(seq):
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  try:
    privs = UserDb.get_privilege(UserDb.get(act_user).role)
  except:
    redirect('/login')
  ts = request.forms.get('regtime')
  print ts
  try:
    db_man.update_read_flag(int(seq), UserDb.ProceedState.REGISTERING)
    if ts: db_man.update_regtime(int(seq), ts)
  except:
    return '更新失败！纪录不存在！%s'%(seq,)
  #redirect('/register')

@route('/reg_approval')
def regappr():
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  try:
    privs = UserDb.get_privilege(UserDb.get(act_user).role)
  except:
    redirect('/login')

  return template('./view/bsfiles/view/reg_approval.tpl',
                  custom_hdr='./view/bsfiles/view/dashboard_cus_file.tpl',
                  user=act_user, startdate='2015-06-25',
                  enddate='2015-06-25', ReadFlag="",
                  smLimitWeightPercent="",
                  VehicheCard="", smTotalWeight="",
                  smWheelCount="",
                  privs=privs, results=None)

@route('/reg_approval', method='POST')
def regappr():
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  try:
    privs = UserDb.get_privilege(UserDb.get(act_user).role)
  except:
    redirect('/login')

  fields = ('ReadFlag=%d', 'SiteID=%d', 'smWheelCount=%d', 
            'VehicheCard=%s', 'smLimitWeightPercent>%d', 'smTotalWeight=%d')
  values = {}
  for f in fields:
    value = request.forms.get(re.split('=|>', f)[0])
    try:
      if '.' in value: values[f] = float(value)
      else: values[f] = int(value)
    except:
      if value:
        if value == 'None': values[f] = None
        else: values[f] = value.decode('utf-8')
  cond = cons_query_where_clause(values)
  interval = cons_query_interval(map(request.forms.get, ['startdate', 'enddate']))
  results = db_man.fetch_cond_recs(cond, interval)
  #details = db_man.fetch_cond_recs(cond, interval, brf=False)
  return template('./view/bsfiles/view/reg_approval.tpl',
                  custom_hdr='./view/bsfiles/view/dashboard_cus_file.tpl',
                  user=act_user, privs=privs,
                  results=results, startdate=request.forms.get('startdate'),
                  enddate=request.forms.get('enddate'), ReadFlag=request.forms.get('ReadFlag'),
                  smLimitWeightPercent=request.forms.get('smLimitWeightPercent'),
                  VehicheCard=request.forms.get('VehicheCard'), smTotalWeight=request.forms.get('smTotalWeight'),
                  smWheelCount=request.forms.get('smWheelCount'))

@route('/registered/<seq>')
def regappr(seq):
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  try:
    privs = UserDb.get_privilege(UserDb.get(act_user).role)
  except:
    redirect('/login')
  try:
    db_man.update_read_flag(int(seq), UserDb.ProceedState.REGISTERED)
  except:
    return '更新失败！纪录不存在！%s'%(seq,)
  redirect('/reg_approval')

@route('/blacklist_query')
def blquery():
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  try:
    privs = UserDb.get_privilege(UserDb.get(act_user).role)
  except:
    redirect('/login')

  return template('./view/bsfiles/view/blacklist_query.tpl',
                  custom_hdr='./view/bsfiles/view/dashboard_cus_file.tpl',
                  user=act_user,
                  privs=privs, blist=db_man.get_blacklist())

@route('/blacklist_mng')
def blmng():
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  try:
    privs = UserDb.get_privilege(UserDb.get(act_user).role)
  except:
    redirect('/login')

  return template('./view/bsfiles/view/blacklist_mng.tpl',
                  custom_hdr='./view/bsfiles/view/dashboard_cus_file.tpl',
                  user=act_user,
                  privs=privs, blist=db_man.get_blacklist())

@route('/request_black', method='POST')
def reqbl():
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  try:
    privs = UserDb.get_privilege(UserDb.get(act_user).role)
  except:
    redirect('/login')

  plate = request.forms.get('plate').decode('utf-8')
  db_man.add_blacklist(plate)
  redirect('/blacklist_mng')

@route('/del_black/<seq>', method='POST')
def delblack(seq):
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  try:
    privs = UserDb.get_privilege(UserDb.get(act_user).role)
  except:
    redirect('/login')

  db_man.update_blacklist_state(seq, UserDb.BlackList.DELETING)
  redirect('/blacklist_mng')

@route('/cancel_black/<seq>', method='POST')
def cancel(seq):
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  try:
    privs = UserDb.get_privilege(UserDb.get(act_user).role)
  except:
    redirect('/login')

  db_man.cancel_blacklist_state(seq)
  redirect('/blacklist_mng')

@route('/blacklist_approval')
def blappr():
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  try:
    privs = UserDb.get_privilege(UserDb.get(act_user).role)
  except:
    redirect('/login')

  return template('./view/bsfiles/view/blacklist_approval.tpl',
                  custom_hdr='./view/bsfiles/view/dashboard_cus_file.tpl',
                  user=act_user,
                  privs=privs, blist=db_man.get_blacklist())

@route('/disappr_blacklist/<seq>')
def disappr(seq):
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  try:
    privs = UserDb.get_privilege(UserDb.get(act_user).role)
  except:
    redirect('/login')

  db_man.cancel_blacklist_state(seq)
  redirect('/blacklist_approval')

@route('/appr_blacklist/<seq>')
def disappr(seq):
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  try:
    privs = UserDb.get_privilege(UserDb.get(act_user).role)
  except:
    redirect('/login')

  db_man.confirm_blacklist_state(seq)
  redirect('/blacklist_approval')

@route('/add_role', method='POST')
def add_role():
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  act_user = UserDb.get(act_user)
  rolename = request.forms.get('rn')
  op = request.forms.get('create')
  if op and rolename:
    r = UserDb.Role(rolename=rolename)
    #UserDb.add_role(r)
    r.put()
    redirect('/user_roles')
  else:
    op = request.forms.get('query')
    if op:
      redirect('/user_roles')

@route('/del_role/<rolename>')
def del_role(rolename):
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  act_user = UserDb.get(act_user)
  UserDb.del_role(rolename)
  return rolename, '已删除'

@route('/edit_role/<rolename>')
def edit_role(rolename):
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  act_user = UserDb.get(act_user)
  return template('./view/setting.tpl', setting='edit_role',
                  roles=UserDb.get_roles(), privs=UserDb.get_privilege(act_user.role),
                  role2edit=rolename, curr_user=get_act_user())

@route('/edit_role/<rolename>', method='POST')
def edit_role(rolename):
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  act_user = UserDb.get(act_user)
  desc = request.forms.get('desc')
  status = request.forms.get('status')
  print desc, status, rolename
  UserDb.update_role_status_desc(rolename, status, desc)
  redirect('/user_roles')

@route('/access_control')
def access_control():
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  act_user = UserDb.get(act_user)
  return template('./view/setting.tpl', setting='access_granting',
                  roles=UserDb.get_roles(),
                  privs=UserDb.get_privilege(act_user.role),
                  curr_user=get_act_user())

@route('/access_grant', method='POST')
def grant():
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  act_user = UserDb.get(act_user)
  privs = ['sys', 'query', 'vehicle', 'driver', 'company', 'ship']
  granted = []
  for priv in privs:
    if request.forms.get(priv):
      granted.append(priv)
  role = request.forms.get('grant')
  print role
  UserDb.update_privilege(role, granted)

@route('/account_mngn')
def account_mngn():
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  try:
    privs = UserDb.get_privilege(UserDb.get(act_user).role)
  except:
    redirect('/login')
  return template('./view/bsfiles/view/usr_mng.tpl',
                  custom_hdr='./view/bsfiles/view/dashboard_cus_file.tpl',
                  user=act_user,
                  usrs=UserDb.fetch_users(),
                  privs=privs)

@route('/del_user/<usrname>', method='POST')
def del_user(usrname):
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  print usrname, 'is going to be deleted'
  UserDb.del_user(usrname)
  redirect('/account_mngn')

@route('/edit_user/<usrname>')
def edit_user(usrname):
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  act_user = UserDb.get(act_user)
  return template('./view/setting.tpl', setting='edit_user',
                  privs=UserDb.get_privilege(act_user.role),
                  usrname=usrname, roles=UserDb.get_roles(),
                  curr_user=get_act_user())

@route('/edit_user/<usrname>', method='POST')
def edit_user(usrname):
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  act_user = UserDb.get(act_user)
  nickname = request.forms.get('nickname')
  desc = request.forms.get('desc')
  role = request.forms.get('role')
  print usrname, nickname, desc, role
  UserDb.change_user_info(usrname, desc, role, nickname)
  redirect('/account_mngn')

@route('/account_query', method="POST")
def account_query():
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  act_user = UserDb.get(act_user)
  user = request.forms.get('account')
  if request.forms.get('query'):
    return template('./view/setting.tpl', setting="accounts",
                    users=[UserDb.get(user)],
                    privs=UserDb.get_privilege(act_user.role),
                    curr_user=get_act_user())
  elif request.forms.get('create'):
    redirect('/user_update')

@route('/user_update')
def update_user():
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  act_user = UserDb.get(act_user)
  return template('./view/setting.tpl', setting="adduser",
                  roles=UserDb.get_roles(),
                  privs=UserDb.get_privilege(act_user.role),
                  curr_user=get_act_user())

@route('/update_user', method='POST')
def update_user():
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  print 'update user'
  if request.forms.get('op') == 'update':
    usrname = request.forms.get('usrname')
    passwd  = request.forms.get('passwd')
    role    = request.forms.get('role')
    desc    = request.forms.get('desc')
    nickname= request.forms.get('nickname')
    print usrname, nickname
    newuser = UserDb.User(usrname, passwd, nickname=nickname, desc=desc, role=role)
    newuser.put()
  else:
    print 'user update cancelled!'
  redirect('/account_mngn')

@route('/del_user/<usrname>')
def del_user(usrname):
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  act_user = UserDb.get(act_user)
  UserDb.del_user(usrname)
  redirect('/account_mngn')

@route('/change_passwd')
def change_passwd():
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  act_user = UserDb.get(act_user)
  return template('./view/setting.tpl', setting="change_password",
                  privs=UserDb.get_privilege(act_user.role),
                  curr_user=get_act_user())

@route('/change_passwd', method='POST')
def update_passwd():
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  act_user = UserDb.get(act_user)
  passwd = request.forms.get('newpass')
  cnfm_passwd = request.forms.get('confirmedpass')
  if passwd != cnfm_passwd:
    return '新密码两次输入不一致，请返回重试!'
  UserDb.change_passwd(act_user.usrname, passwd)
  redirect('/index')

@route('/static/<filename:path>')
def send_static(filename):
  return static_file(filename, root='./')


def main():
  db_man.get_param()
  db_man.create_tables()
  init_user_db()
  #websvr = Process(target=run, args=(app, 'wsgiref', '0.0.0.0', '8081'))
  #websvr.start()
  #websvr.join()
  run(app, host='0.0.0.0', port=8081, server='cherrypy')
  #run(app, host='0.0.0.0', port=8081)


if __name__ == '__main__':
  main()
  #test_ftp()
