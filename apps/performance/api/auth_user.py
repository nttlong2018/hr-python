# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from bson import ObjectId
import uuid
import models
import datetime
import logging
import threading
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()

def generate_user_id():
    return str(uuid.uuid4())


def insert(args):
    if args['data'] != None:
        ret = {}
        try:
            lock.acquire()
            user_name = args['data']['login_account']
            if User.objects.filter(username=user_name).exists() == 0:

                args['data']['username'] = generate_user_id()

                data = dict(
                    username         = args['data']['username'],
                    login_account    = args['data']['login_account'],
                    display_name     = args['data']['display_name'],
                    role_code        = (lambda data: data["role_code"] if data.has_key("role_code") else None)(args['data']),
                    email            = args['data']['email'],
                    is_system        = (lambda data: data["is_system"] if data.has_key("is_system") else False)(args['data']),
                    never_expire     = (lambda data: data["never_expire"] if data.has_key("never_expire") else False)(args['data']),
                    manlevel_from    = (lambda data: data["manlevel_from"] if data.has_key("manlevel_from") else None)(args['data']),
                    manlevel_to      = (lambda data: data["manlevel_to"] if data.has_key("manlevel_to") else None)(args['data']),
                    mobile           = (lambda data: data["mobile"] if data.has_key("mobile") else None)(args['data']),
                    description      = (lambda data: data["description"] if data.has_key("description") else None)(args['data'])
                    )

                ret = models.auth_user_info().insert(data)
                if ret.has_key('error') and ret['error'] != None:
                    raise(Exception(ret['error']['code']))

                user = User.objects.create_user(args['data']['username'], '', args['data']['password'])
                user.save()
                lock.release()
                return ret
            lock.release()
            return dict(
                error = "existing login account"
            ) #Already account
        except Exception as ex:
                logger.debug(ex)
                lock.release()
                return ret
    return dict(
            error = "request parameter is not exist"
        )

def update(args):
    if args['data'] != None:
        try:
            lock.acquire()
            user_name = args['data']['login_account']
            if models.auth_user_info().aggregate().match("_id == {0}", ObjectId(args['data']['_id'])).get_item() != None:

                data = dict(
                    _id              = args['data']['_id'],
                    login_account    = args['data']['login_account'],
                    display_name     = args['data']['display_name'],
                    role_code        = (lambda data: data["role_code"] if data.has_key("role_code") else None)(args['data']),
                    email            = args['data']['email'],
                    is_system        = (lambda data: data["is_system"] if data.has_key("is_system") else False)(args['data']),
                    never_expire     = (lambda data: data["never_expire"] if data.has_key("never_expire") else False)(args['data']),
                    manlevel_from    = (lambda data: data["manlevel_from"] if data.has_key("manlevel_from") else None)(args['data']),
                    manlevel_to      = (lambda data: data["manlevel_to"] if data.has_key("manlevel_to") else None)(args['data']),
                    mobile           = (lambda data: data["mobile"] if data.has_key("mobile") else None)(args['data']),
                    description      = (lambda data: data["description"] if data.has_key("description") else None)(args['data'])
                    )

                ret = models.auth_user_info().update(
                    data,
                    "_id == {0}",
                    ObjectId(data['_id']))

                if args['data']['change_password'] != None and args['data']['change_password'] == True:
                    u = User.objects.get(username=args['data']['username'])
                    u.set_password(args['data']['password'])
                    u.save()

                lock.release()
                return ret

            lock.release()
            return None #Already account
        except Exception as ex:
                logger.debug(ex)
                lock.release()
                raise(ex)
    return None

def delete(args):
    if args['data'] != None:
        try:
            user_names = models.auth_user_info().aggregate().project(username = 1).match("_id in {0}", [ObjectId(x["_id"])for x in args['data']]).get_list()

            models.auth_user().delete("username in {0}", [x["username"] for x in user_names])
            ret = models.auth_user_info().delete("_id in {0}", [ObjectId(x["_id"])for x in args['data']])
            return ret
        except Exception as ex:
            logger.debug(ex)
            return dict(
                    error = ex.message
                )
    return dict(
            error = "request parameter is not exist"
        )

def get_list_with_searchtext(args):
    if args['data'] != None:
        try:
            searchText      = args['data'].get('search', '')
            pageSize        = args['data'].get('pageSize', 0)
            pageIndex       = args['data'].get('pageIndex', 20)
            sort            = args['data'].get('sort', 20)
            where           = (lambda data: data["where"] if data.has_key("where") else {})(args['data'])

            pageIndex       = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
            pageSize        = (lambda pSize: pSize if pSize != None else 20)(pageSize)

            items = models.auth_user_info().aggregate().project(
                    login_account       = 1,
                    username            = 1,
                    display_name        = 1,
                    role_code           = 1,
                    is_system           = 1,
                    never_expire        = 1,
                    manlevel_from       = 1,
                    manlevel_to         = 1,
                    email               = 1,
                    mobile              = 1,
                    description         = 1,
                    created_on          = 1
                    )

            if(searchText != None):
                items.match("contains(login_account, @name)",name=searchText)

            if(where != None and where != {}):
                try:
                    if where.has_key('filter') and  where.has_key('value') and len(where['filter']) and len(where['value']):
                        items.match(where["filter"],where["value"])
                except Exception as ex:
                    raise(Exception("syntax where error"))

            if(sort != None):
                items.sort(sort)

            return items.get_page(pageIndex, pageSize)
        except Exception as ex:
            raise(ex)

    return dict(
            error = "request parameter is not exist"
        )

def update_role_code(args):
    try:
        if args['data'] != None:
            lock.acquire()

            if args['data'].has_key('role_code') and args['data'].has_key('users'):
                user_names = [x["username"]for x in args['data']['users']]
                ret = models.auth_user_info().update(
                    dict(
                        role_code = args['data']['role_code']
                        ),
                    "username in {0}",
                    user_names)

                lock.release()
                return ret

        return dict(
            error = "request parameter is not exist"
        )

    except Exception as ex:
        logger.debug(ex)
        lock.release()
        raise(ex)

def remove_role_code_by_user(args):
    try:
        lock.acquire()
        if args['data'].has_key('users'):
            user_names = [x["username"]for x in args['data']['users']]
            ret = models.auth_user_info().update(
                dict(
                    role_code = None
                    ),
                "username in {0}",
                user_names)

            lock.release()
            return ret
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        logger.debug(ex)
        lock.release()
        raise(ex)

def remove_role_code_by_role(roles):
    try:
        lock.acquire()
        ret = models.auth_user_info().update(
            dict(
                role_code = None
                ),
            "role_code in {0}",
            roles)

        lock.release()
        return ret
    except Exception as ex:
        logger.debug(ex)
        lock.release()
        raise(ex)