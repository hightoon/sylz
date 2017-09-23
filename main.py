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
from datetime import datetime, timedelta
from subprocess import Popen
from multiprocessing import Process
from bottle import route, request, redirect, template,static_file, run, app, hook
from ftplib import FTP
from beaker.middleware import SessionMiddleware

from PIL import Image

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

def save_query_conditions(cond, interval):
  request.session['cond'] = cond
  request.session['interval'] = interval

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

def ms_cons_query_where_clause(query_mapping, sites=None, percent_range=[0, 100]):
  #conds = ['=:'.join([col, col]) for col in query_mapping.keys()]
  readflag_str = ''
  if query_mapping.has_key('ReadFlag=%d') and query_mapping['ReadFlag=%d'] is None:
    readflag_str += ' ReadFlag is NULL '
    query_mapping.pop('ReadFlag=%d')
  cond_str = ' and '.join(query_mapping.keys())
  if cond_str and readflag_str: readflag_str += ' and '
  site_cond = ''
  if sites:
    site_cond = '(' + ' OR '.join(['SiteID=%d'] * len(sites)) + ')'
  if cond_str and site_cond: cond_str += ' and '
  percent_low, percent_high = percent_range
  percent = ''
  if percent_low and percent_high:
    percent = '(smLimitWeightPercent>%d AND smLimitWeightPercent<%d)'
  if site_cond and percent: site_cond += ' and '
  return readflag_str + cond_str + site_cond + percent, tuple(query_mapping.values() + sites + percent_range)

def store_stat_query(siteid, startdate, enddate):
  request.session['stat-siteid'] = siteid
  request.session['stat-startdate'] = startdate
  request.session['stat-enddate'] = enddate

def cons_query_interval(dates, timerange):
  timefmt = '%Y-%m-%d'
  try:
    [datetime.strptime(t, timefmt) for t in dates]
  except:
    return None
  else:
    return dates[0] + ' ' + timerange[0] + ':00', dates[1] + ' ' + timerange[1] + ':59'

def cons_query_multi_interval(dates, timerange):
  timefmt = '%Y-%m-%d'
  try:
    startd, endd = [datetime.strptime(t, timefmt) for t in dates]
  except:
    return None
  else:
    intervals = []
    for d in xrange(abs(endd - startd).days):
      cur = startd + timedelta(days=d)
      intervals.append((cur.strftime(timefmt) + ' ' + timerange[0] + ':00',
                        cur.strftime(timefmt) + ' ' + timerange[1] + ':59'))
    return intervals

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

@route('/mlogin', method='GET')
def do_login():
  usrname = request.GET.get('usrname')
  passwd = request.GET.get('passwd')

  isvalid, user = validate_from_db(usrname, passwd)
  if isvalid:
    set_act_user(usrname)
    return {'response': 'ok'}
  else:
    return {'response': 'error'}

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
  request.session['stat-siteid'] = None
  today = datetime.strftime(datetime.now(), '%Y-%m-%d')
  #startdate = today + ' 00:00:00'
  #enddate = today + ' 23:59:59'
  #period = '%s~%s'%(startdate, enddate)
  #results, percent_results = db_man.period_stat((startdate, enddate), siteid=1, percent=True)
  #sites = list(results[0].keys())
  #numofsite = len(sites)
  #sites = list(results[0].keys())
  #numofsite = len(sites)
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
                  user=act_user, #query_results='./view/bsfiles/view/query_rslts.tpl',
                  query_results=None,
                  #results=db_man.fetch_all_bad_brf(30),
                  #stat=json.dumps(stat), sites='|'.join(sites),
                  #numofsite=numofsite, sites=sites, stat=results,
                  siteids=db_man.get_site_ids(), period=today,  #percent=percent_results,
                  startdate=today, enddate=today, sitenames=db_man.get_sites(),
                  siteid=db_man.get_site_ids()[0],
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
  store_stat_query(siteid, startt, endt)
  results, percent_results = db_man.period_stat((startt, endt), siteid=siteid, percent=True)
  sites = list(results[0].keys())
  numofsite = len(sites)

  if request.forms.get('export'):
    if siteid=="":
      return "请选择需要导出数据的站点，选择全部无法导出站点数据!"
    import csv
    reload(sys)
    sys.setdefaultencoding('utf8')
    exptime = datetime.strftime(datetime.now(), '%Y%m%dT%H%M%S')
    csvname = 'tongji%s.csv'%exptime
    with open(csvname, 'wb') as csvfile:
      writer = csv.writer(csvfile, dialect='excel')
      writer.writerow(('站点', '时段', '超限车次',))
      for s in xrange(numofsite):
        for h in xrange(24):
          writer.writerow((sites[s], '%2d:00-%2d:00'%(h, h+1), results[h][sites[s]]))
    return "<a href=\"/static/%s\">打开统计报告</a>"%csvname

  return template('./view/bsfiles/view/dashboard.tpl',
                  custom_hdr='./view/bsfiles/view/dashboard_cus_file.tpl',
                  user=act_user, query_results='./view/bsfiles/view/query_rslts.tpl',
                  numofsite=numofsite, sites=sites, stat=results, sitenames=db_man.get_sites(),
                  siteids=db_man.get_site_ids(), period=period, percent=percent_results,
                  startdate=startdate, enddate=enddate, siteid=siteid,
                  privs=privs)

