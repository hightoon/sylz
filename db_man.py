#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, os.path, shutil
import pymssql, decimal
import UserDb
from datetime import datetime, date, timedelta
from ftplib import FTP

from PIL import Image

"""
    odbc db manipulation
"""

host = ''
inst = ''
user = ''
pswd = ''
dbnm = ''
ftpp = ''
fpth = ''

tabname2sqlcmd = {
    'LimitW': 0,
    'smArea': 1,
    'smHighWayDate': 2,
    'smSites': 3,
    'blacklist': 4
}

status = {
    None: '未处理',
    1: '已申请处理',
    2: '处理申请已审核',
    3: '处理已登记',
    4: '处理登记已审核'
}

init_db_cmds = [
    """ if exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[LimitW]') and
        OBJECTPROPERTY(id, N'IsUserTable') = 1)
        drop table [dbo].[LimitW]""",
    """ if exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[smArea]') and
        OBJECTPROPERTY(id, N'IsUserTable') = 1)
        drop table [dbo].[smArea]""",
    """ if exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[smHighWayDate]') and
        OBJECTPROPERTY(id, N'IsUserTable') = 1)
        drop table [dbo].[smHighWayDate]
    """,
    """ if exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[smSites]') and
        OBJECTPROPERTY(id, N'IsUserTable') = 1)
        drop table [dbo].[smSites]
    """,
    """ if exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[blacklist]') and
        OBJECTPROPERTY(id, N'IsUserTable') = 1)
        drop table [dbo].[blacklist]
    """
]

setup_db_cmds = [
    """ if not exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[LimitW]'))
        CREATE TABLE [dbo].[LimitW] (
        [VehicheType] [int] NOT NULL ,
        [LimitWeight] [int] NOT NULL
        ) ON [PRIMARY]
    """,
    """ if not exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[smArea]'))
        CREATE TABLE [dbo].[smArea] (
        [ID] [int] IDENTITY (1, 1) NOT NULL ,
        [AreaID] [int] NULL ,
        [AreaName] [nvarchar] (50) COLLATE Chinese_PRC_CI_AS NULL ,
        [AreaInfo] [nvarchar] (50) COLLATE Chinese_PRC_CI_AS NULL ,
        [SiteID] [int] NULL
        ) ON [PRIMARY]
    """,
    """ if not exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[smHighWayDate]'))
        CREATE TABLE [dbo].[smHighWayDate] (
        [Xuhao] [bigint] IDENTITY (1, 1) NOT NULL ,
        [RecordID] [bigint] NOT NULL ,
        [SiteID] [int] NOT NULL ,
        [smDevCode] [varchar] (20) COLLATE Chinese_PRC_CI_AS NULL ,
        [smTime] [datetime] NULL ,
        [VehicheCard] [varchar] (30) COLLATE Chinese_PRC_CI_AS NULL ,
        [smVehicheStr] [varchar] (20) COLLATE Chinese_PRC_CI_AS NULL ,
        [smState] [varchar] (10) COLLATE Chinese_PRC_CI_AS NULL ,
        [smWheelCount] [tinyint] NULL ,
        [smSpeed] [decimal](9, 2) NULL ,
        [smTotleAxesSpace] [decimal](9, 2) NULL ,
        [smTotalWeight] [decimal](9, 2) NULL ,
        [smRoadNum] [tinyint] NULL ,
        [smLimitWeight] [decimal](9, 2) NULL ,
        [smLimitWeightPercent] [decimal](9, 1) NULL ,
        [smPlatePath] [varchar] (200) COLLATE Chinese_PRC_CI_AS NULL ,
        [smImgPath] [varchar] (200) COLLATE Chinese_PRC_CI_AS NULL ,
        [smLengh] [decimal](9, 2) NULL ,
        [smWidth] [decimal](9, 2) NULL ,
        [smHeight] [decimal](9, 2) NULL ,
        [smOverLengh] [decimal](9, 2) NULL ,
        [smOverWidth] [decimal](9, 2) NULL ,
        [smOverHeight] [decimal](9, 2) NULL ,
        [smUser] [varchar] (20) COLLATE Chinese_PRC_CI_AS NULL ,
        [ReadFlag] [tinyint] NULL ,
        [BAKE] [varchar] (200) COLLATE Chinese_PRC_CI_AS NULL
        ) ON [PRIMARY]
    """,
    """ if not exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[smSites]'))
        CREATE TABLE [dbo].[smSites] (
        [ID] [int] IDENTITY (1, 1) NOT NULL ,
        [SiteID] [int] NULL ,
        [SiteName] [varchar] (50) COLLATE Chinese_PRC_CI_AS NULL ,
        [SiteInfo] [varchar] (50) COLLATE Chinese_PRC_CI_AS NULL
        ) ON [PRIMARY]
    """,
    """ if not exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[blacklist]'))
        CREATE TABLE [dbo].[blacklist] (
        [SeqNum] [bigint] IDENTITY (1, 1) NOT NULL ,
        [Time] [datetime] NOT NULL ,
        [Plate] [varchar] (30) COLLATE Chinese_PRC_CI_AS NOT NULL,
        [State] [int] NOT NULL
        ) ON [PRIMARY]
    """
]

