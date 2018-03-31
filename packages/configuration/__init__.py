import utilities
import imp
import sys
import os
from django.conf.urls import url, include
import importlib
import  re
from django.core.wsgi import get_wsgi_application
from django.conf.urls.static import static
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
        paths = _dict.get("ROUTES")
        _urls = get_routes_from_config(paths)
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
def get_routes_from_config(paths):
    ret=[]
    for p in paths:
        data=utilities.load_json_config_file(p)
        sys.path.append(utilities.get_host_directory()+data.get("VIEWS").get("path"))
        importlib.import_module(data.get("VIEWS").get("name"))
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




