# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import common
import datetime
from Query import Position
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
    ret=Position.display_list_position()
    
    if(searchText != None):
        ret.match("contains(job_pos_name, @name)",name=searchText)

    if(sort != None):
        ret.sort(sort)
        
    return ret.get_page(pageIndex, pageSize)

def get_list_details_with_searchtext(args):

    if args['data'].has_key('job_pos_code'):
        pos_code = args['data']['job_pos_code']
        searchText = args['data'].get('search', '')
        pageSize = args['data'].get('pageSize', 0)
        pageIndex = args['data'].get('pageIndex', 20)
        sort = args['data'].get('sort', 20)

        pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
        pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
        ret=Position.display_list_postion_detail(pos_code)
    
        #if(searchText != None):
        #    ret.match("contains(job_pos_name, @name)",name=searchText)

        if(sort != None):
            ret.sort(sort)

        return ret.get_page(pageIndex, pageSize)

    else:
        return dict(
            error = "job_pos_code is not exist"
        )

def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            if args['data'].has_key('_id') or args['data'].has_key('job_pos_code'):
                collection  =  common.get_collection('HCSLS_Position')
                check_exist = collection.find_one({"job_pos_code":args['data']['job_pos_code']})
                if check_exist == None:
                    data =  set_dict_insert_data(args)
                    ret  =  models.HCSLS_Position().insert(data)
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
            ret  =  models.HCSLS_Position().update(
                data, 
                "_id == {0}", 
                ObjectId(args['data']['_id']))
            if ret['data'].raw_result['updatedExisting'] == True:
                ret.update(
                    item = Position.display_list_position().match("_id == {0}", ObjectId(args['data']['_id'])).get_item()
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
            ret  =  models.HCSLS_Position().delete("_id in {0}",[ObjectId(x["_id"])for x in args['data']])
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
                if args['data'].has_key('job_pos_code'):
                    details = set_dict_detail_insert_data(args['data']['details'])
                    ret = Position.insert_details(args, details)
                else:
                    lock.release()
                    return dict(
                        error = "request parameter job_pos_code is not exist"
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
            collection  =  common.get_collection('HCSLS_Position')
            if args['data']['details'].has_key('rec_id'):
                check_exist = collection.find_one(
                    {
                        "job_pos_code":args['data']['job_pos_code'], 
                        "details":{
                                "$elemMatch":{
                                    "rec_id":args['data']['details']["rec_id"]
                                    }
                             }
                     })
                if check_exist != None:
                    details = set_dict_detail_update_data(args['data']['details'])
                    ret = Position.update_details(args, details)

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
            if args['data'].has_key('job_pos_code'):
                if args['data'].has_key('rec_id'):
                    ret = Position.remove_details(args)
                    lock.release()
                    return ret
                else:
                    error_message = "parameter 'rec_id' is not exist"
            else:
                error_message = "parameter 'job_pos_code' is not exist"

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
        job_pos_code       = (lambda x: x['job_pos_code']      if x.has_key('job_pos_code')        else None)(args['data']),
        job_pos_name       = (lambda x: x['job_pos_name']      if x.has_key('job_pos_name')        else None)(args['data']),
        job_pos_name2      = (lambda x: x['job_pos_name2']     if x.has_key('job_pos_name2')       else None)(args['data']),
        man_level          = (lambda x: x['man_level']         if x.has_key('man_level')           else None)(args['data']),
        ordinal            = (lambda x: x['ordinal']           if x.has_key('ordinal')             else None)(args['data']),
        note               = (lambda x: x['note']              if x.has_key('note')                else None)(args['data']),
        is_fix             = (lambda x: x['is_fix']            if x.has_key('is_fix')              else None)(args['data']),
        coeff              = (lambda x: x['coeff']             if x.has_key('coeff')               else None)(args['data']),
        begin_date_cal     = (lambda x: x['begin_date_cal']    if x.has_key('begin_date_cal')      else None)(args['data']),
        lock               = (lambda x: x['lock']              if x.has_key('lock')                else None)(args['data']),
        details            = (lambda x: x['details']           if x.has_key('details')             else [])(args['data'])
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
    del ret_dict['job_pos_code']
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
    ret_dict['modified_by'] = common.get_user_id()
    return ret_dict