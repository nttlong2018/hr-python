# -*- coding: utf-8 -*-
from bson import ObjectId
import models
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

def updare(args):
    try:
        lock.acquire()

        return None
        lock.release()
    except Exception as ex:
        lock.release()
        pass

def delete(args):
    try:
        return None
    except Exception as ex:
        pass

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