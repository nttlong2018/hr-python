from . import utilities
import imp
import sys
import os
from django.conf.urls import url, include
import importlib
import  re
from django.core.wsgi import get_wsgi_application
from django.conf.urls.static import static
import logging
logger = logging.getLogger(__name__)
app_info={}
app_info_dir={}
__cache_find_path={}
__cache_find_name={}
__paths__=[]
def load_settings(name):
    "Load setting from web app json file"
    global _default_settings
    ret_module = imp.new_module(name)
    _dict=utilities.load_json_config_file(name)
    _default_settings=_dict
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
    if template_dir!=None:
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
    """Return static dirs """
    return  _default_settings.get("STATICFILES_DIRS")
def get_default_language():
    return _default_settings.get("DEFAULT_LANGUAGE")
def get_default_language_engine():
    return _default_settings.get("DEFAULT_LANGUAGE_ENGINE")
def get_static_url():
    return _default_settings.get("STATIC_URL")
def get_static_root():
    return _default_settings.get("STATIC_ROOT")
def get_app_info(file_name):
    """get application info by path of file
    if path of file is in application package"""
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
def get_app_info_by_name(module_name):
    return __cache_find_name[module_name]
def load_app_config(paths):
    """
    Load all application info according to 'paths'
    'paths' is a list of application directory
    """
    global __cache_find_name
    try:
        ret={
            "APPS":[],
            "DEFAULT":None
        }
        ret_apps=[]
        global  app_info
        global  app_info_dir
        global  __paths__
        global __cache_find_name
        for p in paths:

            data=utilities.load_json_from_file(p["PATH"]+"/config")
            app_info.update({data.get("NAME"): data})


            _dir=(utilities.get_host_directory()+"/"+p.get("PATH")).replace("\\","/").replace("//","/")
            __paths__.append(_dir)
            app_info_dir.update({_dir:data})
            module_file=utilities.get_host_directory()+"/"+p["PATH"]
            ret_config = {
                "NAME": data.get("NAME"),
                "URLS": [],
                "DIR":_dir,
                "MODULE":None,
                "PACKAGE_NAME":None,
                "HOST":None
            }

            sys.path.append(module_file)
            module=None
            try:
                # module_name = data.get("VIEWS").get("name")
                package_name=module_file.split('/')[module_file.split('/').__len__()-1]
                module=importlib.import_module(package_name)
                ret_config.update({"MODULE":module})
                ret_config.update({"PACKAGE_NAME": package_name})
                get_app_info(module.__file__).update({"DIR": package_name})
                get_app_info(module.__file__).update({"MODULE": module})
                get_app_info(module.__file__).update({"HOST": p["HOST"]})
                __cache_find_name[module.__name__]=get_app_info(module.__file__)

            except Exception as ex:
                logger.error(ex)
                logger.error("'"+module_file+"' was not found")

                raise Exception("'"+module_file+"' was not found")
            __cache_find_name.update({module.__name__:data})

            _urls=[]

            for route in data.get("ROUTES"):
                _url = route.get("url")
                if (p.get("HOST") != "default"):
                    # _url="^"+p.get("HOST")+"/"+route.get("url")
                    ret_config.update({
                        "HOST":p.get("HOST")
                    })
                _urls.append({
                    "url": _url,
                    "view": module.__name__ + "." + route.get("view"),
                    "name": route.get("name")
                })
            ret_config.update({"URLS":_urls})
            if(ret_config["NAME"]=="default"):
                ret.update({
                    "DEFAULT":ret_config
                })
            else:
                ret_apps.append(ret_config)
            ret.update({
                "APPS":ret_apps
            })

        return  ret
    except Exception as ex:
        logger.error(ex)
        raise ex

def buil_urls(mdl,urls,static_url,static_root):

    urlpatterns=static(_default_settings["CLIENT_STATIC"], document_root=utilities.get_host_directory()+"/"+_default_settings["SERVER_STATIC"])+[]
    urlpatterns += static("default/static/", document_root=urls["DEFAULT"]["DIR"]+"/static") + []

    for app in urls["APPS"]:
        urlpatterns += static(app["HOST"]+"/static/", document_root=app["DIR"]+"/static") + []
        url_module=build_sub_app_urls(app)
        urlpatterns +=[
            url("^"+app["HOST"]+"/", include(url_module.__name__, namespace=url_module.__name__))
        ]

    for route in urls["DEFAULT"]["URLS"]:

        urlpatterns+=[
            url(route.get("url"),  route.get("view"), name=route.get("name"))
        ]

    setattr(mdl,"urlpatterns",urlpatterns)
def build_sub_app_urls(config):
    urlpatterns=[]
    for route in config["URLS"]:
        urlpatterns+=[
            url(route.get("url"), route.get("view"), name=route.get("name"))
        ]

    url_module=imp.new_module(config["NAME"]+"_urls_include")
    setattr(url_module, "urlpatterns",urlpatterns )

    sys.modules.update({
        config["NAME"] + "_urls_include":url_module
    })

    return  url_module




