from pymongo import MongoClient
import re
_db=None
_es=None
def load_config(config):
    global _db
    global _es
    if _db==None:
        _db=MongoClient(host=config["host"],port=config["port"]).get_database(config["name"])
        if config.has_key("user"):
            if not _db.authenticate(config["user"],config["password"]):
                raise Exception("Authenticate error ast {0}:{1}".format(config["host"],config["port"]))
    if config.has_key("elasticsearch"):
        from elasticsearch import Elasticsearch
        if _es==None:
            _es=Elasticsearch(config["elasticsearch"])




    print config
def register(*args,**kwargs):
    item=_db.get_collection("sys_views").find_one({
                "App":{"$regex": re.compile("^"+ kwargs["app"]+"$",re.IGNORECASE)},
                "Path":{"$regex": re.compile("^"+ kwargs["id"]+"$",re.IGNORECASE)}
           })
    if item==None:
        ret=_db.get_collection("sys_views").insert_one({
            "App":kwargs["app"],
            "Path":kwargs["id"],
            "Create":kwargs.get("create",False),
            "Read": kwargs.get("read", False),
            "Update": kwargs.get("update", False),
            "Delete": kwargs.get("delete", False),
            "IsPulic": kwargs.get("is_public", False),
            "Extend": kwargs.get("extend", {}),
            "Description": kwargs.get("Description", ""),
            "Name":kwargs.get("name",kwargs.get("id"))
        })
        return {
            "app":kwargs["app"],
            "id":kwargs["id"],
            "view_id":ret.inserted_id.__str__(),
            "create":kwargs.get("create",False),
            "read": kwargs.get("read", False),
            "update": kwargs.get("update", False),
            "delete": kwargs.get("delete", False),
            "is_public":kwargs.get("is_pulic",False),
            "extend":kwargs.get("extend"),
            "description":kwargs.get("description")
        }
    else:
        return {
            "app": kwargs["app"],
            "id": kwargs["id"].__str__(),
            "view_id": item["_id"],
            "create": item.get("Create", False),
            "read": item.get("Read", False),
            "update": item.get("Update", False),
            "delete": item.get("Delete", False),
            "is_public": item.get("IsPulic", False),
            "extend": item.get("Extend"),
            "description": item.get("Description")
        }
def get_view_info(*args,**kwargs):
    item = _db.get_collection("sys_views").find_one({
        "App": {"$regex": re.compile("^" + kwargs["app"] + "$", re.IGNORECASE)},
        "Path": {"$regex": re.compile("^" + kwargs["id"] + "$", re.IGNORECASE)}
    })
    if item==None:
        return None
    else:
        return {
            "app": kwargs["app"],
            "id": kwargs["id"].__str__(),
            "view_id": item["_id"],
            "create": item.get("Create", False),
            "read": item.get("Read", False),
            "update": item.get("Update", False),
            "delete": item.get("Delete", False),
            "is_public": item.get("IsPulic", False),
            "extend": item.get("Extend"),
            "description": item.get("Description")
        }
