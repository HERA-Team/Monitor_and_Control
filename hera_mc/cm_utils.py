# -*- mode: python; coding: utf-8 -*-
# Copyright 2016 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""Some low-level configuration management utility functions.

"""

from __future__ import print_function

from hera_mc import mc
import datetime, os.path, pytz

def _log(msg,**kwargs):
    fp = open(mc.cm_log_file,'a')
    dt = datetime.datetime.now()
    fp.write(str(dt) + '  ' + msg + '\n')
    for key,value in kwargs.items():
        if key=='args':
            fp.write('  --args  ')
            vargs = vars(value)
            for k,v in vargs.items():
                fp.write(str(k)+':  '+str(v)+';  ')
            fp.write('\n')
        elif key=='data_dict':
            fp.write('  --data  \n')
            for k,v in value.items():
                fp.write('    '+k+'  ')
                for d in v:
                    fp.write(str(d)+';  ')
                fp.write('\n')
        else:
            fp.write('  --other  ')
            fp.write(str(key)+':  '+str(value)+'\n')
    fp.close()

def _get_datetime(_date,_time):
    if _date.lower() == '<' or _time.lower() == '<':
        return datetime.datetime(2000,1,1,tzinfo=pytz.utc)
    if _date.lower() == '>' or _time.lower() == '>':
        return datetime.datetime(2025,12,31,tzinfo=pytz.utc)
    if _date.lower() == 'n/a' or _time.lower() == 'n/a':
        return None
    if _date.lower() == 'now':
        dt_d = datetime.datetime.utcnow()
    else:
        data = _date.split('/')
        dt_d = datetime.datetime(int(data[2])+2000,int(data[0]),int(data[1]),tzinfo=pytz.utc)
    if _time.lower() == 'now':
        dt_t = datetime.datetime.utcnow()
    elif _time == '0':
        dt_t = datetime.datetime(dt_d.year,dt_d.month,dt_d.day,0,0,0,tzinfo=pytz.utc)
    else:
        data = _time.split(':')
        dt_t = datetime.datetime(dt_d.year,dt_d.month,dt_d.day,int(data[0]),int(data[1]),0,tzinfo=pytz.utc)
    dt = datetime.datetime(dt_d.year,dt_d.month,dt_d.day,dt_t.hour,dt_t.minute,dt_t.second,tzinfo=pytz.utc)
    return dt

# def _pull_out_component(cmpt_list,i,nc='-'):
#     try:
#         c = cmpt_list[i]
#     except IndexError:
#         try:
#             c = cmpt_list[-1]
#         except IndexError:
#             c = nc
#     return c
    
def _get_stopdate(_stop_date):
    if type(_stop_date)==datetime:
        return _stop_date
    else:
        return datetime.datetime(2020,12,31,tzinfo=pytz.utc)

def _is_active(current, _start_date, _stop_date):
    _stop_date = _get_stopdate(_stop_date)
    if current > _start_date and current < _stop_date:
        is_active=True
    else:
        is_active=False
    return is_active

def _query_default(a,args):
    vargs = vars(args)
    default = vargs[a]
    s = '%s [%s]:  ' % (a,str(default))
    v = raw_input(s).strip()
    if len(v) == 0:
        v = default
    return v

def _query_yn(s,default='y'):
    if default:
        s+=' ['+default+']'
    s+=':  '
    ans = raw_input(s)
    if len(ans)==0 and default:
        ans = default
    elif len(ans)>0:
        ans = ans.lower()
    else:
        print('No answer provided.')
        ans = _query_yn(s,default)
    if ans[0]=='y':
        return True
    else:
        return False
