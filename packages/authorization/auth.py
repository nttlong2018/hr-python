from mongoengine.fields import key_has_dot_or_dollar
from pymongo import MongoClient
from threading import Lock
_lock=Lock()
import re
_db=None
_es=None
_es_index_view="auth_view_index"
_es_doc_type_view="auth_view_doc_type"
_es_index_role="auth_role_index"
_es_doc_type_role="auth_role_doc_type"
_privileges_cache={}
def load_config(config):
    global _db
    global _es
    if _db==None:
        _db=MongoClient(host=config["host"],port=config["port"]).get_database(config["name"])
        if config.has_key("user") and config.get("user","")!="":
            if not _db.authenticate(config["user"],config["password"]):
                raise Exception("Authenticate error ast {0}:{1}".format(config["host"],config["port"]))
    if config.has_key("elasticsearch"):
        from elasticsearch import Elasticsearch
        if _es==None:
            _es=Elasticsearch(config["elasticsearch"])
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
        if _es!=None:
            if _es.exists(index=_es_index_view, doc_type=_es_doc_type_view, id=kwargs["id"]):
                _es.update(index=_es_index_view, doc_type=_es_doc_type_view, id=kwargs["id"], body={"doc": kwargs})
            else:
                _es.create(index=_es_index_view, doc_type=_es_doc_type_view, id=kwargs["id"], body=kwargs)
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
        if _es != None:
            if _es.exists(index=_es_index_view, doc_type=_es_doc_type_view, id=kwargs["id"]):
                _es.update(index=_es_index_view, doc_type=_es_doc_type_view, id=kwargs["id"],
                           body={"doc": kwargs})
            else:
                _es.create(index=_es_index_view, doc_type=_es_doc_type_view, id=kwargs["id"], body=kwargs)
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
def create_role(*args,**kwargs):
    print(kwargs)
def get_view_of_user(*args,**kwargs):
    global _privileges_cache
    key="{0}/{1}".format(kwargs["view_id"],kwargs["user_id"])
    if not _privileges_cache.has_key(key):
        try:
            _lock.acquire()
            lst=list(_db.get_collection("sys_roles").aggregate([
                {
                    "$unwind":"$Views"
                },{
                    "$match":{
                        "path":{
                            "$regex":re.compile("^"+kwargs["view_id"]+"$",re.IGNORECASE)
                        }
                    }
                }
            ]))
            if lst.__len__()==0:
                _lock.release()
                _privileges_cache[key]=None
                return None
            else:
                lst_roles=list(_db.get_collection("sys_users").aggregate([
                    {
                        "$unwind":"$Roles"
                    },{
                        "$match":{
                            "Code":lst[0]["Code"]
                        }
                    }
                ]))
                if lst_roles.__len__()==0:
                    _lock.release()
                    _privileges_cache[key] = None
                    return None
                else:
                    _privileges_cache[key]=lst[0]["Views"]
            _lock.release()
        except Exception as ex:
            _lock.release()
            raise ex

    return _privileges_cache[key]
def create_role(*args,**kwargs):
    kwargs=args[0]
    role=_db.get_collection("sys_roles").find_one({
        "Code":re.compile("^"+ kwargs.get("code","")+"$",re.IGNORECASE)
    })
    if role==None:
        ret=_db.get_collection("sys_roles").insert_one({
            "Code":kwargs.get("code",""),
            "Name":kwargs.get("name",""),
            "Description":kwargs.get("description")
        })
        ret_doc= {
            "id":ret.inserted_id.__str__(),
            "code":kwargs.get("code",""),
            "name":kwargs.get("name",""),
            "description":kwargs.get("description","")
        }
        if _es != None:
            if _es.exists(index=_es_index_role, doc_type=_es_doc_type_role, id=kwargs["code"]):
                _es.update(index=_es_index_role, doc_type=_es_doc_type_role, id=kwargs["code"],
                           body={"doc": ret_doc})
            else:
                _es.create(index=_es_index_role, doc_type=_es_doc_type_role, id=kwargs["code"], body=ret_doc)

        return  ret_doc;
    else:
        _db.get_collection("sys_roles").update({
            "Code": re.compile("^" + kwargs.get("code", "") + "$", re.IGNORECASE)
        },{
            "$set":{
                "name": kwargs.get("name", ""),
                "description": kwargs.get("description", "")
            }
        })
        ret_doc= {
            "id": role["_id"].__str__(),
            "code": kwargs.get("code", ""),
            "name": kwargs.get("name", ""),
            "description": kwargs.get("description", "")
        }
        if _es != None:
            if _es.exists(index=_es_index_role, doc_type=_es_doc_type_role, id=kwargs["code"]):
                _es.update(index=_es_index_role, doc_type=_es_doc_type_role, id=kwargs["code"],
                           body={"doc": ret_doc})
            else:
                _es.create(index=_es_index_role, doc_type=_es_doc_type_role, id=kwargs["code"], body=ret_doc)
