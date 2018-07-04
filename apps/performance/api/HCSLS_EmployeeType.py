# -*- coding: utf-8 -*-
from bson import ObjectId
import models
from Query import EmployeeType
import logging
import threading
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()

def get_list_with_searchtext(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    ret=EmployeeType.display_list_employee_type()
    
    if(searchText != None):
        ret.match("contains(emp_type_name, @name)",name=searchText)

    if(sort != None):
        ret.sort(sort)
        
    return ret.get_page(pageIndex, pageSize)

def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args)
            ret  =  models.HCSLS_EmployeeType().insert(data)
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def update(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_update_data(args)
            ret  =  models.HCSLS_EmployeeType().update(
                data, 
                "_id == {0}", 
                ObjectId(args['data']['_id']))
            if ret['data'].raw_result['updatedExisting'] == True:
                ret.update(
                    item = EmployeeType.display_list_employee_type().match("_id == {0}", ObjectId(args['data']['_id'])).get_item()
                    )
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def delete(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            ret  =  models.HCSLS_EmployeeType().delete("_id in {0}",[ObjectId(x["_id"])for x in args['data']])
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def set_dict_insert_data(args):
    ret_dict = dict()

    ret_dict.update(
        emp_type_code      = (lambda x: x['emp_type_code']      if x.has_key('emp_type_code')       else None)(args['data']),
        emp_type_name      = (lambda x: x['emp_type_name']      if x.has_key('emp_type_name')       else None)(args['data']),
        emp_type_name2     = (lambda x: x['emp_type_name2']     if x.has_key('emp_type_name2')      else None)(args['data']),
        rate_main_sal      = (lambda x: x['rate_main_sal']      if x.has_key('rate_main_sal')       else None)(args['data']),
        rate_soft_sal      = (lambda x: x['rate_soft_sal']      if x.has_key('rate_soft_sal')       else None)(args['data']),
        true_type          = (lambda x: x['true_type']          if x.has_key('true_type')           else None)(args['data']),
        #probation_time_by  = (lambda x: x['probation_time_by']  if x.has_key('probation_time_by')   else None)(args['data']),
        #probation_time     = (lambda x: x['probation_time']     if x.has_key('probation_time')      else None)(args['data']),
        #is_fix             = (lambda x: x['is_fix']             if x.has_key('is_fix')              else None)(args['data']),
        #coeff              = (lambda x: x['coeff']              if x.has_key('coeff')               else None)(args['data']),
        #begin_date_cal     = (lambda x: x['begin_date_cal']     if x.has_key('begin_date_cal')      else None)(args['data']),
        ordinal            = (lambda x: x['ordinal']            if x.has_key('ordinal')             else None)(args['data']),
        note               = (lambda x: x['note']               if x.has_key('note')                else None)(args['data']),
        lock               = (lambda x: x['lock']               if x.has_key('lock')                else None)(args['data'])
        #department_code    = (lambda x: x['department_code']    if x.has_key('department_code')     else None)(args['data'])
    )

    return ret_dict

def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['emp_type_code']
    return ret_dict