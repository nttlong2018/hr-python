_host_directory=None
_utilities_json_config_cache=dict()
import  os
import json
from pathlib import  Path
import sys
from django.http import HttpResponse
def get_host_directory():
    "get host directory"
    global _host_directory
    if _host_directory==None:
        _host_directory=os.path.dirname(sys.modules['__main__'].__file__)
    return  _host_directory
def load_json_config_file(fileName):
    global _utilities_json_config_cache
    if _utilities_json_config_cache==None:
        _utilities_json_config_cache={}
    if not _utilities_json_config_cache.has_key(fileName):
        with open(get_host_directory()+"/configs/"+fileName+".json") as json_file:
            _utilities_json_config_cache.update({fileName:json.load(json_file)})
    return  _utilities_json_config_cache.get(fileName)
def render(fileName,model):
    try:
        from mako.template import Template
        from mako.lookup import TemplateLookup
        import configuration
        mylookup = TemplateLookup(directories=configuration._default_settings["TEMPLATES_DIRS"])
        return HttpResponse(mylookup.get_template(fileName).render(**model))
    except Exception as ex:
        return HttpResponse(ex.message)

def model(**data):
    data["res"]=get_res
def get_res(key):
    return "hello :"+key