@route('/stat/json')
def statjson():
  if not request.session.has_key('stat-siteid') or request.session['stat-siteid'] is None: return {'data': 'notok'}
  hourdata, percent = db_man.period_stat((request.session['stat-startdate'], request.session['stat-enddate']), 
      siteid=request.session['stat-siteid'], percent=True)
  if hourdata:
    site = hourdata[0].keys()[0]
    hourdata = [d[site] for d in hourdata]
    hourdatax = ['%.2d:00-%.2d:00'%(x, x+1) for x in xrange(24)]
  print hourdata
  return {'data': [{
    'values': percent[percent.keys()[0]],
    'labels': ['正常', '轻微', '一般', '严重', '特别严重'],
    'type': 'pie'
    }],
    'bardata': [{
      'x': hourdatax,
      'y': hourdata,
      'type': 'bar'
    }]
  }


@route('/statdata/export')
def export():
  return 'ok, data exported.'

@route('/query')
def query():
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  try:
    privs = UserDb.get_privilege(UserDb.get(act_user).role)
  except:
    redirect('/login')
  today = datetime.strftime(datetime.now(), '%Y-%m-%d')
  return template('./view/bsfiles/view/vehicle_query_auto.tpl',
                  custom_hdr='./view/bsfiles/view/dashboard_cus_file.tpl',
                  user=act_user, startdate=today,
                  enddate=today, ReadFlag="",
                  smState="", smLimitWeightPercent="",
                  VehicheCard="", smTotalWeight="", SiteID=db_man.get_sites(),
                  smWheelCount="", sites=db_man.get_sites(),
                  starttime='00:00', endtime='23:59',
                  privs=privs, results=[UserDb.Record.TAB_BRF_HDR])

