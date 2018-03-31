_host_directory=None
_utilities_json_config_cache=dict()
import  os
import json
from pathlib import  Path
import sys
from django.http import HttpResponse
from . import models
import logging
logger = logging.getLogger(__name__)

def get_host_directory():
    "get host directory"
    global _host_directory
    if _host_directory==None:
        _host_directory=os.path.dirname(sys.modules['__main__'].__file__)
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
def render(http_request,app,language,fileName,model):
    def get_res(key,**caption):
        return  fileName
    def get_app_res(key,**caption):
        return key
    def get_global_res(key,**caption):
        return key
    try:
        from mako.template import Template
        from mako.lookup import TemplateLookup
        import configuration
        render_model={
            "get_res":get_res,
            "get_app_res":get_app_res,
            "get_global_res":get_global_res
        }

        mylookup = TemplateLookup(directories=configuration._default_settings["TEMPLATES_DIRS"])
        return HttpResponse(mylookup.get_template(fileName).render(**render_model))
    except Exception as ex:
        logger.error(ex)
        return HttpResponse(ex.message)


