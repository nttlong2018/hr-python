# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import logging
import threading
from qmongo import helpers
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()

def get_list_with_searchtext(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)
    where = args['data'].get('where', None)

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    ret = models.HCSSYS_ExcelTemplate().aggregate().project(
            function_id = 1,
            template_code = 1,
            template_name = 1,
            is_default = 1,
            view_name = 1
            )

    if where != None:
        ret.match("function_id == @func_id",func_id=where['function_id'])

    if(searchText != None):
        ret.match("contains(template_name, @name)",name=searchText)

    if(sort != None):
        ret.sort(sort)
        
    return ret.get_page(pageIndex, pageSize)

def get_datail_with_searchtext(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)
    where = args['data'].get('where', None)

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    ret = models.HCSSYS_ExcelTemplate().aggregate().project(
            function_id = 1,
            detail = 1
            )

    if where != None:
        ret.match("function_id == @func_id",func_id=where['function_id'])

    if(searchText != None):
        ret.match("contains(template_name, @name)",name=searchText)

    if(sort != None):
        ret.sort(sort)
        
    rs = ret.get_page(pageIndex, pageSize)

    if len(rs['items']) > 0:
        return {
                'total_items': rs['total_items'], 
                'items': rs['items'][0]['detail'], 
                'page_index': rs['page_index'], 
                'page_size': rs['page_size']
            }
    return rs

def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args)
            ret  =  models.HCSSYS_ExcelTemplate().insert(data)
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
            ret  =  models.HCSSYS_ExcelTemplate().update(data, "_id == {0}", _id = args['data']['_id'])
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
            ret  =  models.HCSSYS_ExcelTemplate().delete("_id in {0}",[ObjectId(x["_id"])for x in args['data']])
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def remove_detail(args):
    try:
        lock.acquire()
        ret = {}
        id = ""
        if args['data'] != None:
            filter_value=helpers.filter("detail.field_name == {0}", args['data']['detail'][0]['field_name']).get_filter()
            ret  =  models.HCSSYS_ExcelTemplate().update({
                    "$pull": filter_value
                },"_id == {0}",id)
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
        function_id              = (lambda x: x['function_id']   if x.has_key('function_id')   else None)(args['data']),
        template_code            = (lambda x: x['template_code'] if x.has_key('template_code') else None)(args['data']),
        template_name            = (lambda x: x['template_name'] if x.has_key('template_name') else None)(args['data']),
        is_default               = (lambda x: x['is_default']    if x.has_key('is_default')    else None)(args['data']),
        view_name                = (lambda x: x['view_name']     if x.has_key('view_name')     else None)(args['data']),
        detail = dict(
            field_name           = (lambda x: x['field_name']       if x.has_key('field_name')       else None)(args['data']),
            lookup_data          = (lambda x: x['lookup_data']      if x.has_key('lookup_data')      else None)(args['data']),
            lookup_key_field     = (lambda x: x['lookup_key_field'] if x.has_key('lookup_key_field') else None)(args['data']),
            lookup_result        = (lambda x: x['lookup_result']    if x.has_key('lookup_result')    else None)(args['data']),
            allow_null           = (lambda x: x['allow_null']       if x.has_key('allow_null')       else None)(args['data']),
            is_key               = (lambda x: x['is_key']           if x.has_key('is_key')           else None)(args['data']),
            language             = (lambda x: x['language']         if x.has_key('language')         else None)(args['data']),
            header_text          = (lambda x: x['header_text']      if x.has_key('header_text')      else None)(args['data']),
            is_visible           = (lambda x: x['is_visible']       if x.has_key('is_visible')       else None)(args['data']),
            ordinal              = (lambda x: x['ordinal']          if x.has_key('ordinal')          else None)(args['data'])
            )
        )
    return ret_dict

def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['function_id']
    del ret_dict['template_code']
    return ret_dict