import re
from pymongo import MongoClient
import datetime

_coll=None
_db=None
_collection_name=None
def set_config(*args,**kwargs):
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

def get_language_item(schema,lan,app,view,key,value):
    global _coll
    global lock
    coll=_coll
    if schema!=None:
        coll=_db.get_collection(schema+"."+_collection_name)
    item=coll.find_one({
            "Language":{
                "$regex":re.compile("^"+lan+"$",re.IGNORECASE)
            },
            "App":{
                "$regex": re.compile("^" + app + "$", re.IGNORECASE)
            },
            "View":{
                "$regex": re.compile("^" + view + "$", re.IGNORECASE)
            },
            "Key":{
                "$regex": re.compile("^" + key + "$", re.IGNORECASE)
            }
        })
    if item==None:
        coll.insert_one({
            "Language":lan,
            "App":app,
            "View":view,
            "Key":key,
            "Value":value
        })
        return value
    else:
        return item["Value"]
