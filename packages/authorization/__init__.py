_instance_=None
_cache={}
_cache_view={}
_provider_name=""
import importlib
import inspect
import threading
_role_index_search_="authorization_role_index"
_view_index_search_="authorization_view_index"
from threading import Lock
_lock=None
from . import models
def set_provider(name):
    global _provider_name
    global _instance_
    global _cache
    global lock
    _provider_name = name
    _lock=Lock()
    _instance_ = importlib.import_module(name)
def load_config(*args,**kwargs):
    fx = lambda x, y: y if x.keys().__len__() == 0 else x
    _config=fx(kwargs,args)[0]

    global _lock
    if _lock == None:
        _lock = Lock()
    if _config==None or _config.keys().__len__()==0:
        raise Exception("Config is emty")
    try:
        _instance_.load_config(_config)
    except Exception as ex:
        _lock.release()
        raise Exception("Error at '{0}' with message {1}".format(_provider_name,ex))

def validate_view_args(args):


    keys=["id","path","name","create","read","dalete","update","app","custom","description"]
    require_keys=["id","path","name","create","read","dalete","update","app"]
    ok=True
    for key in args.keys():
        if not (key in keys):
            raise Exception("'{0}' is invalid".format(key))
    for key in require_keys:
        ok=ok and args.has_key(key)
    if not ok:
        Exception("Param require {0}",require_keys)
def register(*arg,**args):
    validate_view_args(args)
    key="{0}/{1}".format(args["app"],args["id"]).lower()
    try:
        if not _cache.has_key(key):
            _lock.acquire()
            view=_instance_.register(**args)
            _cache[key]=view
            _lock.release()
    except Exception as ex:
        _lock.release()
        raise Exception("Error at '{0}' with message {1}".format(_provider_name, ex))

def get_view_of_role(*self,**kwargs):
    view=None
    key="{0}/{1}/{2}".format(kwargs["app"],kwargs["id"],kwargs["role_id"])
    try:
        if not _cache_view.has_key(key):
            _lock.acquire()
            view=_instance_.get_view_of_role(kwargs)
            _cache_view[key]=view
            _lock.release()
        return _cache_view[key]
    except Exception as ex:
        raise Exception("get_view_of_role {0}".format(ex))
def create_role(*self,**kwargs):
    if not kwargs.has_key("id"):
        raise Exception("id is require")
    if not kwargs.has_key("name"):
        raise Exception("name is require")
    if not kwargs.has_key("code"):
        raise Exception("code is require")
    try:
        return _instance_.create_role(kwargs)
    except Exception as ex:
        raise Exception("Error at '{0}' with message {1}".format(_provider_name, ex))

def add_user_to_role(*args,**kwargs):
    try:
        return _instance_.add_user_to_role(kwargs)
    except Exception as ex:
        raise Exception("create_role {0}".format(ex))
def set_view_to_role(*args,**kwargs):
    if not kwargs.has_key("view_id"):
        raise Exception("view_id is require")
    if not kwargs.has_key("role_id"):
        raise Exception("role_id is require")
    if not kwargs.has_key("create"):
        raise Exception("create is require")
    if not kwargs.has_key("read"):
        raise Exception("read is require")
    if not kwargs.has_key("update"):
        raise Exception("update is require")
    if not kwargs.has_key("delete"):
        raise Exception("delete is require")
    if not kwargs.has_key("description"):
        raise Exception("description is require")
    try:
        return _instance_.set_view_to_role(kwargs)
    except Exception as ex:
        raise Exception("Error at '{0}' with message {1}".format(_provider_name, ex))
def get_list_of_roles(*args,**kwargs):
    if not kwargs.has_key("search"):
        raise Exception("search is missing")
    if not kwargs.has_key("page_index"):
        raise Exception("page_index is missing")
    if not kwargs.has_key("page_size"):
        raise Exception("page_size is missing")
    return _instance_.get_list_of_roles(kwargs)
def get_list_of_views(*args,**kwargs):
    if not kwargs.has_key("search"):
        raise Exception("search is missing")
    if not kwargs.has_key("page_index"):
        raise Exception("page_index is missing")
    if not kwargs.has_key("page_size"):
        raise Exception("page_size is missing")
    try:
        return _instance_.get_list_of_views(kwargs)
    except Exception as ex:
        raise Exception("Error at '{0}' with message {1}".format(_provider_name, ex))
def get_view_info(*args,**kwargs):
    if not kwargs.has_key("id"):
        raise Exception("id is missing")
    if not kwargs.has_key("app"):
        raise Exception("app is missing")
    key = "{0}/{1}".format(kwargs["app"], kwargs["id"]).lower()

    try:
        if not _cache.has_key(key):
            _lock.acquire()
            view=_instance_.get_view_info(*args,**kwargs)
            _cache[key]=view
            _lock.release()
        return _cache[key]
    except Exception as ex:
        _lock.release()
        raise Exception("Error at '{0}' with message {1}".format(_provider_name, ex))