def create_dir(fp):
    dir = '/'.join(fp.split('/')[:-1])
    try:
        os.makedirs(dir)
    except:
        pass

def retr_img_from_ftp(filename):
    usr, passwd = user, pswd
    ret = True
    create_dir(filename)
    localfn = filename
    with open(localfn, 'wb') as lf:
        try:
            ftp = FTP(host, timeout=0.1)
            ftp.login(usr, passwd)
        except Exception as e:
            print e
            ret = False
        else:
            try:
              ftp.retrbinary('RETR ' + filename, lf.write)
            except Exception as e:
              print 'get pic failed ', e
              ret = False
            finally:
              ftp.quit()
    if not ret:
        os.remove(localfn)
    return ret

def get_param():
    global host, inst, user, pswd, dbnm, ftpp, fpth
    with open('conf.txt', 'rb') as conf:
        for ln in conf:
            param = ln.split()
            if   param[0] == 'host': host = param[1]
            elif param[0] == 'inst': inst = param[1]
            elif param[0] == 'user': user = param[1]
            elif param[0] == 'pass': pswd = param[1]
            elif param[0] == 'dbnm': dbnm = param[1]
            elif param[0] == 'ftpp': ftpp = param[1]
            elif param[0] == 'fpth': fpth = param[1]
            else: pass

def exec_sql_file(cur, f):
    sqlstr = ''
    with open(f, 'r') as fd:
        for line in fd:
            if len(line) < 5:
                print sqlstr
                cur.execute(sqlstr)
                sqlstr = ''
            elif 'PRINT' in line:
                print line.split("'")[1]
            else:
                sqlstr += line


def connectdb():
    conn = pymssql.connect('%s'%(host,), '%s'%(user,), pswd, dbnm, charset='utf8')
    #conn = pymssql.connect('192.168.0.6\SQLEXPRESS', '.\\haitong', '111111', 'ssss', charset='utf8')
    #conn = pymssql.connect('10.140.163.132\SQLEXPRESS', '.\\quentin', '111111', 'ssss', charset='utf8')
    conn.autocommit(True)
    return conn

def drop_existing_tables():
    conn = connectdb()
    cur = conn.cursor()
    for s in init_db_cmds:
        cur.execute(s)
    conn.close()

def drop_table(tn):
    conn = connectdb()
    cur = conn.cursor()
    cur.execute(init_db_cmds[tabname2sqlcmd[tn]])
    conn.close()

def create_tables():
    #drop_table('blacklist')
    conn = connectdb()
    cur = conn.cursor()
    for s in setup_db_cmds:
        cur.execute(s)
    # alter table already exists
    try: cur.execute('ALTER TABLE [dbo].[smHighWayDate] ADD ProcTime [datetime] NULL')
    except Exception as e: print e
    conn.close()

