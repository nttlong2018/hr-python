import os
import sys
import importlib
from django.conf.urls.static import static
from django.conf.urls import include,url
_apps=None
class app_config():
    package_name=""
    package_path=""
    path=""
    mdl=None
    urls=None
    host_dir=""
    name=""
    auth=None
    login=None
    template_dir=""
    client_static=""
    static=""
    settings=None
    authenticate=None
    on_begin_request=None
    on_end_request = None

    def __init__(self,path):
        global _apps
        if _apps==None:
            _apps={}
            for app in sys.modules["settings"].APPS:
                _apps.update({
                    app["path"]:app
                })
        get_package_name = lambda x: x.split('/')[x.split('/').__len__() - 1]
        get_dir = lambda x, y: os.getcwd() + x[0:x.__len__() - y.__len__() - 1]
        self.package_name=get_package_name(path)
        self.package_path=get_dir(path,self.package_name)
        self.path=path
        sys.path.append(self.package_path)
        self.mdl=importlib.import_module(self.package_name)
        if hasattr(self.mdl,"settings"):
            self.settings=getattr(self.mdl,"settings")
        if(self.settings!=None):
            if hasattr(self.settings,"authenticate"):
                self.authenticate=getattr(self.settings,"authenticate")
            if hasattr(self.settings,"on_authenticate"):
                self.onAuthenticate=getattr(self.settings,"on_authenticate")
            if hasattr(self.settings,"on_begin_request"):
                self.on_begin_request = getattr(self.settings, "on_begin_request")
            if hasattr(self.settings,"on_end_request"):
                self.on_end_request = getattr(self.settings, "on_end_request")
        self.host_dir=(lambda x:x if x!="default" else "")(_apps.get(path).get("host"))
        self.name=_apps.get(path).get("name")
        self.template_dir = _apps[path].get("template_dir", os.path.join(path, "templates"))
        self.client_static=_apps[path].get("client_static",path+ "/static")
        self.static=_apps[path].get("static_dir",os.path.join(path, "static"))
    def get_urls(self):
        if self.urls==None:
            self.urls=[]
        if self.host_dir=="":
            self.urls=url(r'^', include(self.package_name+".urls"))
        else:
            self.urls = url(r'^' + self.host_dir + "/", include(self.package_name + ".urls"))
        return dict(
            urls=self.urls,
            static_url=static(self.get_client_static(), document_root=self.get_server_static())
        )
    def get_client_static(self):
        return self.client_static
    def get_server_static(self):
        _path= (self.static).replace("/",os.path.sep)
        return os.getcwd()+os.path.sep+_path




