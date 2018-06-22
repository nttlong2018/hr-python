# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import datetime
import logging
import encryptor
import quicky
from qmongo import helpers
import qmongo
import uuid
logger = logging.getLogger(__name__)

__collectionName = ''
__collection = {}
__transaction_collection = None

def generate_guid():
    return str(uuid.uuid4())

def get_collection(col_name):
    return models.db_context.db.get_collection(quicky.tenancy.get_schema() + "." + col_name)

def get_pagination(args):
    try:
        global __collectionName 
        global __collection 

        if('collection' in args['data'].keys()):
            __collectionName    =   args['data']['collection']
            __collection        =   getattr(models, __collectionName)()
            pageIndex           =   args['data'].get('pageIndex', 0)
            pageSize            =   args['data'].get('pageSize', 20)
            where               =   args['data'].get('where', '')
            sort                =   args['data'].get('sort', {})
            return get_data(pageIndex, pageSize, where, sort)
        return {"error":"Not found collection name"}

    except Exception as ex:
        logger.debug(ex)
        raise(ex)

def get_data(pageIndex, pageSize, where, sort):
    try:
        global __collection
        _Sort   =   (lambda x: x if x != None else {})(sort)
        item    =   __collection.aggregate()
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

        ret      = {}
        ret_list = []

        if (args['data'] != None) or (not args['data'].has_key('key')) or (args['data']['key'] == ""):

            combobox_code = encryptor.get_value(args['data']['key'])

            combobox_info = models.HCSSYS_ComboboxList().aggregate().project(
                combobox_code       =   1,
                language            =   1,
                display_name        =   1,
                description         =   1,
                table_name          =   1,
                table_fields        =   1,
                display_fields      =   1,
                predicate           =   1,
                value_field         =   1,
                caption_field       =   1,
                sorting_field       =   1,
                filter_field        =   1,
                multi_select        =   1,
                page_size           =   1)

            language_code = quicky.applications.get_settings().LANGUAGE_CODE
            combobox_info = combobox_info.match("combobox_code == {0} and language == {1}", combobox_code, language_code).get_item()

            __collectionName = combobox_info['table_name']

            try:
                __collection = getattr(models, __collectionName)()
            except Exception as ex:
                return {"error":"Not found collection name"}

            column    = combobox_info['table_fields']
            where     = combobox_info['predicate']
            sort      = combobox_info['sorting_field']
            filter    = []
            page_size = 30

            if combobox_info.has_key("filter_field"):
                filter = combobox_info['filter_field']

            if combobox_info.has_key("page_size"):
                page_size = combobox_info['page_size']

            if column != []:
                try:
                    dict_column = dict()
                    for x in column:
                        dict_column.update({x:1})
                    if where.has_key("column") and (where.get('column', None) != None and len(where.get('column', None)) > 0):
                        for x in where['column']:
                            dict_column.update({x:1})
                    ret = __collection.aggregate().project(dict_column)
                except Exception as ex:
                    raise(Exception("column not exist in collection"))
            else:
                raise(Exception("Not found column name"))

            #predicate
            if where.has_key('operator') and \
               (where.get('column', None) != None and\
               len(where.get('column', None)) > 0) and\
               where.get('operator', '') != "":
                try:
                    if args['data'].has_key('value') and args['data'].get('value', None) != None and type(args['data']['value']) is list:
                        dict_where = dict()
                        for x in args['data']['value']:
                            new_key    = x.keys()[0].replace("@", "")
                            old_key    = x.keys()[0]
                            x[new_key] = x.pop(old_key)
                            dict_where.update(x)

                        ret.match(where['operator'], dict_where)
                    else:
                        ret.match(where['operator'])

                except Exception as ex:
                    raise(Exception("syntax where error"))

                #filter with text from browser
                if args['data'].has_key('search') and args['data'].get('search', None) != None and args['data']['search'] != "":
                    if len(filter) > 0:
                        filter_query = ""
                        filter_dict = dict()
                        for i in range(len(filter)):
                            if i == len(filter):
                                filter_query += "contains(" + filter[i] + ", " + "@" + filter[i] + ")"
                            else:
                                filter_query += "contains(" + filter[i] + ", " + "@" + filter[i] + ") or "
                            filter_dict.update({filter[i].format() : args['data']['search']})

                        ret.match(filter_query, filter_dict)

            if sort != {}:
                try:
                    ret.sort(sort)
                except Exception as ex:
                    raise(Exception("syntax sort error"))

            #Pagination
            page_index = 0
            data = dict()
            if args['data'].has_key('pageIndex') and args['data'].get('pageIndex', None) != None:
                page_index = args['data']['pageIndex']

            data = ret.get_page(page_index, page_size)

            if data != {}:
                for y in where['column']:
                    for x in data['items']:
                        if y not in data['items'][0].keys():
                            del x[y.format()]

            ret_list = data


            return {"data"           : ret_list,
                    "display_name"   : combobox_info["display_name"],
                    "display_fields" : combobox_info["display_fields"],
                    "value_field"    : combobox_info["value_field"],
                    "caption_field"  : combobox_info["caption_field"],
                    "sorting_field"  : combobox_info["sorting_field"],
                    "filter_field"   : combobox_info["filter_field"],
                    "page_size"      : combobox_info["page_size"],
                    "error"          : None}
        raise(Exception("Not found collection name"))

    except Exception as ex:
        logger.debug(ex)
        return {"data": None, "error": ex.message}

