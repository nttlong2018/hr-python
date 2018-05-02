from . import extens
from . import applications
from . import authorize
import threading
import logging
import os
logger=logging.getLogger(__name__)
global lock
lock=threading.Lock()
_cache_view={}
def template_uri(fn):
    def layer(*args, **kwargs):
        def repl(f):
            return fn(f,*args, **kwargs)
        return repl
    return layer
@template_uri
def template(fn,*_path,**kwargs):
    if _path.__len__()==1:
        _path=_path[00]
    if _path.__len__()==0:
        _path=kwargs


    app=applications.get_app_by_file(fn.func_code.co_filename)
    def exec_request(request, **kwargs):
        try:


            from django.shortcuts import redirect
            is_allow = True
            is_public = False
            authenticate = None

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
                    if request.path_info == login_url:
                        return fn(request, **kwargs)
                    else:
                        url = request.get_abs_url() + login_url
                        url += "?next=" + request.get_abs_url() + request.path
                        return redirect(url)
            if hasattr(app.settings, "authenticate"):
                if not app.settings.authenticate(request):
                    if login_url==None:
                        raise (Exception("it look like you forgot set 'login_url' in {0}/settings.py".format(app.path)))
                    url = request.get_abs_url() + login_url
                    url += "?next=" + request.get_abs_url() + request.path
                    return redirect(url)

            return fn(request, **kwargs)
        except Exception as ex:
            logger.debug(ex)
            raise (ex)

    return exec_request