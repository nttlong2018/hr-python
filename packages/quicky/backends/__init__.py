from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
"""
This package allow login without using password. 
How to use this:
    from django.contrib.auth.models import User
    
    from django.contrib.auth import  login
    user = User.objects.get(username="<username>", schema="<schema>")
    setattr(user, "backend", 'quicky.backends.HashModelBackend')
    request.user = user
    ling(request, user, schema="<schema>")

"""
class HashModelBackend(ModelBackend):
    def authenticate(self, username=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
            return user
        except UserModel.DoesNotExist:
            return None
import re
from pymongo import MongoClient
_db = None
_coll = None
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
def create_login_token(username,schema):
    if _coll == None:
        raise (Exception("It looks like you for get call 'quicky.backends.set_config\r\n"
                         "How to call it?\r\n"
                         "from quicky import backends\r\n"
                         "backends.set_config(dict(\r\n"
                         "host=...\r\n"
                         "port=...\r\n"
                         "name=..database name \r\n"
                         "collection=..name of storage token collection ..."
                         ")"))
    ret=_coll.insert_one({
        "username":username,
        "schema":schema
    })
    return ret.inserted_id.__str__()
def sigin_by_login_token(request,token,next_url):
    if _coll == None:
        raise (Exception("It looks like you for get call 'quicky.backends.set_config\r\n"
                         "How to call it?\r\n"
                         "from quicky import backends\r\n"
                         "backends.set_config(dict(\r\n"
                         "host=...\r\n"
                         "port=...\r\n"
                         "name=..database name \r\n"
                         "collection=..name of storage token collection ..."
                         ")"))
    from django.contrib.auth.models import User
    from django.contrib.auth import get_user_model
    from django.contrib.auth import login
    from django.shortcuts import redirect
    from bson import ObjectId
    ret=_coll.find_one({
        "_id":ObjectId(token)
    })
    try:
        user = User.objects.get(username=ret["username"], schema=ret["schema"])
        setattr(user, "backend", 'quicky.backends.HashModelBackend')
        request.user = user
        login(request, user, schema=ret["schema"])
        return redirect(next_url)

        # return user
    except Exception as ex:
        return