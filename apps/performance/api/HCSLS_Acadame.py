# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import common
import datetime
from Query import Acadame
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
    ret=Acadame.display_list_acadame()
    
    if(searchText != None):
        ret.match("contains(train_mode_name, @name)",name=searchText)

    if(sort != None):
        ret.sort(sort)
        
    return ret.get_page(pageIndex, pageSize)

def get_list_details_with_searchtext(args):

    if args['data'].has_key('train_level_code'):
        train_level_code = args['data']['train_level_code']
        searchText = args['data'].get('search', '')
        pageSize = args['data'].get('pageSize', 0)
        pageIndex = args['data'].get('pageIndex', 20)
        sort = args['data'].get('sort', 20)

        pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
        pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
        ret=Acadame.display_list_acadame_detail(train_level_code)
    
        #if(searchText != None):
        #    ret.match("contains(train_level_name, @name)",name=searchText)

        if(sort != None):
            ret.sort(sort)

        return ret.get_page(pageIndex, pageSize)

    else:
        return dict(
            error = "train_level_code is not exist"
        )

def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            if args['data'].has_key('_id') or args['data'].has_key('train_level_code'):
                collection  =  common.get_collection('HCSLS_Acadame')
                check_exist = collection.find_one({"train_level_code":args['data']['train_level_code']})
                if check_exist == None:
                    data =  set_dict_insert_data(args)
                    ret  =  models.HCSLS_Acadame().insert(data)
                    lock.release()
                    return ret
                else:
                    update(args)
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
            ret  =  models.HCSLS_Acadame().update(
                data, 
                "_id == {0}", 
                ObjectId(args['data']['_id']))
            if ret['data'].raw_result['updatedExisting'] == True:
                ret.update(
                    item = Acadame.display_list_acadame().match("_id == {0}", ObjectId(args['data']['_id'])).get_item()
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
            ret  =  models.HCSLS_Acadame().delete("_id in {0}",[ObjectId(x["_id"])for x in args['data']])
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
                if args['data'].has_key('train_level_code'):
                    details = set_dict_detail_insert_data(args['data']['details'])
                    ret = Acadame.insert_details(args, details)
                else:
                    lock.release()
                    return dict(
                        error = "request parameter train_level_code is not exist"
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

def update_details(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            collection  =  common.get_collection('HCSLS_Acadame')
            if args['data']['details'].has_key('rec_id'):
                check_exist = collection.find_one(
                    {
                        "train_level_code":args['data']['train_level_code'], 
                        "details":{
                                "$elemMatch":{
                                    "rec_id":args['data']['details']["rec_id"]
                                    }
                             }
                     })
                if check_exist != None:
                    details = set_dict_detail_update_data(args['data']['details'])
                    ret = Acadame.update_details(args, details)

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
            if args['data'].has_key('train_level_code'):
                if args['data'].has_key('rec_id'):
                    ret = Acadame.remove_details(args)
                    lock.release()
                    return ret
                else:
                    error_message = "parameter 'rec_id' is not exist"
            else:
                error_message = "parameter 'train_level_code' is not exist"

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
        train_level_code       = (lambda x: x['train_level_code']      if x.has_key('train_level_code')        else None)(args['data']),
        train_level_name       = (lambda x: x['train_level_name']      if x.has_key('train_level_name')        else None)(args['data']),
        range                  = (lambda x: x['range']                 if x.has_key('range')                   else None)(args['data']),
        ordinal                = (lambda x: x['ordinal']               if x.has_key('ordinal')                 else None)(args['data']),
        note                   = (lambda x: x['note']                  if x.has_key('note')                    else None)(args['data']),
        train_cof              = (lambda x: x['train_cof']             if x.has_key('train_cof')               else None)(args['data']),
        is_fix                 = (lambda x: x['is_fix']                if x.has_key('is_fix')                  else None)(args['data']),
        coeff                  = (lambda x: x['coeff']                 if x.has_key('coeff')                   else None)(args['data']),
        begin_date_cal         = (lambda x: x['begin_date_cal']        if x.has_key('begin_date_cal')          else None)(args['data']),
        lock                   = (lambda x: x['lock']                  if x.has_key('lock')                    else None)(args['data']),
        train_level_name2      = (lambda x: x['train_level_name2']     if x.has_key('train_level_name2')       else None)(args['data']),
        details                = (lambda x: x['details']               if x.has_key('details')                 else [])(args['data'])
    )

    if ret_dict.has_key('details') and type(ret_dict['details']) is dict:
        ret_dict['details'].update(
            rec_id            = common.generate_guid(),
            seniority_from    = (lambda x: x['seniority_from']      if x.has_key('seniority_from')        else None)(args['data']),
            seniority_to      = (lambda x: x['seniority_to']        if x.has_key('seniority_to')          else None)(args['data']),
            coefficient       = (lambda x: x['coefficient']         if x.has_key('coefficient')           else None)(args['data']),
            salary            = (lambda x: x['salary']              if x.has_key('salary')                else None)(args['data']),
            created_on        = datetime.datetime.now(),
            created_by        = common.get_user_id(),
            modified_on       = None,
            modified_by       = None
        )


    return ret_dict

def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['train_level_code']
    del ret_dict['details']
    #if ret_dict.has_key('details'):
    #    del ret_dict['details']['rec_id']
    #ret_dict['details']['modified_on'] = datetime.datetime.now()
    #ret_dict['details']['modified_on'] = common.get_user_id
    return ret_dict

def set_dict_detail_insert_data(args):
    ret_dict = dict()
    ret_dict.update(
            rec_id            = common.generate_guid(),
            seniority_from    = (lambda x: x['seniority_from']      if x.has_key('seniority_from')        else None)(args),
            seniority_to      = (lambda x: x['seniority_to']        if x.has_key('seniority_to')          else None)(args),
            coefficient       = (lambda x: x['coefficient']         if x.has_key('coefficient')           else None)(args),
            salary            = (lambda x: x['salary']              if x.has_key('salary')                else None)(args),
            created_on        = datetime.datetime.now(),
            created_by        = common.get_user_id(),
            modified_on       = None,
            modified_by       = None
            )
    return ret_dict

def set_dict_detail_update_data(args):
    ret_dict = set_dict_detail_insert_data(args)
    del ret_dict['rec_id']
    ret_dict['modified_on'] = datetime.datetime.now()
    ret_dict['modified_on'] = common.get_user_id()
    return ret_dict