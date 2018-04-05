import  os
import json
from pathlib import Path
import sys
from django.http import HttpResponse
from mako.template import Template
from mako.lookup import TemplateLookup
import config

import importlib
import threading
_host_directory=None
_utilities_json_config_cache=dict()
_language_engine_module=None
_language_resource_cache={}
import logging

logger = logging.getLogger(__name__)

def get_host_directory():
    "get host directory"
    global _host_directory
    if _host_directory==None:
        _host_directory=os.getcwd()
    return  _host_directory
def load_json_from_file(file_name):
    with open(get_host_directory() + "/" + file_name + ".json") as json_file:
        return json.load(json_file)

def load_json_config_file(fileName):
    global _utilities_json_config_cache

    if _utilities_json_config_cache==None:
        _utilities_json_config_cache={}
    if not _utilities_json_config_cache.has_key(fileName):
        with open(get_host_directory()+"/configs/"+fileName+".json") as json_file:
            _utilities_json_config_cache.update({fileName:json.load(json_file)})
    return  _utilities_json_config_cache.get(fileName)
def render(render_config):
    global _language_engine_module
    global _language_resource_cache
    if _language_engine_module==None:
        _language_engine_module=build_language_engine(config.get_default_language_engine())

    from django.core.context_processors import csrf
    http_request=render_config["request"]

    language=render_config["language"]
    fileName=render_config["file"]
    model=render_config.get("model",{})
    def get_view_path():
        ret=http_request.get_full_path()
        if render_config["app_name"]=="default":
            if ret[0:1]=="/":
                ret=ret[1:ret.__len__()]
            return ret
        else:
            if ret[0:1]=="/":
                ret=ret[1:ret.__len__()]
            ret=ret[render_config["host"].__len__():ret.__len__()]
            if ret[0:1]=="/":
                ret=ret[1:ret.__len__()]
            return  ret
    def get_app_name():
        return render_config["app_name"]
    def get_language():
        return render_config["language"]


    def get_res(key,**caption):
        if caption==None:
            caption=key
            key=key.lower()
        lang_key="language={};app={};view={};key={}".format(language,render_config["app_name"],get_view_path(),key)
        ret_value=None
        if not _language_resource_cache.has_key(lang_key):
            lock = threading.Lock()
            with lock:
                ret_value=_language_engine_module.get_language_item(language,render_config["app_name"],get_view_path(),key,key)
                _language_resource_cache.update({
                    lang_key:ret_value
                    })

        return  _language_resource_cache[lang_key]
    def get_app_res(key,**caption):
        if caption == None:
            caption = key
            key = key.lower()
        lang_key = "language={};app={};view={};key={}".format(language, render_config["app_name"], "_", key)
        ret_value = None
        if not _language_resource_cache.has_key(lang_key):
            lock = threading.Lock()
            with lock:
                try:
                    ret_value = _language_engine_module.get_language_item(language, render_config["app_name"],
                                                                          "_", key, key)
                    _language_resource_cache.update({
                        lang_key: ret_value
                    })
                except Exception:
                    pass
        return _language_resource_cache[lang_key]
    def get_global_res(key,**caption):
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
    def get_abs_url():
        return render_config["request"].build_absolute_uri().replace(render_config["request"].get_full_path(),"")

    def get_static(path):
        return render_config["request"].build_absolute_uri().replace(render_config["request"].get_full_path(),"") +"/"+render_config["static"]+path
    def get_csrftoken():
        return  csrf(http_request)["csrf_token"]
    try:


        render_model={
            "get_res":get_res,
            "get_app_res":get_app_res,
            "get_global_res":get_global_res,
            "get_static":get_static,
            "get_abs_url":get_abs_url,
            "get_csrftoken":get_csrftoken,
            "model":model,
            "get_view_path":get_view_path
        }

        # mylookup = TemplateLookup(directories=config._default_settings["TEMPLATES_DIRS"])
        if fileName!=None:
            mylookup = TemplateLookup(directories=["apps/" + render_config["templates"]])
            return HttpResponse(mylookup.get_template(fileName).render(**render_model))
        else:
            mylookup = TemplateLookup(directories=["apps/" + render_config["templates"]])
            return HttpResponse(mylookup.get_template(http_request.__dict__["template_file"]).render(**render_model))
    except Exception as ex:
        logger.error(ex)
        return HttpResponse(ex.message)

def build_language_engine(config):
    mdl=importlib.import_module(config["NAME"])
    mdl.load(config["CONFIG"])
    return  mdl;

