# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import common
import datetime
from Query import TMLS_Rank
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
    ret=TMLS_Rank.display_list_rank()

    if(searchText != None):
        ret.match("contains(rank_code, @name) or contains(rank_name, @name)" + \
            "contains(rank_content, @name) or contains(total_from, @name)" + \
            "contains(total_to, @name) or contains(ordinal, @name)" ,name=searchText)

    if(sort != None):
        ret.sort(sort)
        
    return ret.get_page(pageIndex, pageSize)

def get_list_details_with_searchtext(args):

    if args['data'].has_key('rank_code'):
        rank_code = args['data']['rank_code']
        searchText = args['data'].get('search', '')
        pageSize = args['data'].get('pageSize', 0)
        pageIndex = args['data'].get('pageIndex', 20)
        sort = args['data'].get('sort', 20)

        pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
        pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
        ret=TMLS_Rank.get_details(rank_code)
    
        #if(searchText != None):
        #    ret.match("contains(rank_code, @name)",name=searchText)

        if(sort != None):
            ret.sort(sort)

        return ret.get_page(pageIndex, pageSize)

    else:
        return dict(
            error = "rank_code is not exist"
        )

def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args)
            ret  =  models.TMLS_Rank().insert(data)
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
            ret  =  models.TMLS_Rank().update(
                data, 
                "_id == {0}", 
                ObjectId(args['data']['_id']))
            if ret['data'].raw_result['updatedExisting'] == True:
                ret.update(
                    item = TMLS_Rank.display_list_acadame().match("_id == {0}", ObjectId(args['data']['_id'])).get_item()
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
            ret  =  models.TMLS_Rank().delete("_id in {0}",[ObjectId(x["_id"])for x in args['data']])
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def insert_details(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            if not args['data']['details'].has_key('rec_id'):
                if args['data'].has_key('rank_code'):
                    details = set_dict_detail_insert_data(args['data']['details'])
                    ret = TMLS_Rank.insert_details(args, details)
                else:
                    lock.release()
                    return dict(
                        error = "request parameter rank_code is not exist"
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

def delete_detail(args):
    try:
        lock.acquire()
        ret = {}
        error_message = None
        if args['data'] != None:
            if args['data'].has_key('rank_code'):
                if args['data'].has_key('rec_id'):
                    ret = TMLS_Rank.remove_details(args)
                    lock.release()
                    return ret
                else:
                    error_message = "parameter 'rec_id' is not exist"
            else:
                error_message = "parameter 'rank_code' is not exist"

            lock.release()
            return dict(
                error = error_message
            )
        else:
            error_message = "request parameter is not exist"

        lock.release()
        return dict(
            error = error_message
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def set_dict_insert_data(args):
    ret_dict = dict()

    ret_dict.update(
        rank_code         = (lambda x: x['rank_code']         if x.has_key('rank_code')        else None)(args['data']),
        rank_name         = (lambda x: x['rank_name']         if x.has_key('rank_name')        else None)(args['data']),
        rank_content      = (lambda x: x['rank_content']      if x.has_key('rank_content')     else None)(args['data']),
        total_from        = (lambda x: x['total_from']        if x.has_key('total_from')       else None)(args['data']),
        total_to          = (lambda x: x['total_to']          if x.has_key('total_to')         else None)(args['data']),
        is_change_object  = (lambda x: x['is_change_object']  if x.has_key('is_change_object') else None)(args['data']),
        lock              = (lambda x: x['lock']              if x.has_key('lock')             else None)(args['data']),
        details           = (lambda x: x['details']           if x.has_key('details')          else [])(args['data'])
    )

    return ret_dict

def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['rank_code']

    return ret_dict

def set_dict_detail_insert_data(args):
    ret_dict = dict()
    ret_dict.update(
            rec_id            = common.generate_guid(),
            rank_code         = (lambda x: x['rank_code']      if x.has_key('rank_code')        else None)(args),
            change_object     = (lambda x: x['change_object']  if x.has_key('change_object')    else None)(args),
            object_level      = (lambda x: x['object_level']   if x.has_key('object_level')     else None)(args),
            object_code       = (lambda x: x['object_code']    if x.has_key('object_code')      else None)(args),
            object_name       = (lambda x: x['object_name']    if x.has_key('object_name')      else None)(args),
            priority_no       = (lambda x: x['priority_no']    if x.has_key('priority_no')      else None)(args),
            total_from        = (lambda x: x['total_from']     if x.has_key('total_from')       else None)(args),
            total_to          = (lambda x: x['total_to']       if x.has_key('total_to')         else None)(args),
            created_on        = datetime.datetime.now(),
            created_by        = common.get_user_id(),
            modified_on       = None,
            modified_by       = None
            )
    return ret_dict