@route('/query', method="POST")
def send_query_results():
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  try:
    privs = UserDb.get_privilege(UserDb.get(act_user).role)
  except:
    redirect('/login')

  inplate = request.forms.get('VehicheCard').decode('utf-8')
  fields = ('ReadFlag=%d', 'smState=%s', 'smWheelCount=%d', 'SiteID=%d',
            'smLimitWeightPercent>%d', 'smTotalWeight>%d')
  values = {}
  for f in fields:
    value = request.forms.get(re.split('>|=| like ', f)[0])
    try:
      if '.' in value: values[f] = float(value)
      else: values[f] = int(value)
    except:
      if value:
        if value == 'None': values[f] = None
        else:
          values[f] = value.decode('utf-8')
  cond = cons_query_where_clause(values)
  interval = cons_query_interval(map(request.forms.get, ['startdate', 'enddate']))
  hourange = request.forms.get('timeInterval')
  if hourange and interval[0][:10] == interval[1][:10]:
    starthour, endhour = tuple(hourange.split('-'))
    interval = (interval[0][:10]+' '+starthour, interval[1][:10]+' '+endhour)
  #print cond
  results = db_man.fetch_cond_recs(cond, interval, inplate=inplate)
  #details = db_man.fetch_cond_recs(cond, interval, brf=False)

  return template('./view/bsfiles/view/vehicle_query.tpl',
                  custom_hdr='./view/bsfiles/view/dashboard_cus_file.tpl',
                  user=act_user, privs=privs, startdate=request.forms.get('startdate'),
                  enddate=request.forms.get('enddate'), ReadFlag=request.forms.get('ReadFlag'),
                  smState=request.forms.get('smState'), smLimitWeightPercent=request.forms.get('smLimitWeightPercent'),
                  VehicheCard=request.forms.get('VehicheCard'), smTotalWeight=request.forms.get('smTotalWeight'),
                  smWheelCount=request.forms.get('smWheelCount'), SiteID=request.forms.get('SiteID'),
                  sites=db_man.get_sites(),
                  results=results)

@route('/query/multisites', method="POST")
def send_query_results():
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  try:
    privs = UserDb.get_privilege(UserDb.get(act_user).role)
  except:
    redirect('/login')

  sites_selected = request.forms.getall('SiteID')
  #print('sites selected:', sites_selected)
  if sites_selected: 
    sites_selected = sites_selected[0].split(',')
  percent_low = request.forms.get('smLimitWeightPercentLow')
  percent_high = request.forms.get('smLimitWeightPercentHigh')
  try:
    percent_low, percent_high = int(percent_low), int(percent_high)
  except:
    percent_low, percent_high = 0, 100
  print percent_low, percent_high
  inplate = request.forms.get('VehicheCard').decode('utf-8')
  fields = ('ReadFlag=%d', 'smState=%s', 'smWheelCount=%d',
            'smTotalWeight>%d')
  values = {}
  for f in fields:
    value = request.forms.get(re.split('>|=| like ', f)[0])
    try:
      if '.' in value: values[f] = float(value)
      else: values[f] = int(value)
    except:
      if value:
        if value == 'None': values[f] = None
        else:
          values[f] = value.decode('utf-8')
  cond = ms_cons_query_where_clause(values, map(int, sites_selected), [percent_low, percent_high])
  interval = cons_query_interval(map(request.forms.get, ['startdate', 'enddate']), 
                                 map(request.forms.get, ['starttime', 'endtime']))
  #hourange = request.forms.get('timeInterval')
  #if hourange and interval[0][:10] == interval[1][:10]:
  #  starthour, endhour = tuple(hourange.split('-'))
  #  interval = (interval[0][:10]+' '+starthour, interval[1][:10]+' '+endhour)
  st, et = map(request.forms.get, ['starttime', 'endtime'])
  save_query_conditions(cond, interval)
  results = []
  #for interval in intervals:
  results = db_man.fetch_cond_recs(cond, interval, inplate=inplate)
  #results = [r for r in results if st < r[2].split()[1] < et] #r[2] is very ugly, i know it
  #details = db_man.fetch_cond_recs(cond, interval, brf=False)
  if results:
    tab_hd = results[0]
    results = results[1:] #remove tab header
  data = [r for r in results if st < r[2].split()[1] < et]
  data = [[float(d) if type(d)==decimal.Decimal else d for d in r] for r in data]
  return {'data': data}
  '''
  return template('./view/bsfiles/view/vehicle_query_auto.tpl',
                  custom_hdr='./view/bsfiles/view/dashboard_cus_file.tpl',
                  user=act_user, privs=privs, startdate=request.forms.get('startdate'),
                  enddate=request.forms.get('enddate'), ReadFlag=request.forms.get('ReadFlag'),
                  smState=request.forms.get('smState'), smLimitWeightPercent=request.forms.get('smLimitWeightPercent'),
                  VehicheCard=request.forms.get('VehicheCard'), smTotalWeight=request.forms.get('smTotalWeight'),
                  smWheelCount=request.forms.get('smWheelCount'), SiteID=''.join(request.forms.getall('SiteID')),
                  sites=db_man.get_sites(), starttime='00:00', endtime='23:59',
                  results=results)
  '''

