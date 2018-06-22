# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import auth_user
import tmp_transactions
import common
import datetime
import logging
import threading
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()

def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data = dict(
                role_code = args['data']['role_code'],
                role_name = args['data']['role_name'],
                dd_code = args['data']['dd_code'],
                stop = (lambda data: data["stop"] if data.has_key("stop") else False)(args['data']),
                description = (lambda data: data["description"] if data.has_key("description") else None)(args['data'])
                )
            ret =  models.AD_Roles().insert(data)
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
            data = dict(
                _id = ObjectId(args['data']['_id']),
                role_name = args['data']['role_name'],
                dd_code = args['data']['dd_code'],
                stop = (lambda data: data["stop"] if data.has_key("stop") else False)(args['data']),
                description = (lambda data: data["description"] if data.has_key("description") else None)(args['data'])
                )

            #data_lock = models.common()

            #data_trans = tmp_transactions.create(common.generate_guid(), "api_path", dat, ord = 1)

            ret = models.AD_Roles().update(
                    data,
                    "_id == {0}",
                    data['_id'])

            #ret_user = {}
            #if args['data'].has_key('users'):
            #    usernames = [x["username"]for x in args['data']['users']]
            #    ret_user =  auth_user.update_role_code(usernames, args['data'][role_code])
            ##Update cột role code vào bảng auth_user_info
            #user_names = [x["username"]for x in (lambda data: data["users"] if data.has_key("users") else [])(args['data'])]
            #if len(user_names) > 0:
            #    try:
            #        auth_user.update_role_code(user_names, args['data']['role_code'])
            #    except Exception as ex:
            #        #rollback update AD_Roles
            #        raise(ex)
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
            role_codes = [x["role_code"]for x in  args['data']] 
            ret =  models.AD_Roles().delete("role_code in {0}", role_codes)
            #Remove role_code các user có trị tương ứng
            auth_user.remove_role_code_by_role(role_codes)
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def get_list_with_searchtext(args):
    try:
        if args['data'] != None:
                searchText      = args['data'].get('search', '')
                pageSize        = args['data'].get('pageSize', 0)
                pageIndex       = args['data'].get('pageIndex', 20)
                sort            = args['data'].get('sort', 20)

                pageIndex       = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
                pageSize        = (lambda pSize: pSize if pSize != None else 20)(pageSize)

                items = models.AD_Roles().aggregate().project(
                        role_code       = 1,
                        role_name       = 1,
                        dd_code         = 1,
                        description     = 1,
                        stop            = 1,
                        created_on      = 1
                        )

                if(searchText != None):
                    items.match("contains(role_name, @name)",name=searchText)

                if(sort != None):
                    items.sort(sort)
            
                return items.get_page(pageIndex, pageSize)

        return dict(
                error = "request parameter is not exist"
            )
    except Exception as ex:
        raise(ex)