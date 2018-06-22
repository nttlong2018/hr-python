# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import datetime
import logging
import threading
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()

def get_list(args):
    items = models.HCSSYS_Departments().aggregate().project(
        department_code = 1,
        department_name = 1,
        parent_code     = 1
        )
    
    return items.get_list()

def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            if not args['data'].has_key('department_code') or not args['data'].has_key('department_name'):
                field_list = []
                if not args['data'].has_key('department_code'):
                    field_list.append("department_code")
                if not args['data'].has_key('department_name'):
                    field_list.append("department_name")
                lock.release()
                return {
                    "error":{
                        "fields":field_list,
                        "code":"missing"
                        }
                }
                
            data =  set_dict_data(args)
            ret  =  models.HCSSYS_Departments().insert(data)
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
            data = set_dict_data(args)
            ret  =  models.HCSSYS_Departments().update(data, "_id == @id", id = ObjectId(args['data']['_id']))
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
            ret =  models.HCSSYS_Departments().delete("_id in {0}", [ObjectId(x["_id"])for x in args['data']])
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def set_dict_data(args):
    data = dict(
        department_code     =     args['data']['department_code'],
        department_name     =     args['data']['department_name'],
        department_name2    =     (lambda x: x['department_name2'] if x.has_key('department_name2') else None)(args['data']),
        department_alias    =     (lambda x: x['department_alias'] if x.has_key('department_alias') else None)(args['data']),
        parent_code         =     (lambda x: x['parent_code'] if x.has_key('parent_code') else None)(args['data']),
        level               =     (lambda x: x['level'] if x.has_key('level') else None)(args['data']),
        level_code          =     (lambda x: x['level_code'] if x.has_key('level_code') else None)(args['data']),
        department_tel      =     (lambda x: x['department_tel'] if x.has_key('department_tel') else None)(args['data']),
        department_fax      =     (lambda x: x['department_fax'] if x.has_key('department_fax') else None)(args['data']),
        department_email    =     (lambda x: x['department_email'] if x.has_key('department_email') else None)(args['data']),
        department_address  =     (lambda x: x['department_address'] if x.has_key('department_address') else None)(args['data']),
        nation_code         =     (lambda x: x['nation_code'] if x.has_key('nation_code') else None)(args['data']),
        province_code       =     (lambda x: x['province_code'] if x.has_key('province_code') else None)(args['data']),
        district_code       =     (lambda x: x['district_code'] if x.has_key('district_code') else None)(args['data']),
        is_company          =     (lambda x: x['is_company'] if x.has_key('is_company') else None)(args['data']),
        is_fund             =     (lambda x: x['is_fund'] if x.has_key('is_fund') else None)(args['data']),
        is_fund_bonus       =     (lambda x: x['is_fund_bonus'] if x.has_key('is_fund_bonus') else None)(args['data']),
        decision_no         =     (lambda x: x['decision_no'] if x.has_key('decision_no') else None)(args['data']),
        decision_date       =     (lambda x: x['decision_date'] if x.has_key('decision_date') else None)(args['data']),
        effect_date         =     (lambda x: x['effect_date'] if x.has_key('effect_date') else None)(args['data']),
        license_no          =     (lambda x: x['license_no'] if x.has_key('license_no') else None)(args['data']),
        tax_code            =     (lambda x: x['tax_code'] if x.has_key('tax_code') else None)(args['data']),
        lock_date           =     (lambda x: x['lock_date'] if x.has_key('lock_date') else None)(args['data']),
        logo_image          =     (lambda x: x['logo_image'] if x.has_key('logo_image') else None)(args['data']),
        manager_code        =     (lambda x: x['manager_code'] if x.has_key('manager_code') else None)(args['data']),
        secretary_code      =     (lambda x: x['secretary_code'] if x.has_key('secretary_code') else None)(args['data']),
        ordinal             =     (lambda x: x['ordinal'] if x.has_key('ordinal') else None)(args['data']),
        lock                =     (lambda x: x['lock'] if x.has_key('lock') else None)(args['data']),
        note                =     (lambda x: x['note'] if x.has_key('note') else None)(args['data']),
        region_code         =     (lambda x: x['region_code'] if x.has_key('region_code') else None)(args['data']),
        domain_code         =     (lambda x: x['domain_code'] if x.has_key('domain_code') else None)(args['data']),
        signed_by           =     (lambda x: x['signed_by'] if x.has_key('signed_by') else None)(args['data'])
    )
    return data