@route('/query/multisites/rawdata')
def sites_data():
  cond = request.session['cond']
  interval = request.session['interval']
  print cond, interval
  results = db_man.fetch_cond_recs(cond, interval)
  st, et = [t.split()[1] for t in request.session['interval']]
  print st, et
  data = [r for r in results[1:] if st < r[2].split()[1] < et]
  data = [[float(d) if type(d)==decimal.Decimal else d for d in r] for r in data]
  return {'data': data}

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

  today = datetime.strftime(datetime.now(), '%Y-%m-%d')
  return template('./view/bsfiles/view/rec_proceed.tpl',
                  custom_hdr='./view/bsfiles/view/dashboard_cus_file.tpl',
                  user=act_user, startdate=today,
                  enddate=today, ReadFlag="None",
                  smState="", smLimitWeightPercent="",
                  VehicheCard="", smTotalWeight="",
                  smWheelCount="", SiteID="", sites=db_man.get_sites(),
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

  inplate = request.forms.get('VehicheCard').decode('utf-8')
  fields = ('ReadFlag=%d', 'SiteID=%d', 'smWheelCount=%d', 'smState=%s',
            'smLimitWeightPercent>%d', 'smTotalWeight>%d')
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
  hourange = request.forms.get('timeInterval')
  if hourange and interval[0][:10] == interval[1][:10]:
    starthour, endhour = tuple(hourange.split('-'))
    interval = (interval[0][:10]+' '+starthour, interval[1][:10]+' '+endhour)
  results = db_man.fetch_cond_recs(cond, interval, inplate=inplate)
  #details = db_man.fetch_cond_recs(cond, interval, brf=False)
  return template('./view/bsfiles/view/rec_proceed.tpl',
                  custom_hdr='./view/bsfiles/view/dashboard_cus_file.tpl',
                  user=act_user, privs=privs,
                  results=results, startdate=request.forms.get('startdate'),
                  enddate=request.forms.get('enddate'), ReadFlag=request.forms.get('ReadFlag'),
                  smState=request.forms.get('smState'), smLimitWeightPercent=request.forms.get('smLimitWeightPercent'),
                  VehicheCard=request.forms.get('VehicheCard'), smTotalWeight=request.forms.get('smTotalWeight'),
                  SiteID=request.forms.get('SiteID'), sites=db_man.get_sites(),
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

  today = datetime.strftime(datetime.now(), '%Y-%m-%d')
  return template('./view/bsfiles/view/proc_approval.tpl',
                  custom_hdr='./view/bsfiles/view/dashboard_cus_file.tpl',
                  user=act_user, startdate=today,
                  enddate=today, ReadFlag="1",
                  smLimitWeightPercent="",
                  VehicheCard="", smTotalWeight="",
                  smWheelCount="", SiteID="", sites=db_man.get_sites(),
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

  inplate = request.forms.get('VehicheCard').decode('utf-8')
  fields = ('ReadFlag=%d', 'SiteID=%d', 'smWheelCount=%d',
            'smLimitWeightPercent>%d', 'smTotalWeight>%d')
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
  hourange = request.forms.get('timeInterval')
  if hourange and interval[0][:10] == interval[1][:10]:
    starthour, endhour = tuple(hourange.split('-'))
    interval = (interval[0][:10]+' '+starthour, interval[1][:10]+' '+endhour)
  results = db_man.fetch_cond_recs(cond, interval, inplate=inplate)
  #details = db_man.fetch_cond_recs(cond, interval, brf=False)
  return template('./view/bsfiles/view/proc_approval.tpl',
                  custom_hdr='./view/bsfiles/view/dashboard_cus_file.tpl',
                  user=act_user, privs=privs,
                  results=results, startdate=request.forms.get('startdate'),
                  enddate=request.forms.get('enddate'), ReadFlag=request.forms.get('ReadFlag'),
                  smLimitWeightPercent=request.forms.get('smLimitWeightPercent'),
                  VehicheCard=request.forms.get('VehicheCard'), smTotalWeight=request.forms.get('smTotalWeight'),
                  smWheelCount=request.forms.get('smWheelCount'),
                  SiteID=request.forms.get('SiteID'), sites=db_man.get_sites())

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

  today = datetime.strftime(datetime.now(), '%Y-%m-%d')
  return template('./view/bsfiles/view/proc_rec.tpl',
                  custom_hdr='./view/bsfiles/view/dashboard_cus_file.tpl',
                  user=act_user, startdate=today,
                  enddate=today, ReadFlag="2",
                  smLimitWeightPercent="",
                  VehicheCard="", smTotalWeight="",
                  smWheelCount="",
                  SiteID="", sites=db_man.get_sites(),
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

  inplate = request.forms.get('VehicheCard').decode('utf-8')
  fields = ('ReadFlag=%d', 'SiteID=%d', 'smWheelCount=%d',
            'smLimitWeightPercent>%d', 'smTotalWeight>%d')
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
  hourange = request.forms.get('timeInterval')
  if hourange and interval[0][:10] == interval[1][:10]:
    starthour, endhour = tuple(hourange.split('-'))
    interval = (interval[0][:10]+' '+starthour, interval[1][:10]+' '+endhour)
  results = db_man.fetch_cond_recs(cond, interval, inplate=inplate)
  #details = db_man.fetch_cond_recs(cond, interval, brf=False)
  return template('./view/bsfiles/view/proc_rec.tpl',
                  custom_hdr='./view/bsfiles/view/dashboard_cus_file.tpl',
                  user=act_user, privs=privs,
                  results=results, startdate=request.forms.get('startdate'),
                  enddate=request.forms.get('enddate'), ReadFlag=request.forms.get('ReadFlag'),
                  smLimitWeightPercent=request.forms.get('smLimitWeightPercent'),
                  VehicheCard=request.forms.get('VehicheCard'), smTotalWeight=request.forms.get('smTotalWeight'),
                  smWheelCount=request.forms.get('smWheelCount'),
                  SiteID=request.forms.get('SiteID'), sites=db_man.get_sites())

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

  today = datetime.strftime(datetime.now(), '%Y-%m-%d')
  return template('./view/bsfiles/view/reg_approval.tpl',
                  custom_hdr='./view/bsfiles/view/dashboard_cus_file.tpl',
                  user=act_user, startdate=today,
                  enddate=today, ReadFlag="3",
                  smLimitWeightPercent="",
                  VehicheCard="", smTotalWeight="",
                  smWheelCount="",
                  SiteID="", sites=db_man.get_sites(),
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

  inplate = request.forms.get('VehicheCard').decode('utf-8')
  fields = ('ReadFlag=%d', 'SiteID=%d', 'smWheelCount=%d',
            'smLimitWeightPercent>%d', 'smTotalWeight>%d')
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
  hourange = request.forms.get('timeInterval')
  if hourange and interval[0][:10] == interval[1][:10]:
    starthour, endhour = tuple(hourange.split('-'))
    interval = (interval[0][:10]+' '+starthour, interval[1][:10]+' '+endhour)
  results = db_man.fetch_cond_recs(cond, interval, inplate=inplate)
  #details = db_man.fetch_cond_recs(cond, interval, brf=False)
  return template('./view/bsfiles/view/reg_approval.tpl',
                  custom_hdr='./view/bsfiles/view/dashboard_cus_file.tpl',
                  user=act_user, privs=privs,
                  results=results, startdate=request.forms.get('startdate'),
                  enddate=request.forms.get('enddate'), ReadFlag=request.forms.get('ReadFlag'),
                  smLimitWeightPercent=request.forms.get('smLimitWeightPercent'),
                  VehicheCard=request.forms.get('VehicheCard'), smTotalWeight=request.forms.get('smTotalWeight'),
                  smWheelCount=request.forms.get('smWheelCount'),
                  SiteID=request.forms.get('SiteID'), sites=db_man.get_sites())

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

@route('/blacklist_query', method='POST')
def blquery():
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  try:
    privs = UserDb.get_privilege(UserDb.get(act_user).role)
  except:
    redirect('/login')

  plate = request.forms.get('plate').decode('utf8')
  allblack = db_man.get_blacklist()
  return template('./view/bsfiles/view/blacklist_query.tpl',
                  custom_hdr='./view/bsfiles/view/dashboard_cus_file.tpl',
                  user=act_user,
                  privs=privs, blist=[b for b in allblack if plate in b[1]])

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

@route('/blacklist_mng', method='POST')
def blmng():
  act_user = get_act_user()
  if act_user is None:
    redirect('/')
  try:
    privs = UserDb.get_privilege(UserDb.get(act_user).role)
  except:
    redirect('/login')

  plate = request.forms.get('plate').decode('utf8')
  allblack = db_man.get_blacklist()
  return template('./view/bsfiles/view/blacklist_mng.tpl',
                  custom_hdr='./view/bsfiles/view/dashboard_cus_file.tpl',
                  user=act_user,
                  privs=privs, blist=[b for b in allblack if plate in b[1]])

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
                  privs=privs, blist=[b for b in db_man.get_blacklist()
                                      if b[-1]!=UserDb.BlackList.APPROVED])

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

#### restful api ####
@route('/mquery/ow/<siteid>')
def mquery_by_siteid(siteid):
  return {'data': db_man.mquery_siteid(int(siteid)), 'isNew': db_man.recs_in_half_min(int(siteid))}

@route('/mquery/detail/<seq>')
def mquery_detail(seq):
  return {'data': db_man.mquery_detail(int(seq))}

@route('/mquery/history/<plate>')
def mquery_history(plate):
  return {'data': db_man.mquery_history(plate.decode('utf8'))}

@route('/mquery/isblack/<plate>')
def isblack(plate):
  res = 'no'
  if db_man.is_black(plate):
    res = 'yes'
  return {'data': res}

@route('/mquery/allsites')
def mallsites():
  return {'data': db_man.mquery_sites()}

@route('/extern_query')
def exquery():
  return template('./view/bsfiles/view/extern_query.tpl',
                  custom_hdr='./view/bsfiles/view/dashboard_cus_file.tpl',
                  user=None,
                  VehicheCard='',
                  results=None)

@route('/extern_query', method='POST')
def exquery():
  print 'extern post'
  plate = request.forms.get('VehicheCard')
  results = db_man.ext_query_all(plate)
  return template('./view/bsfiles/view/extern_query.tpl',
                  custom_hdr='./view/bsfiles/view/dashboard_cus_file.tpl',
                  user=None,
                  VehicheCard=plate,
                  results=results)

@route('/ext/details/<seq>')
def detail(seq):
  imgpath = db_man.fpth
  detail = db_man.query_detail_by_seq(int(seq))
  #images have to be retrieved from sever for external user
  db_man.retr_img_from_ftp(detail[-1][-2])
  db_man.retr_img_from_ftp(detail[-1][-3])
  panel = "panel-info"
  if detail[1][4] == '1': panel = 'panel-danger'
  isblack, history_recs = db_man.query_history_by_plate(detail[-1][3])
  print isblack, history_recs, imgpath
  return template('./view/bsfiles/view/rec_detail.tpl',
                   custom_hdr=None, panel_type=panel,
                  detail=detail, length=len(detail[0]),
                  isblack=isblack, history_recs=None,
                  imgpath='/static/')

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
  run(app, host='0.0.0.0', port=8080, server='cherrypy', debug=True)
  #run(app, host='0.0.0.0', port=8081)


if __name__ == '__main__':
  main()
  #test_ftp()
