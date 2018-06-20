"""
The encryptor packahe support encrypt an decrypt text with mongodb sync collection
"""
_cache={}
_cache_revert={}
import re
from pymongo import MongoClient
import datetime
import logging
import threading
import uuid
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()
_coll=None
_db=None
_collection_name=None
def set_config(*args,**kwargs):
    """
    Set database connction for encrypt data sync
    :param args:including "host(mongodb server hosting)","port","name" (Database name),"collection" (the collection of encrypt data
    :param kwargs:
    :return:
    """
    global _coll
    global _db
    global _collection_name
    if type(args) is tuple and args.__len__()>0:
        args=args[0]
    else:
        args=kwargs
    if not args.has_key("host"):
        raise Exception("'host' was not found")
    if not args.has_key("port"):
        raise Exception("'port' was not found")
    if not args.has_key("name"):
        raise Exception("'name' was not found")
    if not args.has_key("collection"):
        raise Exception("'collection' was not found")
    if _coll==None:
        cnn=MongoClient(host=args["host"],port=args["port"])
        _db=cnn.get_database(args["name"])
        if args.has_key("user") and (args["user"]!="" or args["user"]!=None):
            _db.authenticate(args["user"],args["password"])
        _coll=_db.get_collection(args["collection"])
        _collection_name=args["collection"]


def get_key(value):
    """
    get uuid from value if uuid of value was not found this function will generate a uuid and sync to database then return uuid
    :param value: any text
    :return: uuid
    """
    global _cache
    global _cache_revert
    if _cache.has_key(value):
        return _cache[value]
    else:
        lock.acquire()
        try:
            item=_coll.find_one({
                "value":re.compile("^"+value+"$",re.IGNORECASE)
                })
            if item==None:
                key=str(uuid.uuid4())
                _coll.insert_one({
                    "value":value,
                    "key":key
                    })
                _cache[value]=key
                _cache_revert[key]=value
            else:
                _cache[value]=item["key"]
                _cache_revert[item["key"]]=item["value"]
            lock.release()
            return _cache[value]
        except Exception as ex:
            lock.release()
            logger.debug(ex)
            raise(ex)

def get_value(key):
    """
    get value which is corectponding with key
    :param key: uuid text
    :return: text has been map when call get_key in this package
    """
    global _cache_revert
    if _cache_revert.has_key(key):
        return _cache_revert[key]
    else:
         lock.acquire()
         try:
             item=_coll.find_one({
                "key":re.compile("^"+key+"$",re.IGNORECASE)
                })
             if item==None:
                 raise(Exception("Key was not found"))
             _cache[value]=item["key"]
             _cache_revert[item["key"]]=item["value"]
             lock.release()
             return _cache_revert[key]
         except Exception as ex:
             lock.release()
             logger.debug(ex)
             raise(ex)


