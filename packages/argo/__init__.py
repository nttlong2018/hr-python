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
__root_url__=None
lock = threading.Lock()
logger = logging.getLogger(__name__)
__session_cache__={}
_language_resource_cache={}
_settings=None
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
        app = applications.get_app_by_file(fn.func_code.co_filename)
        if app.on_begin_request!=None and callable(app.on_begin_request):
            app.on_begin_request(request)

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

        setattr(request,"application",app)
        if auth_path==None:
            auth_path=app.authenticate
        if login_path==None:
            login_path=app.login
        def set_auth(*args,**kwargs):
            global __session_cache__
            data=kwargs
            if type(args) is tuple:
                if args.__len__()>0:
                    data=args[0]


            if not data.has_key("user"):
                raise Exception("Please set 'user' info {id:string,username:string}")
            __session_cache__.update({
                request.session._get_session_key(): data
            })
            request.session["authenticate"] = data
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
                "application": app,
                "get_user":request.get_user

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
                ret = ret[app.host_dir.__len__():ret.__len__()]
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
                    ret_value =  get_settings().LANGUAGE_ENGINE.get_language_item(language, app.name,
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
                        ret_value =  get_settings().LANGUAGE_ENGINE.get_language_item(language, app.name,
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
                        ret_value = get_settings().LANGUAGE_ENGINE.get_language_item(language, "_",
                                                                              "_", key, key)
                        _language_resource_cache.update({
                            lang_key: ret_value
                        })
                    except Exception as ex:
                        raise("'get_global_res' error {0}".format(ex))
                        pass
            return _language_resource_cache[lang_key]
        def get_app_host():
            if app.name == "default":
                return ""
            else:
                return app.host_dir
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
        def get_user():
            if not request.session.has_key("authenticate"):
                return None
            return request.session["authenticate"].get("user",None)

        setattr(request,"render", render)
        setattr(request,"set_auth", set_auth)
        setattr(request,"get_auth", get_auth)
        setattr(request,"get_app_host",get_app_host)
        setattr(request,"get_app_url", get_app_url)
        setattr(request,"get_abs_url", get_abs_url)
        setattr(request,"get_static",get_static)
        setattr(request,"get_language", get_language)
        setattr(request,"get_view_path",get_view_path)
        setattr(request,"get_app_name", get_app_name)
        setattr(request,"get_res",get_res)
        setattr(request,"get_app_res", get_app_res)
        setattr(request,"get_global_res", get_global_res)
        setattr(request,"decode_uri", decode_uri)
        setattr(request,"encode_uri",encode_uri)
        setattr(request,"get_raw_url",get_raw_url)
        setattr(request, "get_user", get_user)
        _url_login = ""
        if login_path!=None:
            if login_path[0:2] == "./":
                _url_login = get_abs_url() + "/" + login_path[2:login_path.__len__()]
            else:
                _url_login = app.host + "/" + login_path

        if request.path_info== "/"+_url_login:
            if app.on_end_request != None and callable(app.on_end_request):
                res=app.on_end_request(request)
                if res!=None:
                    return res
            return fn(request,**kwargs)
        fn_on_authenticate=None
        _url_login = "login"
        if hasattr(app.settings, "login"):
            _url_login = getattr(app.settings, "login")
        if _url_login[0:2] == "~/":
            _url_login = _url_login[2:_url_login.__len__()]
        else:
            _url_login = app.host_dir + "/" + _url_login
        _url_login="/"+_url_login
        is_login_page=request.path_info.lower()==_url_login.lower()
        if app.authenticate != None and (not is_login_page and not is_public):
            authorization.register(app=app.name, id=get_view_path())
            if type(app.authenticate) is str:
                path_to_auth_fn = app.authenticate.split(".")[app.authenticate.split(".").__len__() - 1]
                path_to_auth_mdl = app.authenticate[0: app.authenticate.__len__() - path_to_auth_fn.__len__() - 1]
                import importlib
                mdl=None
                try:
                    mdl = importlib.import_module(path_to_auth_mdl)
                except Exception as ex:
                    raise Exception("{0} was not found or error. Error message '{1}'\r\n"
                                ". See '{2}' at '{3}' \r\n"
                                "on file '{4}'".format(path_to_auth_mdl,ex.message,fn.__name__,fn.__module__,fn.func_code.co_filename))
                try:
                    if hasattr(mdl,path_to_auth_fn):
                        fn_on_authenticate=getattr(mdl, path_to_auth_fn)
                        if not callable(fn_on_authenticate):
                            raise (Exception("'{0}' in '{1}' must be a function".format(path_to_auth_fn, path_to_auth_fn)))
                    else:
                        raise(Exception("'{0}' was noy found in '{1}'".format(path_to_auth_fn,path_to_auth_fn)))
                except Exception as ex:
                    raise Exception("Error '{0}' at '{1}' in file '{2}'".format(ex.message,mdl.__name__,mdl.__file__))
            elif callable(app.authenticate):
                fn_on_authenticate=app.authenticate

        if fn_on_authenticate!=None:
                is_ok=fn_on_authenticate(request)
                if is_ok:
                    if app.on_end_request != None and callable(app.on_end_request):
                        res = app.on_end_request(request)
                        if res != None:
                            return res
                    ret= fn(request, **kwargs)
                    return ret
                else:
                    url_next = request.get_abs_url()  +\
                               _url_login + "?next=" +\
                               request.encode_uri(request.get_raw_url())
                    return redirect(url_next)
        elif is_login_page:
            if app.on_end_request != None and callable(app.on_end_request):
                res=app.on_end_request(request)
                if res!=None:
                    return res
            return fn(request, **kwargs)
        elif is_public:
            if app.on_end_request != None and callable(app.on_end_request):
                res=app.on_end_request(request)
                if res!=None:
                    return res
            return fn(request, **kwargs)
        else:
            view_info=authorization.get_view_info(
                app=app.name,
                id=get_view_path())

            if view_info==None:
                if app.on_end_request != None and callable(app.on_end_request):
                    res = app.on_end_request(request)
                    if res != None:
                        return res
                return fn(request,**kwargs)
            elif view_info["is_public"]:
                return fn(request, **kwargs)
            else:
                _login_info=membership.validate_session(request.session.session_key)
                if _login_info==None:
                    if app.on_end_request != None and callable(app.on_end_request):
                        res = app.on_end_request(request)
                        if res != None:
                            return res
                    return HttpResponse('Unauthorized', status=401)
                elif _login_info.user.isSysAdmin:
                    return fn(request, **kwargs)
                else:
                    privileges=authorization.get_view_of_user(user_id=_login_info.user.userId,view_id=view_info["id"])
                    if privileges==None:
                        if _login_info.user.isSysAdmin:
                            privileges={
                                "is_public":True
                            }
                            if app.on_end_request != None and callable(app.on_end_request):
                                res = app.on_end_request(request)
                                if res != None:
                                    return res
                            return fn(request, **kwargs)
                        else:
                            if app.on_end_request != None and callable(app.on_end_request):
                                res = app.on_end_request(request)
                                if res != None:
                                    return res
                            return HttpResponse('Unauthorized', status=401)
                    else:
                        if app.on_end_request != None and callable(app.on_end_request):
                            res = app.on_end_request(request)
                            if res != None:
                                return res
                        return fn(request, **kwargs)
    return exec_request




def get_settings():
    global _settings
    if _settings==None:
        _settings = sys.modules.get("settings")
        STATIC_URL = getattr(_settings, "STATIC_URL")
        if STATIC_URL == None:
            setattr(_settings, "STATIC_URL", "/static/")
    return _settings
