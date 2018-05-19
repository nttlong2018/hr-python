from . import extens
from . import applications

from . import authorize
import threading
import logging
import os
import sys
logger=logging.getLogger(__name__)
global lock
lock=threading.Lock()
_cache_view={}
_db_multi_tenancy=None
_cache_multi_tenancy={}
def template_uri(fn):

    def layer(*args, **kwargs):
        def repl(f):
            return fn(f, *args, **kwargs)
        return repl
    return layer
@template_uri
def template(fn,*_path,**kwargs):
    if _path.__len__()==1:
        _path=_path[00]
    if _path.__len__()==0:
        _path=kwargs


    app=applications.get_app_by_file(fn.func_code.co_filename)
    setattr(fn,"__application__",app)
    from . import get_django_settings_module
    is_multi_tenancy = get_django_settings_module().__dict__.get("USE_MULTI_TENANCY", False)
    def exec_request(request, **kwargs):
        app=fn.__application__

        try:
            from django.shortcuts import redirect
            is_allow = True
            is_public = False
            authenticate = None
            if app==None and request.path[request.path.__len__() - 4:request.path.__len__()]=="/api":
                app_name=request.path.split('/')[request.path.split('/').__len__()-2]
                from . import applications
                app=applications.get_app_by_name(app_name)




            if not hasattr(app, "settings") or app.settings==None:
                raise (Exception("'settings.py' was not found in '{0}' at '{1}' or look like you forgot to place 'import settings' in '{1}/__init__.py'".format(app.name, os.getcwd()+os.sep+app.path)))
            login_url = app.get_login_url()

            if hasattr(app.settings, "is_public"):
                is_public = getattr(app.settings, "is_public")
            if hasattr(app.settings, "authenticate"):
                authenticate = getattr(app.settings, "authenticate")
            # if not is_public or callable(authenticate):

            extens.apply(request, _path, app)
            if type(_path) is dict:
                if _path.get("is_public", False):
                    return fn(request, **kwargs)
                elif _path.get("login_url", None) != None:
                    if app.host_dir != "":
                        login_url = "/" + app.host_dir + "/" + _path["login_url"]
                    else:
                        login_url = "/" + _path["login_url"]

            if login_url != None:
                if request.user.is_anonymous():
                    if request.path_info.lower() == login_url.lower():
                        return fn(request, **kwargs)
                    else:
                        url = request.get_abs_url() + login_url
                        url += "?next=" + request.get_abs_url() + request.path
                        return redirect(url)
            if hasattr(app.settings, "authenticate"):
                if not app.settings.authenticate(request):
                    if login_url==None:
                        raise (Exception("it look like you forgot set 'login_url' in {0}/settings.py".format(app.path)))
                    if request.path_info.lower() == login_url.lower():
                        return fn(request, **kwargs)
                    url = request.get_abs_url() + login_url
                    url += "?next=" + request.get_abs_url() + request.path
                    return redirect(url)

            return fn(request, **kwargs)
        except Exception as ex:
            logger.debug(ex)
            raise (ex)
    def exec_request_for_multi(request,tenancy_code, **kwargs):
        setattr(threading.current_thread(),"tenancy_code",tenancy_code)
        setattr(threading.currentThread(), "tenancy_code", tenancy_code)
        return exec_request(request,**kwargs)
    if is_multi_tenancy:
        return exec_request_for_multi
    else:
        return exec_request
def get_tenancy_schema(code):
    from . import get_django_settings_module
    import re
    cmp=re.compile("[a-zA-Z_0-9-]+\z",re.IGNORECASE)
    if get_django_settings_module().MULTI_TENANCY_DEFAULT_SCHEMA==code:
        return code
    global _db_multi_tenancy
    global _cache_multi_tenancy
    if _db_multi_tenancy==None:
        import pymongo

        config=get_django_settings_module().MULTI_TENANCY_CONFIGURATION
        cnn=pymongo.MongoClient(
            host=config["host"],
            port=config["port"]
        )
        db=cnn.get_database(config["name"])
        if config.get("user","")!="":
            db.authenticate(config["user"],config["password"])
        _db_multi_tenancy=db.get_collection(config["collection"])
    if not _cache_multi_tenancy.has_key(code):
        lock.acquire()
        try:
            item=_db_multi_tenancy.find_one(
                {
                    "Code":{
                        "$regex":re.compile("^"+code+"$",)
                    }
                }
            )
            if item==None:
                raise (Exception("'{0}' was not register"))
            lock.release()
            _cache_multi_tenancy.update({
                code: item["schema"]
            })
            return _cache_multi_tenancy["code"]
        except Exception as ex:
            lock.release()
            raise (ex)