def fetch_all_veh_recs():
    conn = connectdb()
    cur = conn.cursor(as_dict=True)
    cur.execute('SELECT * FROM smHighWayDate')
    results = [UserDb.Record.TAB_HDR]
    rows = cur.fetchall()
    if rows:
        for row in rows:
            results.append((row['Xuhao'], row['RecordID'], row['SiteID'], row['smTime'], row['VehicheCard'],
                            row['smState'], row['smWheelCount'], row['smSpeed'], row['smTotalWeight'],
                            row['smRoadNum'], row['smLimitWeight'], row['smLimitWeightPercent'], row['ProcTime'],
                            row['smPlatePath'], row['smImgPath']))
    conn.close()
    return results

def fetch_all_veh_recs_brf():
    conn = connectdb()
    cur = conn.cursor(as_dict=True)
    cur.execute('SELECT * FROM smHighWayDate')
    results = [UserDb.Record.TAB_BRF_HDR]
    rows = cur.fetchall()
    if rows:
        for row in rows:
            results.append((row['Xuhao'], row['RecordID'], row['smTime'], row['VehicheCard']))
    conn.close()
    return results

def fetch_all_bad():
    conn = connectdb()
    cur = conn.cursor(as_dict=True)
    cur.execute('SELECT * FROM smHighWayDate WHERE smState=%s', u'超限')
    results = [UserDb.Record.TAB_HDR]
    rows = cur.fetchall()
    if rows:
        for row in rows:
            results.append((row['Xuhao'], row['RecordID'], row['SiteID'], row['smTime'], row['VehicheCard'],
                            row['smState'], row['smWheelCount'], row['smSpeed'], row['smTotalWeight'],
                            row['smRoadNum'], row['smLimitWeight'], row['smLimitWeightPercent'], row['ProcTime'],
                            row['smPlatePath'], row['smImgPath'], row['ReadFlag']))
    conn.close()
    return results

def fetch_all_bad_brf(n):
    conn = connectdb()
    cur = conn.cursor(as_dict=True)
    cur.execute('SELECT TOP 30 * FROM smHighWayDate WHERE smState=%s ORDER BY Xuhao DESC', '1')
    results = [UserDb.Record.TAB_BRF_HDR]
    rows = cur.fetchall()
    if rows:
        for row in rows:
            results.append((row['Xuhao'], get_site_name(row['SiteID']),
                            datetime.strftime(row['smTime'], '%Y-%m-%d %H:%M:%S'),
                            row['VehicheCard'], row['smTotalWeight']/1000,
                            row['smLimitWeightPercent'], status[row['ReadFlag']],))
    conn.close()
    return results

def fetch_all_good():
    conn = connectdb()
    cur = conn.cursor(as_dict=True)
    cur.execute('SELECT * FROM smHighWayDate WHERE smState=%s', u'正常')
    results = [UserDb.Record.TAB_HDR]
    rows = cur.fetchall()
    if rows:
        for row in rows:
            results.append((row['Xuhao'], row['RecordID'], row['SiteID'], row['smTime'], row['VehicheCard'],
                            row['smState'], row['smWheelCount'], row['smSpeed'], row['smTotalWeight'],
                            row['smRoadNum'], row['smLimitWeight'], row['smLimitWeightPercent'],
                            row['smPlatePath'], row['smImgPath'], row['ReadFlag']))
    conn.close()
    return results

def fetch_all_good_brf():
    conn = connectdb()
    cur = conn.cursor(as_dict=True)
    cur.execute('SELECT * FROM smHighWayDate WHERE smState=%s', u'正常')
    results = [UserDb.Record.TAB_BRF_HDR]
    rows = cur.fetchall()
    if rows:
        for row in rows:
            results.append((row['Xuhao'], row['RecordID'], row['smTime'], row['VehicheCard']))
    conn.close()
    return results

