from . import app_info
import os
import sys
import logging
logger=logging.getLogger(__name__)
_cache_apps={}
__cache_find_path={}
_settings=None
def load_app(*args,**kwargs):
    global _cache_apps
    try:
        if not _cache_apps.has_key(args[0]["path"]):
            _cache_apps.update({
                args[0]["path"]:app_info.app_config(args)
            })
        return _cache_apps[args[0]["path"]]

    except Exception as ex:
        logger.debug(ex)
        logger.debug("quicky.applications.load_app error {0} in '{1}'".format(ex,args[0]["path"]))
        raise (Exception("quicky.applications.load_app error in '{1}'.\n Detail information is:\n\t\t ""{0}"" ".format(ex,args[0]["path"])))

def get_app_by_file(file_name):
    """get application info by path of file
    if path of file is in application package"""
    global __cache_find_path
    if __cache_find_path.has_key(file_name):
        return __cache_find_path[file_name]


    _path=os.path.dirname(file_name)
    _dir=_path.replace("\\","/").replace("//","/")
    matched_app=None
    if _cache_apps.has_key(_dir):
        matched_app=_cache_apps[_dir]
    if matched_app==None:
        for key in _cache_apps.keys():
            if key in _dir:
                matched_app=_cache_apps[key]
    __cache_find_path.update({file_name:matched_app})
    return __cache_find_path[file_name]
def get_app_by_name(app_name):
    for key in _cache_apps.keys():
        if _cache_apps[key].name.lower()==app_name.lower():
            return _cache_apps[key]
def get_settings():
    global _settings
    if _settings==None:
        _settings = sys.modules.get("settings")
        STATIC_URL = getattr(_settings, "STATIC_URL")
        if STATIC_URL == None:
            setattr(_settings, "STATIC_URL", "/static/")
    return _settings