import  os
import json
import applications

import sys
from django.http import HttpResponse
from mako.template import Template
from mako.lookup import TemplateLookup
from . import language as lang_manager
import threading
import logging
logger=logging.getLogger(__name__)
global lock
lock=threading.Lock()
from datetime import date, datetime

from bson.objectid import ObjectId
import importlib
from . import applications
_language_cache={}
class render_server():
    def __init__(self):
        pass
def get_language_item(language,app_name,view,key,value):
    global _language_cache
    hash_key="language={0};app={1};view={2};key={3}".format(language,app_name,view,key).lower()
    if not _language_cache.has_key(hash_key):
        try:
            lock.acquire()
            ret=lang_manager.get_language_item(language,app_name,view,key,value)
            _language_cache[hash_key]=ret
            lock.release()
        except Exception as ex:
            lock.release()
            raise ex
    return _language_cache[hash_key]
def apply(request,template_file,app):
    import api
    from django.core.context_processors import csrf
    def get_language():
        if hasattr(request,"request.LANGUAGE_CODE"):
            return request.LANGUAGE_CODE
        else:
            from django.utils import translation
            return translation.get_language()


    def get_app_url(path):
        if app.name == "default" or get_app_host()=="":
            return get_abs_url() + (lambda: "" if path == "" else "/" + path)()
        else:
            return (get_abs_url() + "/" + get_app_host() + (lambda: "" if path == "" else "/" + path)())

    def get_app_host():
        if app.name == "default":
            return ""
        else:
            return app.host_dir
    def get_view_path():
        ret = request.get_full_path().split("?")[0]
        if app.name == "default":
            if ret[0:1] == "/":
                ret = ret[1:ret.__len__()]
            if ret == "":
                return "index"
            else:
                return ret
        else:
            if ret[0:1] == "/":
                ret = ret[1:ret.__len__()]
            ret = ret[app.host_dir.__len__():ret.__len__()]
            if ret[0:1] == "/":
                ret = ret[1:ret.__len__()]
            if ret == "":
                return "index"
            else:
                return ret
    def get_user():
        return request.user
    def get_res(key):
        return get_language_item(get_language(),app.name,get_view_path(),key,key)
    def get_app_res(key):
        return get_language_item(get_language(), app.name, "-", key, key)
    def get_global_res(key):
        return get_language_item(get_language(), "-", "-", key, key)
    def get_static(path):
        if app.host_dir=="":
            return get_abs_url()+"/"+app.name+"/static/"+path
            # return request.get_app_url(app.name+"/static")+"/"+path
        else:
            return request.get_app_url("static")+"/"+path
    def get_abs_url():
        __root_url__= None

        if request.get_full_path() == "/":
            __root_url__ = request.build_absolute_uri()
        else:
            __root_url__ = request.build_absolute_uri().replace(
                request.get_full_path(), "")
        if __root_url__[__root_url__.__len__() - 1] == "/":
            __root_url__ = __root_url__[0:__root_url__.__len__() - 1]
        return __root_url__
    def get_app():
        return app
    def get_app_name():
        return app.name
    def get_api_key(path):
        return api.get_api_key(path)
    def get_api_path(id):
        return api.get_api_path(id)
    def register_view():
        return applications.get_settings().AUTHORIZATION_ENGINE.register_view(app=get_app_name(),view=get_view_path())

    def render(model):
        from mako import exceptions
        login_page=None
        is_public=None
        if type(template_file) is dict:
            fileName=template_file["file"]
            login_page=template_file.get("login",None)
            is_public = template_file.get("is_public", False)
        else:
            fileName = template_file
        def get_csrftoken():
            if type(csrf(request)["csrf_token"]) is str:
                return csrf(request)["csrf_token"]
            else:
                return csrf(request)["csrf_token"].encode()

        render_model = {
            "get_res": get_res,
            "get_app_res": get_app_res,
            "get_global_res": get_global_res,
            "get_static": get_static,
            "get_abs_url": get_abs_url,
            "get_csrftoken": get_csrftoken,
            "model": model,
            "get_view_path": get_view_path,
            "get_user": get_user,
            "get_app_url": get_app_url,
            "get_app_host": get_app_host,
            "get_static": get_static,
            "get_language": get_language,
            "template_file": template_file,
            "get_api_key":get_api_key,
            "get_api_path":get_api_path,
            "register_view":register_view,
            "request":request
        }
        # mylookup = TemplateLookup(directories=config._default_settings["TEMPLATES_DIRS"])
        if fileName != None:
            ret_res=None
            mylookup = TemplateLookup(directories=[os.getcwd() + "/" + request.get_app().template_dir],
                                      default_filters=['decode.utf8'],
                                      input_encoding='utf-8',
                                      output_encoding='utf-8',
                                      encoding_errors='replace'
                                      )
            try:
                ret_res=mylookup.get_template(fileName).render(**render_model)

            except exceptions.MakoException as ex:
                logger.debug(ex)
                raise (ex)
            except Exception as ex:
                logger.debug(exceptions.html_error_template().render())
                raise (Exception(exceptions.html_error_template().render()))
            return HttpResponse(ret_res)


        else:
            mylookup = TemplateLookup(directories=["apps/templates"],
                                      default_filters=['decode.utf8'],
                                      input_encoding='utf-8',
                                      output_encoding='utf-8',
                                      encoding_errors='replace'
                                      )
            return HttpResponse(mylookup.get_template(fileName).render(**render_model))


    setattr(request,"template_file",template_file)
    setattr(request, "render", render)
    setattr(request, "get_user", get_user)
    setattr(request, "get_res", get_res)
    setattr(request, "get_app_res", get_app_res)
    setattr(request, "get_global_res", get_global_res)
    setattr(request, "get_static", get_static)
    setattr(request, "get_abs_url", get_abs_url)
    setattr(request, "get_app", get_app)
    setattr(request,"get_view_path",get_view_path)
    setattr(request,"get_app_host",get_app_host)
    setattr(request, "get_app_url", get_app_url)
    setattr(request,"get_language",get_language)
    setattr(request, "get_app_name", get_app_name)
    setattr(request, "get_api_key", get_api_key)
    setattr(request, "get_api_path", get_api_path)
    setattr(request,"register_view",register_view)




