# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import common

def get_dropdown_collections(args):
    HCSSYS_CollectionInfo = common.get_collection("HCSSYS_CollectionInfo")
    ret = HCSSYS_CollectionInfo.aggregate([
        {
            '$group':{
                 '_id': {
                     "caption":"$table_name", 
                     "value" : "$table_name"
                    }
            }
        },
        {
            '$replaceRoot': { 'newRoot': "$_id" }
        }
        ])

    return list(ret)

def get_dropdown_columns(args):
    pass