from . import extens
from . import applications

from . import authorize
import threading
import logging
import os
import sys
import tenancy
logger=logging.getLogger(__name__)
global lock
settings=None
lock=threading.Lock()
_cache_view={}
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
        global  settings
        if settings==None:
            from . import get_django_settings_module
            settings=get_django_settings_module()
        host_dir=None
        if hasattr(settings,"HOST_DIR"):
            host_dir=settings.HOST_DIR
        app=fn.__application__

        try:
            from django.shortcuts import redirect
            import threading
            not_inclue_tenancy_code=False
            if hasattr(request,"not_inclue_tenancy_code"):
                not_inclue_tenancy_code=request.not_inclue_tenancy_code
            is_allow = True
            is_public = False
            authenticate = None
            request_path=request.path
            tenancy_code=tenancy.get_customer_code()
            if not not_inclue_tenancy_code and tenancy_code!=None:
                request_path=request_path[tenancy_code.__len__()+1:request_path.__len__()]
            if app==None and request_path[request_path.__len__() - 4:request_path.__len__()]=="/api":
                app_name=request_path.split('/')[request_path.split('/').__len__()-2]
                if app_name==tenancy_code:
                        app_name="" 
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
                cmp_url = login_url
                if host_dir != None:
                    cmp_url = "/"+host_dir +  login_url
                if request.user.is_anonymous():
                    if request.path_info.lower() == cmp_url.lower():
                        return fn(request, **kwargs)
                    else:
                        url = request.get_abs_url() + login_url
                        url += "?next=" + request.get_abs_url() + request.path
                        return redirect(url)
            if hasattr(app.settings, "authenticate"):
                if not app.settings.authenticate(request):
                    if login_url==None:
                        raise (Exception("it look like you forgot set 'login_url' in {0}/settings.py".format(app.path)))
                    cmp_url=login_url
                    if host_dir!=None:
                        cmp_url = "/" + host_dir + login_url
                    if request.path_info.lower() == cmp_url.lower():
                        return fn(request, **kwargs)
                    url = request.get_abs_url() + login_url
                    url += "?next=" + request.get_abs_url() + request.path
                    return redirect(url)
            return fn(request, **kwargs)
        except Exception as ex:
            logger.debug(ex)
            raise (ex)
    def exec_request_for_multi(request,tenancy_code, **kwargs):

        from . import get_tenancy_schema
        code=get_tenancy_schema(tenancy_code)
        if code==None:
            from django.http import HttpResponse, HttpResponseNotFound
            return HttpResponseNotFound("Page not found")
        setattr(threading.current_thread(),"tenancy_code",code)
        setattr(threading.currentThread(), "tenancy_code", code)
        setattr(threading.current_thread(),"request_tenancy_code",tenancy_code)
        setattr(threading.currentThread(), "request_tenancy_code", tenancy_code)
        setattr(threading.current_thread(),"user",request.user)
        setattr(threading.currentThread(), "user", request.user)

        return exec_request(request,**kwargs)
    if is_multi_tenancy:
        return exec_request_for_multi
    else:
        return exec_request







