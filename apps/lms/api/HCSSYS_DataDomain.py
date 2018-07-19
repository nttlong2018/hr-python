# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import datetime

def get_list(args):
    items = models.HCSSYS_DataDomain().aggregate().project(
        dd_code = 1,
        dd_name = 1,
        access_mode = 1,
        description = 1,
        created_on = 1,
        detail = 1
        )
    
    return items.get_list()

def get_list_with_searchtext(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)

    items = models.HCSSYS_DataDomain().aggregate().project(
            dd_code = 1,
            dd_name = 1,
            access_mode = 1,
            description = 1,
            created_on = 1,
            detail = 1
            )

    if(searchText != None):
        items.match("contains(dd_name, @name)",name=searchText)

    if(sort != None):
        items.sort(sort)
        
    return items.get_page(pageIndex, pageSize)


def insert(args):
    if args['data'] != None:
        ret = models.HCSSYS_DataDomain().insert(args['data'])
        return ret
    return None

def update(args):
    if args['data'] != None:
        if args['data']['dd_code'] == None:
            return None
        else:
            if(args['data'].has_key('dd_code')):
                args['data'].pop('dd_code')
            ret = models.HCSSYS_DataDomain().update(
            args['data'],
            "_id==@_id",
            dict(
                _id = ObjectId(args['data']['_id'])
            ))
            return ret
    return None

def delete(args):
    if args['data'] != None:
        ret = models.HCSSYS_DataDomain().delete("_id in {0}", [ObjectId(x["_id"])for x in args['data']])
        return ret
    return None