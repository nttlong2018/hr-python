# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import datetime
import logging
logger = logging.getLogger(__name__)

__collectionName = ''
__collection = {}
def get_pagination(args):
    try:
        global __collectionName 
        global __collection 

        if('collection' in args['data'].keys()):
            __collectionName = args['data']['collection']
            __collection= getattr(models, __collectionName)()
            pageIndex = args['data'].get('pageIndex', 0)
            pageSize = args['data'].get('pageSize', 20)
            where = args['data'].get('where', '')
            sort = args['data'].get('sort', {})
            return get_data(pageIndex, pageSize, where, sort)
        return {"error":"Not found collection name"}

    except Exception as ex:
        logger.debug(ex)
        raise(ex)

def get_data(pageIndex, pageSize, where, sort):
    try:
        global __collection
        _Sort = (lambda x: x if x != None else {})(sort)
        item = __collection.aggregate()
        if(where != ''):
            item.match(where)
            if _Sort != {}:
                item.sort(_Sort)
        return item.get_page((lambda pIndex: pIndex if pIndex != None else 0)(pageIndex),\
                            (lambda pSize: pSize if pSize != None else 20)(pageSize))
    except Exception as ex:
        logger.debug(ex)
        raise(ex)

def get_config(args):
    try:
        return models.HCSSYS_SystemConfig().aggregate().get_list()[0]
    except Exception as ex:
        logger.debug(ex)
        raise(ex)

def get_dropdown_list(args):
    #Hàm get dropdown list theo tên collection và tên cột
    try:
        global __collectionName 
        global __collection 

        ret = {}
        ret_list = []

        if('collection' in args['data'].keys()):

            __collectionName = args['data']['collection']
            try:
                __collection= getattr(models, __collectionName)()
            except Exception as ex:
                return {"error":"Not found collection name"}

            column = (lambda data: data["column"] if data.has_key("column") else {})(args['data'])
            where = (lambda data: data["where"] if data.has_key("where") else "")(args['data'])
            sort = (lambda data: data["sort"] if data.has_key("where") else {})(args['data'])

            if(len(column) != 2):
                raise(Exception("too much columns are declared"))

            if column != {}:
                try:
                    dict_column = dict()
                    for x in column:
                        dict_column.update({x:1})
                    ret = __collection.aggregate().project(dict_column)
                except Exception as ex:
                    raise(Exception("column not exist in collection"))
            else:
                raise(Exception("Not found column name"))

            if where != "":
                try:
                    ret.where(where)
                except Exception as ex:
                    raise(Exception("syntax where error"))

            if sort != {}:
                try:
                    ret.sort(sort)
                except Exception as ex:
                    raise(Exception("syntax sort error"))

            data = ret.get_list()

            for x in data:
                ret_list.append(
                    dict(
                        value = x[column[0]],
                        caption = x[column[1]],
                        custom = x[column[1]]
                        )
                    )


            return {"data" : ret_list, "error": None}
        raise(Exception("Not found collection name"))

    except Exception as ex:
        logger.debug(ex)
        return {"data": None, "error": ex.message}