def fetch_recs(ow='', proc='', brf=True):
    if ow == '':
        if brf:
            return fetch_all_veh_recs_brf()
        else:
            return fetch_all_veh_recs()
    elif ow == 'yes':
        if brf:
            return fetch_all_bad_brf()
        else:
            return fetch_all_bad()
    elif ow == 'no':
        if brf:
            return fetch_all_good_brf()
        else:
            return fetch_all_good()

def fetch_cond_recs(cond, interval, brf=True, inplate=''):
    conn = connectdb()
    cur = conn.cursor()

    cur.execute('SELECT SiteID, SiteName FROM smSites')
    sites = cur.fetchall()
    sites = dict(sites)

    cur = conn.cursor(as_dict=True)

    if interval:
        startt = interval[0]
        endt = interval[1]
    else:
        startt = datetime.strftime(datetime.now(), '%Y-%m-%d') + ' 00:00:00'
        endt = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

    order = ' ORDER BY smTime DESC'

    #if interval:
    timestr = " smTime between \'%s\' and \'%s\'"%(startt, endt)
    #else: timestr = ''
    if cond[0]:
        if timestr: timestr = ' and ' + timestr
        cur.execute('SELECT * FROM smHighWayDate WHERE ' + cond[0] + timestr + order, cond[1])
    else:
        if timestr: timestr = ' WHERE ' + timestr
        print timestr
        cur.execute('SELECT * FROM smHighWayDate' + timestr + order)
    rows = cur.fetchall()
    if rows:
        if brf:
            results = [UserDb.Record.TAB_BRF_HDR]
            for row in rows:
                sn = '站点-%d'%(row['SiteID'])
                if sites.has_key(row['SiteID']): sn = sites[row['SiteID']]
                if inplate in row['VehicheCard']:
                    results.append((row['Xuhao'], sn,
                                    datetime.strftime(row['smTime'], '%Y-%m-%d %H:%M:%S'),
                                    row['VehicheCard'], row['smWheelCount'],
                                    row['smTotalWeight']/1000,
                                    row['smLimitWeightPercent'],
                                    get_ow_tons(row['smTotalWeight'], row['smLimitWeight']),
                                    status[row['ReadFlag']],))
        else:
            print 'fetch cond details'
            results = [UserDb.Record.TAB_HDR]
            for row in rows:
                #if not os.path.isfile(row['smPlatePath'].replace(r'\\', '_')):
                #    retr_img_from_ftp(row['smPlatePath'].replace(r'\\', '/'))
                #if not os.path.isfile(row['smImgPath'].replace(r'\\', '_')):
                #    retr_img_from_ftp(row['smImgPath'].replace(r'\\', '/'))
                proctime = "记录暂未进行任何处理"
                if row['ProcTime']: proctime = row['ProcTime']
                results.append(
                               ((row['Xuhao'], get_site_name(row['SiteID']),
                                 datetime.strftime(row['smTime'], '%Y-%m-%d %H:%M:%S'),
                                 row['VehicheCard'], row['smTotalWeight']/1000,
                                 row['smLimitWeightPercent'], status[row['ReadFlag']],),
                                (row['Xuhao'], get_site_name(row['SiteID']), datetime.strftime(row['smTime'], '%Y-%m-%d %H:%M:%S'),
                                 row['VehicheCard'],
                                 row['smState'], row['smWheelCount'], row['smSpeed'], row['smTotalWeight']/1000,
                                 row['smRoadNum'], row['smLimitWeight']/1000, row['smLimitWeightPercent'], proctime,
                                 row['smPlatePath'].replace(r'\\', '/'), row['smImgPath'].replace(r'\\', '/'),
                                 row['ReadFlag'])
                              )
                            )
    else:
        results = None

    return results

