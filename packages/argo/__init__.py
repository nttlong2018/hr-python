from . import config
from . import utilities as utils
from . import models
from django.shortcuts import redirect
import membership
import threading
import importlib
import logging
logger = logging.getLogger(__name__)
__cache_app__={}
__cache_app__by_module_name__={}
__session_cache__={}
__root_url__=None
_language_engine_module=None
_language_resource_cache={}
def get_application_by_module_name(module_name):
    try:
        global __cache_app__by_module_name__
        if not __cache_app__by_module_name__.has_key(module_name):
            ret_data = models.app_info()
            app=config.get_app_info_by_name(module_name)
            ret_data.name = app["NAME"]
            ret_data.template_dir = app["DIR"] + "/templates"
            ret_data.client_static = "default/static/"
            ret_data.host = app["HOST"]
            if ret_data.name != "default":
                ret_data.client_static = ret_data.host + "/static/"
            __cache_app__by_module_name__.update({
                file: ret_data
            })
        return __cache_app__by_module_name__[file]
    except Exception as ex:
        logger.error(ex)
        raise Exception("Error in {0} with {1}".format(module_name,ex.message))

def get_application(file):
    global __cache_app__
    global __cache_app__by_module_name__
    if not __cache_app__.has_key(file):
        ret_data=models.app_info()
        __cache_app__by_module_name__[config.get_app_info(file)["MODULE"].__name__]=ret_data
        ret_data.name=config.get_app_info(file)["NAME"]
        ret_data.template_dir=config.get_app_info(file)["DIR"]+"/templates"
        ret_data.client_static="default/static/"
        ret_data.host=config.get_app_info(file)["HOST"]
        if ret_data.name!="default":
            ret_data.client_static = ret_data.host+"/static/"
        __cache_app__.update({
            file:ret_data
        })
    return __cache_app__[file]
def template_uri(fn):
    def layer(*args, **kwargs):
        def repl(f):
            return fn(f,*args, **kwargs)
        return repl
    return layer
@template_uri
def template(fn,_path):
    fn.__dict__.update({"__params__": _path})
    def exec_request(request):
        file_path=fn.__dict__["__params__"]
        auth_path = None
        login_path = None
        if type(file_path) is dict:
            auth_path = file_path.get("auth", None)
            login_path = file_path.get("login", None)
            file_path = file_path.get("file", "")
            if login_path == None and auth_path != None:
                raise Exception("'auth' require 'login'. 'login' need to be set at '" + fn.__name__ + "'")

        global _language_engine_module
        global _language_resource_cache
        if _language_engine_module == None:
            _language_engine_module = build_language_engine(config.get_default_language_engine())

        language = "en"
        if request.session.has_key("language"):
            language = request.session["language"]

        app = get_application(fn.func_code.co_filename)

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
            ret = request.get_full_path()
            if app.name == "default":
                if ret[0:1] == "/":
                    ret = ret[1:ret.__len__()]
                return ret
            else:
                if ret[0:1] == "/":
                    ret = ret[1:ret.__len__()]
                ret = ret[app.host.__len__():ret.__len__()]
                if ret[0:1] == "/":
                    ret = ret[1:ret.__len__()]
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
                lock = threading.Lock()
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
                lock = threading.Lock()
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
                lock = threading.Lock()
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
                return get_abs_url() + "/" + path
            else:
                return get_abs_url() + "/" + get_app_host() + "/" + path

        def get_static(path):
            return request.get_abs_url() + "/" + app.client_static + "/" + path

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
        if auth_path != None:
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
                    fn(request)
                else:
                    redirect(login_path)
            except Exception as ex:
                raise Exception("Error '{0}' at '{1}' in file '{2}'".format(ex.message,mdl.__name__,mdl.__file__))

        return fn(request)

    return exec_request



def build_language_engine(config):
    try:
        if not config.has_key("NAME"):
            logger.error("Language module was not install as config.json")
            raise Exception("Language module was not install as config.json")

        mdl=importlib.import_module(config["NAME"])
        mdl.load(config["CONFIG"])
        return  mdl
    except Exception as ex:
        logger.error(ex)
        raise Exception("Error in {0} with '{1}'".format(config.get("NAME",""),ex.message))
def auth(_url):
    def authdecorator(fn):
        print (_url)