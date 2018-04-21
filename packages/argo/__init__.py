from . import config
from . import utilities as utils
from . import models
from . import db
from . import url
from django.shortcuts import redirect
import membership
import threading
import urllib
import logging
import authorization
import applications
import language
from django.http import HttpResponse
import sys

lock = threading.Lock()
logger = logging.getLogger(__name__)
__session_cache__={}
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

    fn.__dict__.update({"__params__": _path})
    def exec_request(request, **kwargs):
        file_path=fn.__dict__["__params__"]
        auth_path = None
        login_path = None
        is_login_page=False
        is_public=False
        if type(file_path) is dict:
            is_login_page = file_path.get("is_login_page", False)
            is_public= file_path.get("is_public", False)
            auth_path = file_path.get("auth", None)
            login_path = file_path.get("login", None)
            file_path = file_path.get("file", "")
            if login_path == None and auth_path != None:
                raise Exception("'auth' require 'login'. 'login' need to be set at '" + fn.__name__ + "'")



        global _language_engine_module
        global _language_resource_cache


        language = "en"
        if request.session.has_key("language"):
            language = request.session["language"]

        app = applications.get_app_by_file(fn.func_code.co_filename)
        if auth_path==None:
            auth_path=app.auth
        if login_path==None:
            login_path=app.login

        def set_auth(data):
            global __session_cache__

            if not data.has_key("user"):
                raise Exception("Please set 'user' info {id:string,username:string}")
            __session_cache__.update({
                request.session._get_session_key(): data
            })
            request.session["authenticate"] = {
                "user": data
            }

        def get_auth():
            global __session_cache__
            login_info = membership.validate_session(request.session._get_or_create_session_key())
            if login_info == None:
                request.session["authenticate"] = {
                    "user": None
                }
                __session_cache__.update({
                    request.session._get_session_key(): {
                        "user": None
                    }
                })

            else:
                request.session["authenticate"] = {
                    "user": {
                        "user_id": login_info.user.userId,
                        "username": login_info.user.username,
                        "email": login_info.user.email
                    }
                }
                __session_cache__.update({
                    request.session._get_session_key(): {
                        "user": {
                            "user_id": login_info.user.userId,
                            "username": login_info.user.username,
                            "email": login_info.user.email
                        }
                    }
                })

            return __session_cache__[request.session._get_session_key()]

        def render(model):
            return utils.render({
                "app_name": app.name,
                "request": request,
                "language": language,
                "file": file_path,
                "model": model,
                "templates": app.template_dir,
                "static": app.client_static,
                "application": app

            })

        def get_abs_url():
            global __root_url__
            if __root_url__ == None:
                if request.get_full_path() == "/":
                    __root_url__ = request.build_absolute_uri()
                else:
                    __root_url__ = request.build_absolute_uri().replace(
                        request.get_full_path(), "")
                if __root_url__[__root_url__.__len__() - 1] == "/":
                    __root_url__ = __root_url__[0:__root_url__.__len__() - 1]
            return __root_url__

        def get_language():
            return language

        def get_view_path():
            ret = request.get_full_path().split("?")[0]
            if app.name == "default":
                if ret[0:1] == "/":
                    ret = ret[1:ret.__len__()]
                if ret=="":
                    return "index"
                else:
                    return ret
            else:
                if ret[0:1] == "/":
                    ret = ret[1:ret.__len__()]
                ret = ret[app.host.__len__():ret.__len__()]
                if ret[0:1] == "/":
                    ret = ret[1:ret.__len__()]
                if ret=="":
                    return "index"
                else:
                    return ret

        def get_app_name():
            return app.name

        def get_res(key, **caption):
            if caption == None:
                caption = key
                key = key.lower()
            lang_key = "language={};app={};view={};key={}".format(language, app.name,
                                                                  get_view_path(), key)
            ret_value = None
            if not _language_resource_cache.has_key(lang_key):

                with lock:
                    ret_value = _language_engine_module.get_language_item(language, app.name,
                                                                          get_view_path(), key, key)
                    _language_resource_cache.update({
                        lang_key: ret_value
                    })

            return _language_resource_cache[lang_key]

        def get_app_res(key, **caption):
            if caption == None:
                caption = key
                key = key.lower()
            lang_key = "language={};app={};view={};key={}".format(language, app.name, "_", key)
            ret_value = None
            if not _language_resource_cache.has_key(lang_key):

                with lock:
                    try:
                        ret_value = _language_engine_module.get_language_item(language, app.name,
                                                                              "_", key, key)
                        _language_resource_cache.update({
                            lang_key: ret_value
                        })
                    except Exception:
                        pass
            return _language_resource_cache[lang_key]

        def get_global_res(key, **caption):
            if caption == None:
                caption = key
                key = key.lower()
            lang_key = "language={};app={};view={};key={}".format(language, "_", "_", key)
            ret_value = None
            if not _language_resource_cache.has_key(lang_key):

                with lock:
                    try:
                        ret_value = _language_engine_module.get_language_item(language, "_",
                                                                              "_", key, key)
                        _language_resource_cache.update({
                            lang_key: ret_value
                        })
                    except Exception:
                        pass
            return _language_resource_cache[lang_key]

        def get_app_host():
            if app.name == "default":
                return ""
            else:
                return app.host

        def get_app_url(path):
            if app.name == "default":
                return get_abs_url() + (lambda :"" if path=="" else "/"+path)()
            else:
                return get_abs_url() + "/" + get_app_host() +  (lambda :"" if path=="" else "/"+path)()

        def get_static(path):
            return request.get_abs_url() + ("/" + app.client_static + "/" + path).replace("//","/")
        def encode_uri(uri):
            return urllib.quote(uri, safe='~()*!.\'')
        def decode_uri(encode_uri):
            return urllib.unquote(encode_uri)
        def get_raw_url():
            return request.build_absolute_uri(request.get_full_path())

        request.__dict__.update({"render": render})
        request.__dict__.update({"set_auth": set_auth})
        request.__dict__.update({"get_auth": get_auth})
        request.__dict__.update({"get_app_host": get_app_host})
        request.__dict__.update({"get_app_url": get_app_url})
        request.__dict__.update({"get_abs_url": get_abs_url})
        request.__dict__.update({"get_static": get_static})
        request.__dict__.update({"get_language": get_language})
        request.__dict__.update({"get_view_path": get_view_path})
        request.__dict__.update({"get_app_name": get_app_name})
        request.__dict__.update({"get_res": get_res})
        request.__dict__.update({"get_app_res": get_app_res})
        request.__dict__.update({"get_global_res": get_global_res})
        request.__dict__.update({"decode_uri": decode_uri})
        request.__dict__.update({"encode_uri": encode_uri})
        request.__dict__.update({"get_raw_url":get_raw_url})
        _url_login = ""
        if login_path!=None:
            if login_path[0:2] == "./":
                _url_login = app.host + "/" + login_path[2:login_path.__len__()]
            else:
                _url_login = app.host + "/" + login_path

        if request.path_info== "/"+_url_login:
            return fn(request,**kwargs)
        if auth_path != None and (not is_login_page or not is_public):
            _AUTH_ENGINE.register(app=app.name, id=get_view_path())
            path_to_auth_fn = auth_path.split(".")[auth_path.split(".").__len__() - 1]
            path_to_auth_mdl = auth_path[0: auth_path.__len__() - path_to_auth_fn.__len__() - 1]
            import importlib
            mdl=None
            try:
                mdl = importlib.import_module(path_to_auth_mdl)
            except Exception as ex:
                raise Exception("{0} was not found or error. Error message '{1}'\r\n"
                                ". See '{2}' at '{3}' \r\n"
                                "on file '{4}'".format(path_to_auth_mdl,ex.message,fn.__name__,fn.__module__,fn.func_code.co_filename))

            try:
                is_ok=getattr(mdl, path_to_auth_fn)(request)
                if is_ok:
                    fn(request,**kwargs)
                else:

                    url_next=request.get_abs_url()+"/"+_url_login+"?next="+request.encode_uri(request.get_raw_url())
                    return redirect(url_next)
            except Exception as ex:
                raise Exception("Error '{0}' at '{1}' in file '{2}'".format(ex.message,mdl.__name__,mdl.__file__))



        view_info=get_settings().AUTH_ENGINE.get_view_info(app=app.name,id=get_view_path())
        if view_info==None:
            return fn(request,**kwargs)
        elif view_info["is_public"]:
            return fn(request, **kwargs)
        else:

            _login_info=membership.validate_session(request.session.session_key)
            if _login_info==None:
                return HttpResponse('Unauthorized', status=401)
            elif _login_info.user.isSysAdmin:
                return fn(request, **kwargs)
            else:
                privileges=_AUTH_ENGINE.get_view_of_user(user_id=_login_info.user.userId,view_id=view_info["id"])
                if privileges==None:
                    if _login_info.user.isSysAdmin:
                        privileges={
                            "is_public":True
                        }
                        return fn(request, **kwargs)
                    else:
                        return HttpResponse('Unauthorized', status=401)
                else:
                    return fn(request, **kwargs)









    return exec_request




def get_settings():
    return sys.modules["settings"]
