# -*- coding: utf-8 -*-
from bson import ObjectId
import models
from Query import JobWorkingGroup
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
    ret=JobWorkingGroup.get_job_working_group()
    
    if(searchText != None):
        ret.match("contains(gjw_name, @name)",name=searchText)

    if(sort != None):
        ret.sort(sort)
        
    return ret.get_page(pageIndex, pageSize)