def ext_query_all(plate):
    conn = connectdb()
    cur = conn.cursor(as_dict=True)

    cur.execute('SELECT Xuhao, RecordID, SiteID, VehicheCard, \
                 smTotalWeight, smLimitWeight, smLimitWeightPercent,\
                 ReadFlag, ProcTime FROM smHighWayDate WHERE smState=%s', '1')
    rows = cur.fetchall()
    results = [('记录编号', '站点', '车牌号', '车重', '超重', '超限率', '处理状态', '处理时间')]
    for row in rows:
        if plate.decode('utf8') in row['VehicheCard'] and (row['ReadFlag']==2 or row['ReadFlag']==4):
            results.append((row['Xuhao'], row['RecordID'], get_site_name(row['SiteID']),
                           row['VehicheCard'], row['smTotalWeight'], row['smLimitWeight'],
                           row['smLimitWeightPercent'], status[row['ReadFlag']],
                           row['ProcTime']))
    conn.close()
    return results

def recs_in_half_min(siteid):
    conn = connectdb()
    cur = conn.cursor()

    startt = datetime.strftime(datetime.now() - timedelta(seconds=30), '%Y-%m-%d %H:%M:%S')
    endt = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    pstr = " AND smTime between \'%s\' and \'%s\'"%(startt, endt)

    cur.execute('SELECT Xuhao FROM smHighWayDate WHERE SiteID=%d AND smState=%s'+pstr, (siteid, '1',))
    recs = cur.fetchall()
    conn.close()
    if recs: return 1
    else: return 0

def mquery_siteid(siteid):
    conn = connectdb()
    cur = conn.cursor()

    startt = datetime.strftime(datetime.now() - timedelta(hours=1), '%Y-%m-%d %H:%M:%S')
    endt = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    pstr = " AND smTime between \'%s\' and \'%s\'"%(startt, endt)
    order = ' ORDER BY smTime DESC'

    cur.execute('SELECT Xuhao, RecordID, smTime, SiteID, VehicheCard, smTotalWeight, \
        smLimitWeight, smLimitWeightPercent, smPlatePath, smImgPath FROM smHighWayDate WHERE SiteID=%d'+pstr+order,
        siteid)
    results = []
    keys = ('Xuhao', 'RecordID', 'smTime', 'SiteID', 'VehicheCard', 'smTotalWeight', 'smLimitWeight',
            'smLimitWeightPercent', 'smPlatePath', 'smImgPath')
    rows = cur.fetchall()
    for row in rows:
        tmp = {}
        for i in range(len(keys)):
            if keys[i] == 'smTime':
                tmp[keys[i]] = datetime.strftime(row[i], '%Y-%m-%d %H:%M:%S')
            elif type(row[i]) == decimal.Decimal:
                tmp[keys[i]] = str(row[i])
            else:
                try:
                    tmp[keys[i]] = str(row[i].decode('utf8'))
                except:
                    tmp[keys[i]] = row[i]
        results.append(tmp)
    conn.close()
    return results

def mquery_detail(seq):
    conn = connectdb()
    cur = conn.cursor(as_dict=True)

    cur.execute('SELECT Xuhao, SiteID, smTime, VehicheCard, smState, smWheelCount, \
                 smSpeed, smTotalWeight, smRoadNum, smLimitWeight, smLimitWeightPercent,\
                 smPlatePath, smImgPath, ReadFlag FROM smHighWayDate WHERE Xuhao=%d', seq)
    rows = cur.fetchall()
    results = []
    for row in rows:
        for k in row.keys():
            if k == 'smTime':
                row[k] = datetime.strftime(row[k], '%Y-%m-%d %H:%M:%S')
            elif k == 'smPlatePath' or k == 'smImgPath':
                row[k] = row[k].replace(r'\\', '/')
                retr_img_from_ftp(row[k])
                fn, ext = os.path.splitext(row[k])
                copy4mob = fn + '_sm' + ext
                if not os.path.isfile(copy4mob):
                    im = Image.open(row[k])
                    im.resize((80, 60), Image.ANTIALIAS)
                    im.save(copy4mob)
                row[k] = copy4mob
            elif type(row[k]) == decimal.Decimal:
                row[k] = str(row[k])
            else:
                try: row[k] = str(row[k].decode('utf8'))
                except: pass
        results.append(row)
    conn.close()
    return results

