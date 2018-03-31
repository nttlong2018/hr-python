import utilities
import imp
import sys
import os
from django.conf.urls import url, include
import importlib
import  re
from django.core.wsgi import get_wsgi_application
from django.conf.urls.static import static
app_info={}
app_info_dir={}
__cache_find_path={}
__cache_find_name={}
__paths__=[]
def load_settings(name):
    "Load setting from json file"
    global _default_settings
    ret_module = imp.new_module(name)
    _dict=utilities.load_json_config_file(name)
    "if use sqlite3, resolve "
    if(_dict.has_key("SQLITE3")):
        if(not _dict.has_key("DATABASES")):
            _dict.update({"DATABASES":{}})
        if(not _dict.get("DATABASES").has_key("default")):
            _dict.get("DATABASES").update({"default":{
                "ENGINE": "",
                "NAME": ""
            }})
        _DATABASES=_dict.get("DATABASES").get("default")
        _DATABASES.update({"ENGINE":"django.db.backends.sqlite3"})
        _DATABASES.update({"NAME": utilities.get_host_directory()+"/database/"+_dict.get("SQLITE3")})
    _static_dirs=_dict.get("STATICFILES_DIRS")
    template_dir=_dict.get("TEMPLATES_DIRS")
    _STATIC_ROOT=_dict.get("STATIC_ROOT")
    _dict.update({"STATIC_ROOT":utilities.get_host_directory()+"/"+_STATIC_ROOT})
    _staticDirs=[];
    for x in _static_dirs:
        _staticDirs.append((utilities.get_host_directory()+"/"+ x).replace("\\","/"))
    _dict.update({"STATICFILES_DIRS":_staticDirs})
    _dict.update({"WSGI_APPLICATION":name+".wsgi.application"})
    dirs=[]
    for x in template_dir:
        dirs.append((utilities.get_host_directory()+"/"+ x).replace("\\","/"))
    _dict.get("TEMPLATES")[0].update({"DIRS":dirs})
    for  key in _dict.keys():
        setattr(ret_module,key,_dict.get(key))
    # setattr(ret_module, "_appliction", get_wsgi_application())
    if not _dict.has_key("ROOT_URLCONF"):
        url_module=imp.new_module(name+"_urls")
        setattr(ret_module, "ROOT_URLCONF", name+"_urls")

    sys.modules.update({
        name:ret_module
    })

    ret_wsgi=imp.new_module(name+".wsgi")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", name)
    setattr(ret_wsgi, "application", get_wsgi_application())
    sys.modules.update({
        ret_wsgi.__name__: ret_wsgi
    })
    _default_settings=_dict
    if(_dict.has_key("MEMBERSHIP_PROVIDER")):
        import membership
        membership.set_provider(_dict.get("MEMBERSHIP_PROVIDER").get("NAME"))
        membership.set_config(_dict.get("MEMBERSHIP_PROVIDER").get("config"))

    if not _dict.has_key("ROOT_URLCONF"):
        paths = _dict.get("APPS")
        _urls = load_app_config(paths)
        buil_urls(url_module, _urls, _dict.get("STATIC_URL"), _dict.get("STATIC_ROOT"))
        sys.modules.update({
            name + "_urls": url_module
        })
    return ret_module
def get_static_dirs():
    return  _default_settings.get("STATICFILES_DIRS")
def get_static_url():
    return _default_settings.get("STATIC_URL")
def get_static_root():
    return _default_settings.get("STATIC_ROOT")
def get_app_info(file_name):
    global __cache_find_path
    if __cache_find_path.has_key(file_name):
        return __cache_find_path[file_name]

    import  os
    _path=os.path.dirname(file_name)
    _dir=_path.replace("\\","/").replace("//","/")
    matched_app=None
    if app_info_dir.has_key(_dir):
        matched_app=app_info_dir[_dir]
    if matched_app==None:
        for key in app_info_dir.keys():
            if key in _dir:
                matched_app=app_info_dir[key]
    __cache_find_path.update({file_name:matched_app})
    return __cache_find_path[file_name]
def load_app_config(paths):
    """
    Load all application info according to 'paths'
    'paths' is a list of application directory
    """
    ret=[]
    global  app_info
    global  app_info_dir
    global  __paths__
    global __cache_find_name
    for p in paths:
        data=utilities.load_json_from_file(p+"/config")
        app_info.update({data.get("NAME"): data})

        _dir=(utilities.get_host_directory()+"/"+p).replace("\\","/").replace("//","/")
        __paths__.append(_dir)
        app_info_dir.update({_dir:data})

        sys.path.append(utilities.get_host_directory()+"/"+p)
        module=importlib.import_module(data.get("VIEWS").get("name"))
        __cache_find_name.update({module.__name__:data})
        for route in data.get("ROUTES"):
            ret+=[{
                "url":route.get("url"),
                "view":data.get("VIEWS").get("name")+"."+route.get("view"),
                "name":route.get("name")
            }]
    return  ret
def buil_urls(mdl,urls,static_url,static_root):

    urlpatterns=static(static_url, document_root=static_root)+[]
    for route in urls:
        urlpatterns+=[
            url(route.get("url"), route.get("view"), name=route.get("name"))

        ]

    setattr(mdl,"urlpatterns",urlpatterns)




