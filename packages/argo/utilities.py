import  os
import json
from pathlib import  Path
import sys
from django.http import HttpResponse
from mako.template import Template
from mako.lookup import TemplateLookup
import config
_host_directory=None
_utilities_json_config_cache=dict()
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
def render(render_config):
    http_request=render_config["request"]

    language=render_config["language"]
    fileName=render_config["file"]
    model=render_config["model"]
    def get_res(key,**caption):
        return  fileName
    def get_app_res(key,**caption):
        return key
    def get_global_res(key,**caption):
        return key
    def get_abs_url():
        return render_config["request"].build_absolute_uri().replace(render_config["request"].get_full_path(),"")

    def get_static(path):
        return render_config["request"].build_absolute_uri().replace(render_config["request"].get_full_path(),"") +"/"+render_config["static"]+path
    try:


        render_model={
            "get_res":get_res,
            "get_app_res":get_app_res,
            "get_global_res":get_global_res,
            "get_static":get_static,
            "get_abs_url":get_abs_url,
            "model":render_config["model"]
        }

        # mylookup = TemplateLookup(directories=config._default_settings["TEMPLATES_DIRS"])
        mylookup = TemplateLookup(directories=["apps/" + render_config["templates"]])
        return HttpResponse(mylookup.get_template(fileName).render(**render_model))
    except Exception as ex:
        logger.error(ex)
        return HttpResponse(ex.message)



