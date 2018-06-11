# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import logging
logger = logging.getLogger(__name__)

def update(args):
    try:
        if args['data'] != None:
            ret = models.HCSSYS_SystemConfig().update(
            args['data'],
            "_id==@_id",
            dict(
                _id = ObjectId(args['data']['_id'])
            ))
            return ret
        return None
    except Exception as ex:
        logger.debug(ex)
        raise(ex)