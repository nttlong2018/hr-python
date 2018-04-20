import os
import sys
import importlib
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
        self.host_dir=(lambda x:x if x!="default" else "")(_apps.get(path).get("host"))
        self.name=_apps.get(path).get("host")
    def get_urls(self):
        if self.urls==None:
            self.urls=[]
        if self.host_dir=="":
            self.urls=url(r'^', include(self.package_name+".urls"))
        else:
            self.urls = url(r'^' + self.host_dir + "/", include(self.package_name + ".urls"))
        return self.urls

