import json
import re
from pprint import pprint

from pymongo import MongoClient
import os
_db=None
def set_connect(*args,**kwargs):
    global _db
    settings=kwargs
    if type(args) is dict:
        settings=args
    elif type(args) is tuple and args.__len__()>0:
        settings=args[0]
    if _db==None:
        cnn = MongoClient(
            host=settings["host"],
            port=settings["port"]
        )
        db = cnn.get_database(settings["name"])
        if settings["user"] != None and settings["user"] != "":
            if not db.authenticate(settings["user"], settings["password"]):
                raise (Exception("Can not authenticate data"))
        _db = db
def sync_json_data_from_file(json_file_path,collection_name,keys=None):
    try:
        with open(json_file_path) as f:
            data = json.load(f)
            if type(data) is list:
                if keys==None:
                    raise (Exception("It look like you forgot set sysn keys at 'keys' params when call '{0}.sync_json_data_from_file'?\n"
                                     "What is keys params?\n"
                                     "keys is a list of key field for database compare when data is syncrozie to databas"
                                     .format(__name__)))
                coll=_db.get_collection(collection_name)
                for item in data:
                    where={}
                    updater={}
                    for key in keys:
                        if type(item[key]) in [str,unicode]:
                            where.update({
                                key:{"$regex":re.compile("^"+item[key]+"$",re.IGNORECASE)}
                            })
                        else:
                            where.update({
                                key: {
                                    "$eq":  item[key]
                                    }
                            })

                    itm=coll.find_one(where)
                    if itm==None:
                        coll.insert_one(item)
                    else:
                        for key in item.keys():
                            if not key in keys:
                                updater.update({
                                    key:item[key]
                                })
                        coll.update_one(where,{
                            "$set":updater
                        })
            return data
    except Exception as ex:
        raise (Exception("Call '{0}.sync_json_data_from_file' has been error:\n '{1}'".format(__name__,ex)))
