# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import logging
import threading
import common
import quicky
from qmongo import helpers
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()
global __transaction_collection
global __col_name
global __id
__transaction_collection = None
__col_name = None
__id = None

def get_data(id):
    return models.tmp_transactions().aggregate().project(
        transaction_id = 1,
        data = 1
        ).match("transaction_id == @transaction_id", transaction_id = id).get_item()

def begin(col_name, ses, api_path, dat, ord = 1):
    try:
        lock.acquire()
        global __id
        global __col_name
        __id = common.generate_guid()
        __col_name = col_name
        check_transactions()
        ret = models.tmp_transactions().insert(
            dict(
                transaction_id = id,
                collection_name = __col_name,
                session = ses,
                path = api_path,
                ordinal = ord,
                data = dat
                )
            )
        lock.release()
        return ret
    except Exception as ex:
        logger.debug(ex)
        lock.release()
        raise(ex)

def delete():
    ret = models.tmp_transactions().delete(
        "transaction_id == {0}",
        id
        )

def check_transactions():
    global __col_name
    global __transaction_collection
    if __transaction_collection == None:
        __transaction_collection = models.db_context.db.get_collection(quicky.tenancy.get_schema() + "." + "tmp_transactions")
    list_trans = list(__transaction_collection.find(helpers.filter("collection_name == {}", __col_name).get_filter()))
    if list_trans.__len__ != 0:
        raise(Exception('collection ' + __col_name + ' using by ' + list_trans[0]['created_by']))

def roll_back():
    global __col_name
    global __id
    col = getattr(models, __col_name)()
    #Get list ID from tmp_transactions.data
    items = __transaction_collection.aggregate().project(
        data = 1
        ).match("transaction_id = {0}", __id).get_item()
    arr_id = [ObjectId(x["_id"])for x in items['data']]

    col.delete("__id in {0}", arr_id)
    col.insert(
        items["data"]
        )


def commit():
    global __transaction_collection
    global __col_name
    global __id
    try:
        lock.acquire()
        global __id
        ret = models.tmp_transactions().delete("transaction_id == {0}", __id)
        lock.release()
        __transaction_collection = None
        __col_name = None
        __id = None
        delete()
    except Exception as ex:
        logger.debug(ex)
        lock.release()
        __transaction_collection = None
        __col_name = None
        __id = None
        delete()
        raise(ex)