def mquery_history(plate):
    startt = datetime.strftime(datetime.now() - timedelta(days=90), '%Y-%m-%d %H:%M:%S')
    endt = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    pstr = " AND smTime between \'%s\' and \'%s\'"%(startt, endt)
    order = ' ORDER BY smTime DESC'

    conn = connectdb()
    cur = conn.cursor(as_dict=True)

    cur.execute("SELECT Xuhao, SiteID, smTime, VehicheCard, smState, smWheelCount, \
                 smSpeed, smTotalWeight, smRoadNum, smLimitWeight, smLimitWeightPercent,\
                 smPlatePath, smImgPath, ReadFlag FROM smHighWayDate \
                 WHERE VehicheCard LIKE '%%%s%%'"%plate.encode('utf8') + pstr + order)
    rows = cur.fetchall()
    results = []
    for row in rows:
        for k in row.keys():
            if k == 'smTime':
                row[k] = datetime.strftime(row[k], '%Y-%m-%d %H:%M:%S')
            elif type(row[k]) == decimal.Decimal:
                row[k] = str(row[k])
            else:
                try: row[k] = str(row[k].decode('utf8'))
                except: pass
        results.append(row)
    conn.close()
    return results

def query_detail_by_seq(seq):
    conn = connectdb()
    cur = conn.cursor(as_dict=True)
    cur.execute('SELECT * FROM smHighWayDate WHERE Xuhao=%d', seq)
    result = [UserDb.Record.TAB_HDR]
    row = cur.fetchone()
    conn.close()
    if not row: return result
    local_plate_img = row['smPlatePath'].replace(r'\\', '_')
    remote_plate_img = row['smPlatePath'].replace(r'\\', '/')
    local_rear_img = row['smImgPath'].replace(r'\\', '_')
    remote_rear_img = row['smImgPath'].replace(r'\\', '/')
    #if not os.path.isfile(local_plate_img):
    #    retr_img_from_ftp(remote_plate_img)
    #if not os.path.isfile(local_rear_img):
    #    retr_img_from_ftp(remote_rear_img)
    proctime = "记录暂未进行任何处理"
    if row['ProcTime']: proctime = row['ProcTime']
    sitename = get_site_name(row['SiteID'])
    timestr = datetime.strftime(row['smTime'], '%Y-%m-%d %H:%M:%S')
    result.append(
        (row['Xuhao'], sitename, timestr,
         row['VehicheCard'],
         row['smState'], row['smWheelCount'], row['smSpeed'], row['smTotalWeight']/1000,
         row['smRoadNum'], row['smLimitWeight']/1000, row['smLimitWeightPercent'], proctime,
         remote_plate_img, remote_rear_img,
         row['ReadFlag'])
        )
    return result

def query_history_by_plate(plate):
    "get record belongs to plate in the past 90 days"
    tab_hdr = ('纪录编号', '站点', '时间', '车牌', '超重', '超限率',)
    if plate == u"无车牌": return False, [tab_hdr]
    conn = connectdb()
    cur = conn.cursor(as_dict=True)
    startt = datetime.strftime(date.today() - timedelta(days=90), '%Y-%m-%d') + ' 00:00:00'
    endt = datetime.strftime(date.today(), '%Y-%m-%d') + ' 23:59:59'
    pstr = " AND smTime between \'%s\' and \'%s\'"%(startt, endt)
    order = ' ORDER BY smTime DESC'
    cur.execute('SELECT * FROM smHighWayDate WHERE VehicheCard=%s'+pstr+order, plate)
    result = [tab_hdr]
    rows = cur.fetchall()
    cur.execute('SELECT * FROM blacklist WHERE Plate=%s', plate)
    black = cur.fetchone()
    conn.close()
    for row in rows:
        local_plate_img = row['smPlatePath'].replace(r'\\', '_')
        remote_plate_img = row['smPlatePath'].replace(r'\\', '/')
        local_rear_img = row['smImgPath'].replace(r'\\', '_')
        remote_rear_img = row['smImgPath'].replace(r'\\', '/')
        #if not os.path.isfile(local_plate_img):
        #    retr_img_from_ftp(remote_plate_img)
        #if not os.path.isfile(local_rear_img):
        #    retr_img_from_ftp(remote_rear_img)
        sitename = get_site_name(row['SiteID'])
        timestr = datetime.strftime(row['smTime'], '%Y-%m-%d %H:%M:%S')
        result.append(
            (row['RecordID'], sitename, timestr,
             row['VehicheCard'],
             row['smState'], row['smLimitWeightPercent'],
             row['Xuhao'],
             remote_plate_img, remote_rear_img,
             row['ReadFlag'])
            )
    return (black is not None, result)

