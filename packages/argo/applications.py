import importlib
import sys
import os
from . import app_info
_app_cache={}
__cache_find_path={}
def get_app(path):
    global _app_cache
    if not _app_cache.has_key(path):
        _app_cache.update({
            path:app_info.app_config(path)
        })
    return _app_cache[path]
def get_app_by_file(file_name):
    """get application info by path of file
    if path of file is in application package"""
    global __cache_find_path
    if __cache_find_path.has_key(file_name):
        return __cache_find_path[file_name]


    _path=os.path.dirname(file_name)
    _dir=_path.replace("\\","/").replace("//","/")
    matched_app=None
    if _app_cache.has_key(_dir):
        matched_app=_app_cache[_dir]
    if matched_app==None:
        for key in _app_cache.keys():
            if key in _dir:
                matched_app=_app_cache[key]
    __cache_find_path.update({file_name:matched_app})
    return __cache_find_path[file_name]
def get_urls(app):
    app_config=get_app(app["path"])
    urls=app_config.get_urls()
    return urls
