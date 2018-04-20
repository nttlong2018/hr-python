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
def load(*args,**kwargs):
    params=(lambda x,y: x if x!=() else y)(args,kwargs)
    if type(params) is tuple:
        params=params[0]

    get_value=lambda x,y: x.get(y) if x.has_key(y) else ""
    set_provider(params["provider"])
    load_config(params)
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
    _config=fx(kwargs,args)
    if type(_config) is tuple:
        _config=_config[0]

    global _lock
    if _lock == None:
        _lock = Lock()
    _lock.acquire()
    if _config==None or _config.keys().__len__()==0:
        _lock.release()
        raise Exception("Config is emty")
    try:
        _instance_.load_config(_config)
        _lock.release()
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

def grant_role_to_user(*args,**kwargs):
    if not kwargs.has_key("role_code"):
        raise Exception("'role_code' is missing")
    if not kwargs.has_key("username"):
        raise Exception("'username' is missing")
    try:
        return _instance_.grant_role_to_user(*args,**kwargs)
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
    try:
        return _instance_.get_list_of_roles(kwargs)
    except Exception as ex:
        raise Exception("Error at '{0}' with message {1}".format(_provider_name, ex))
def get_list_of_views(*args,**kwargs):
    if not kwargs.has_key("search"):
        raise Exception("search is missing")
    if not kwargs.has_key("page_index"):
        raise Exception("page_index is missing")
    if not kwargs.has_key("page_size"):
        raise Exception("page_size is missing")
    try:
        return _instance_.get_list_of_views(*args,**kwargs)
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

def get_view_of_user(*args,**kwargs):
    return _instance_.get_view_of_user(*args,**kwargs)
def is_allow_read(privileges):
    if privileges.get("is_public",False):
        return True
    return privileges.get("read",False)
def is_allow_create(privileges):
    if privileges.get("is_public", False):
        return True
    return privileges.get("create", False)
def add_view_to_role(*args,**kwargs):
    if not kwargs.has_key("view_path"):
        raise Exception("'view_path' was not found")
    if not kwargs.has_key("app"):
        raise Exception("'app' was not found")
    if not kwargs.has_key("role_code"):
        raise Exception("'role_code' was not found")
    if not kwargs.has_key("create"):
        raise Exception("'create' was not found")
    if not kwargs.has_key("read"):
        raise Exception("'read' was not found")
    if not kwargs.has_key("update"):
        raise Exception("'update' was not found")
    if not kwargs.has_key("delete"):
        raise Exception("'delete' was not found")
    if not kwargs.has_key("extends"):
        raise Exception("'extends' was not found")
    if not kwargs.has_key("is_public"):
        raise Exception("'is_public' was not found")

    try:
         ret = _instance_.add_view_to_role(*args,**kwargs)
         return ret
    except Exception as ex:
        raise Exception("Error at '{0}' with message {1}".format(_provider_name, ex))