def period_stat(p, percent=False, siteid=None):
    conn = connectdb()
    cur = conn.cursor()
    cur.execute('SELECT SiteID, SiteName FROM smSites')
    sites = cur.fetchall()
    sites = dict(sites)
    cur.close()
    cur = conn.cursor(as_dict=True)
    #startt = datetime.strftime(datetime.now(), '%Y-%m-%d') + ' 00:00:00'
    #endt = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    where_str = ''
    where_val = []
    if siteid:
        where_str += ' AND SiteID=%d'
        where_val.append(siteid)

    startt, endt = p
    timestr = " smTime between \'%s\' and \'%s\'"%(startt, endt)
    cur.execute('SELECT * FROM smHighWayDate WHERE ' + timestr + where_str + ' AND smState=%s', tuple(where_val+['1']))
    rows = cur.fetchall()

    # 24 hours results
    results = []
    for i in xrange(24): results.append({})
    for row in rows:
        try: sn = sites[row['SiteID']]
        except: sn = '站点%d'%(row['SiteID'])
        hour = row['smTime'].hour
        if results[hour].has_key(sn): results[hour][sn] += 1
        else: results[hour][sn] = 1
        for res in results:
            if not res.has_key(sn): res[sn] = 0

    percent_results = {}
    if percent:
        percent_ranges = ['smLimitWeightPercent=0', 'smLimitWeightPercent>0 and smLimitWeightPercent<20',
                          'smLimitWeightPercent>=20 and smLimitWeightPercent<50',
                          'smLimitWeightPercent>=50 and smLimitWeightPercent<100',
                          'smLimitWeightPercent>=100']
        numofrange = len(percent_ranges)
        for pr in range(numofrange):
            cur.execute('SELECT * FROM smHighWayDate WHERE ' + timestr + ' AND ' + percent_ranges[pr] + where_str, tuple(where_val))
            recs = cur.fetchall()
            for rec in recs:
                try: sn = sites[rec['SiteID']]
                except: sn = '站点%d'%(rec['SiteID'])
                if percent_results.has_key(sn): percent_results[sn][pr] += 1
                else:
                    percent_results[sn] = [0]*numofrange
                    percent_results[sn][pr] += 1

    conn.close()
    if percent: return results, percent_results
    return results

def get_site_name(siteid):
    conn = connectdb()
    cur = conn.cursor(as_dict=True)
    cur.execute('SELECT SiteID, SiteName FROM smSites WHERE SiteID=%d', siteid)
    sn = cur.fetchone()
    conn.close()
    if sn is None: return '站点-%d'%(siteid)
    return sn['SiteName']

def get_sites():
    conn = connectdb()
    cur = conn.cursor()
    cur.execute('SELECT SiteID, SiteName FROM smSites')
    sites = cur.fetchall()
    conn.close()
    return sites

def mquery_sites():
    conn = connectdb()
    cur = conn.cursor(as_dict=True)
    cur.execute('SELECT SiteID, SiteName FROM smSites')
    sites = cur.fetchall()
    conn.close()
    return sites

def get_site_name_cache(siteid, sites):
    for site in sites:
        if siteid == site['SiteName']:
            return site['SiteID']
    return '站点-%d'%(siteid,)

def get_site_ids():
    conn = connectdb()
    cur = conn.cursor()
    cur.execute("SELECT SiteID FROM smSites")
    rows = cur.fetchall()
    if not rows:
        cur.execute("SELECT SiteID FROM smHighWayDate")
        rows = cur.fetchall()
    conn.close()
    return list(set([row[0] for row in rows]))