def get_list_of_roles(*args,**kwargs):
    kwargs=args[0]
    project={
        "id":"_$id",
        "code":"$Code",
        "name":"$Name",
        "description":"$Description"
    }
    if kwargs.get("search",None)!=None and kwargs.get("search",None)!="":
        if _es!=None:
            x = _es.search(index=_es_index_role, body={"query": {"query_string": {"query": kwargs["search"]}}})
            ret_search = x["hits"]
            ret = {
                "pager": {},
                "items": [x["_source"] for x in ret_search["hits"]]
            }

            ret.update({
                "pager": {
                    "index": kwargs.get("page_index",0),
                    "size":kwargs.get("page_size",50) ,
                    "total": ret_search["total"]
                }
            })
            return ret
        else:
            txt_search=kwargs["search"]
            match={
                "$or":[
                    {
                        "Code":{"$regex":re.compile(txt_search,re.IGNORECASE)}
                    },{
                        "Name": {"$regex": re.compile(txt_search , re.IGNORECASE)}
                    },{
                        "Description": {"$regex": re.compile(txt_search, re.IGNORECASE)}
                    }
                ]
            }
            total =list( _db.get_collection("sys_roles").aggregate([
                {
                    "$match":match
                },{
                    "$count":"1"
                }
            ]))[0]
            items=list(_db.get_collection("sys_roles").aggregate([
                {
                    "$match":match
                },{
                    "$skip":kwargs.get("page_size",50)*kwargs.get("page_index",0)
                },{
                    "$limit":kwargs.get("page_size",50)
                },
                {
                    "$project":project
                }
                ]))
            return {
                "items": items,
                "pager": {
                    "index": kwargs.get("page_index", 0),
                    "size": kwargs.get("page_size", 50),
                    "total": total
                }
            }
    else:
        total=_db.get_collection("sys_roles").count()
        items=list(_db.get_collection("sys_roles").aggregate([
            {
              "$skip":kwargs.get("page_size",50)*kwargs.get("page_index",0)
            },{
                "$limit":kwargs.get("page_size",50)
            },
            {
                "$project":project
            }
        ]))
        return {
            "items":items,
            "pager":{
                "index": kwargs.get("page_index", 0),
                "size": kwargs.get("page_size", 50),
                "total": total
            }
        }
def grant_role_to_user(*args,**kwargs):
    role_code=kwargs["role_code"]
    username=kwargs["username"]
    role=_db.get_collection("sys_roles").find_one({
        "Code":re.compile("^"+role_code+"$",re.IGNORECASE)
    })
    if role_code==None:
        return {
            "error":{
                "message":"Role was not found",
                "code":"RNF"
            }
        }
    user=_db.get_collection("sys_users").find_one({
        "Username":re.compile("^"+username+"$",re.IGNORECASE)
    })
    if user==None:
        return {
            "error": {
                "message": "User was not found",
                "code": "RNF"
            }
        }
    lst=list( _db.get_collection("sys_users").aggregate([
        {
            "$match":{
                "Roles.Code":{
                    "$regex":re.compile("^"+role_code+"$",re.IGNORECASE)
                }
            }
        }
    ]))
    if lst.__len__()==0:
        _db.get_collection("sys_users").update_one({
            "Username": re.compile("^" + username + "$", re.IGNORECASE)
        },{
            "$push":{
                "Roles":{
                    "Code":role["Code"],
                    "Name":role["Name"],
                    "Description":role["Description"]
                }
            }
        })
    lst = list(_db.get_collection("sys_roles").aggregate([
        {
            "$match": {
                "Users.Username": {
                    "$regex": re.compile("^" + username + "$", re.IGNORECASE)
                }
            }
        }
    ]))
    if lst.__len__()==0:
        _db.get_collection("sys_roles").update_one({
            "Code": re.compile("^" + role_code + "$", re.IGNORECASE)
        }, {
            "$push": {
                "Users": {
                    "Username": user["Username"],
                    "DisplayName": user.get("DisplayName",""),
                    "Description": user.get("Description","")
                }
            }
        })
    return  {}
def add_view_to_role(*args,**kwargs):
    view=_db.get_collection("sys_views").find_one({
        "Path":re.compile("^"+kwargs["view_path"]+"$",re.IGNORECASE),
        "App":re.compile("^"+kwargs["app"]+"$",re.IGNORECASE),
    })
    if view==None:
        return {
            "error":{
                "message":"View was not found",
                "code":"VNF"
            }
        }
    role=_db.get_collection("sys_roles").find_one({
        "Code": {"$regex": re.compile("^" + kwargs["role_code"] + "$", re.IGNORECASE)}
    })
    if role==None:
        return {
            "error": {
                "message": "role was not found",
                "code": "RNF"
            }
        }


    _db.get_collection("sys_roles").update_one({
        "Code": {"$regex": re.compile("^" + kwargs["role_code"] + "$", re.IGNORECASE)}
    },{
        "$pull":{
            "Views":{
                "$and": [{
                    "Path": {
                        "$regex": re.compile("^" + kwargs["view_path"] + "$", re.IGNORECASE)
                    }},
                    {"App": {
                        "$regex": re.compile("^" + kwargs["app"] + "$", re.IGNORECASE)
                    }}]
            }
        }

    })

    _db.get_collection("sys_roles").update_one({
        "Code": {"$regex": re.compile("^" + kwargs["role_code"] + "$", re.IGNORECASE)}
    }, {
        "$push": {
            "Views": {
                "App":kwargs["app"],
                "Path": kwargs["view_path"],
                "Read":kwargs["read"],
                "Created":kwargs["create"],
                "Update":kwargs["update"],
                "Delete":kwargs["delete"],
                "Extends":kwargs["extends"],
                "IsPublic":kwargs["is_public"]
            }
        }
    })
def get_list_of_views(*args,**kwargs):
   items=list(_db.get_collection("sys_views").aggregate([
       {
           "$project":{
               "_id":0,
               "id":"$_id",
               "code":"$Code",
               "name":"$Name",
               "path":"$Path",
               "app":"$App",
               "description":"$Description"
           }
       }

   ]))
   return [{
       "id":x["id"].__str__(),
       "path":x["path"],
       "name":x["name"],
       "description":x.get("description"),
       "app":x.get("app","")

   } for x in items]






