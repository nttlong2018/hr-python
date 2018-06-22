# -*- coding: utf-8 -*-
from bson import ObjectId
import models

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
        ret.match("function_id == @func_id",func_id=where)

    if(searchText != None):
        ret.match("contains(template_name, @name)",name=searchText)

    if(sort != None):
        ret.sort(sort)
        
    return ret.get_page(pageIndex, pageSize)