def get_ow_tons(total, limit):
    "input in km and output in ton"
    diff = total - limit
    if diff < 0: diff = 0
    return diff / 1000

def update_read_flag(seq, value):
    conn = connectdb()
    cur = conn.cursor()
    cur.execute('UPDATE smHighWayDate SET ReadFlag=%d, ProcTime=CAST(%s AS DATETIME) WHERE Xuhao=%d',
                (value, datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S'), seq))
    conn.close()

def update_regtime(seq, ts):
    conn = connectdb()
    cur = conn.cursor()
    cur.execute('UPDATE smHighWayDate SET ProcTime=CAST(%s AS DATETIME) WHERE Xuhao=%d', (ts, seq))
    conn.close()

def get_blacklist():
    conn = connectdb()
    cur = conn.cursor(as_dict=True)
    cur.execute('SELECT * FROM blacklist')
    res = []
    rows = cur.fetchall()
    if rows:
        for row in rows:
            res.append((row['SeqNum'], row['Plate'], row['Time'], row['State']))
    conn.close()
    return res

def is_black(plate):
    conn = connectdb()
    cur = conn.cursor()
    cur.execute('SELECT Plate from blacklist')
    rows = cur.fetchall()
    black = [row[0] for row in rows]
    return (plate.decode('utf8') in black)

def update_blacklist_state(seq, state):
    conn = connectdb()
    cur = conn.cursor()
    cur.execute('UPDATE blacklist SET State=%d WHERE SeqNum=%d', (state, seq))
    conn.close()

def get_blacklist_state(seq):
    conn = connectdb()
    cur = conn.cursor(as_dict=True)
    cur.execute('SELECT * FROM blacklist WHERE SeqNum=%d', seq)
    row = cur.fetchone()
    conn.close()
    return row['State']

def approve_blacklist(seq):
    update_blacklist_state(seq, UserDb.BlackList.APPROVED)

def add_blacklist(plate):
    conn = connectdb()
    cur = conn.cursor()
    cur.execute('INSERT blacklist VALUES (CAST (%s AS DATETIME), %s, %d)',
        (datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'), plate, UserDb.BlackList.REQUESTING))
    conn.close()

def del_blacklist(seq):
    conn = connectdb()
    cur = conn.cursor()
    try: cur.execute('DELETE FROM blacklist WHERE SeqNum=%d', seq)
    except Exception as e: print e
    conn.close()

def cancel_blacklist_state(seq):
    conn = connectdb()
    cur = conn.cursor()
    state = get_blacklist_state(seq)
    if state == UserDb.BlackList.REQUESTING:
        del_blacklist(seq)
    elif state == UserDb.BlackList.DELETING:
        update_blacklist_state(seq, UserDb.BlackList.APPROVED)

def confirm_blacklist_state(seq):
    conn = connectdb()
    cur = conn.cursor()
    state = get_blacklist_state(seq)
    if state == UserDb.BlackList.REQUESTING:
        update_blacklist_state(seq, UserDb.BlackList.APPROVED)
    elif state == UserDb.BlackList.DELETING:
        del_blacklist(seq)


def test_main():
    conn = connectdb()
    cur = conn.cursor(as_dict=True)
    #exec_sql_file(cur, r'../sifang/sifang.sql')
    cur.execute('SELECT * FROM smHighWayDate WHERE VehicheCard LIKE \'%%\'')
    #cur.execute('SELECT * FROM smHighWayDate')
    for r in cur.fetchall():
        if '无'.decode('utf-8') in r['VehicheCard']:
            print r['VehicheCard']
    #cur.execute('ALTER TABLE [dbo].[smHighWayDate] ADD ProcTime [datetime] NULL')
    #cur.execute('INSERT blacklist VALUES (%s, %s)', ('2015-08-30 13:23:08', u'浙A124FA'))
    cur.close()
    conn.close()

if __name__ == '__main__':
    get_param()
    test_main()
