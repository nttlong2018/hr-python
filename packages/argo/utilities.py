import  os
import json
from pathlib import Path
import sys
from django.http import HttpResponse
from mako.template import Template
from mako.lookup import TemplateLookup
import config
from datetime import date, datetime
import sqlalchemy
from bson.objectid import ObjectId
import importlib

_host_directory=None
_utilities_json_config_cache=dict()
_language_engine_module=None
_language_resource_cache={}
_root_url=None
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

    from django.core.context_processors import csrf
    http_request=render_config["request"]


    fileName=render_config["file"]
    model=render_config.get("model",{})




    def get_csrftoken():
        return  csrf(http_request)["csrf_token"]
    def get_user():
        if http_request.session.has_key('authenticate'):
            if http_request.session['authenticate'].has_key("user"):
                if http_request.session['authenticate']["user"]!=None:
                    return http_request.session['authenticate']["user"]
        return {}

    render_model={
            "get_res":http_request.get_res,
            "get_app_res":http_request.get_app_res,
            "get_global_res":http_request.get_global_res,
            "get_static":http_request.get_static,
            "get_abs_url":http_request.get_abs_url,
            "get_csrftoken":get_csrftoken,
            "model":model,
            "get_view_path":http_request.get_view_path,
            "get_user":get_user,
            "get_app_url":http_request.get_app_url,
            "get_app_host":http_request.get_app_host,
            "get_static":http_request.get_static,
            "get_language":http_request.get_language
        }
    # mylookup = TemplateLookup(directories=config._default_settings["TEMPLATES_DIRS"])
    if fileName!=None:
            mylookup = TemplateLookup(directories=[http_request.application.template_dir],
                                      default_filters=['decode.utf8'],
                                      input_encoding='utf-8',
                                      output_encoding='utf-8',
                                      encoding_errors='replace'
                                      )
            return HttpResponse(mylookup.get_template(fileName).render(**render_model))
    else:
        mylookup = TemplateLookup(directories=["apps/" + render_config["templates"]],
                                  default_filters=['decode.utf8'],
                                  input_encoding='utf-8',
                                  output_encoding='utf-8',
                                  encoding_errors='replace'
                                  )
        return HttpResponse(mylookup.get_template(http_request.__dict__["template_file"]).render(**render_model))
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif type(obj) is ObjectId:
        return obj.__str__()
    elif type(obj) is sqlalchemy.orm.state.InstanceState:
        return  None
    return obj.__str__()
def to_json(ret):
    if type(ret) is list:
        if ret.__len__()==0:
            ret_data="[]"
        else:


            if type(ret[0]) is dict:
                ret_data=json.dumps(ret,default=json_serial)
            else:
                ret_data=json.dumps([r.__dict__ for r in ret],default=json_serial)
    else:
        if ret==None:
            ret_data=None
        else:
            if type(ret) is dict:
                ret_data = json.dumps(ret, default=json_serial)
            else:
                ret_data = json.dumps(ret.__dict__, default=json_serial)
    return ret_data

