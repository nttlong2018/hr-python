
import os
import sys
import importlib
from django.conf.urls.static import static
from django.conf.urls import include,url
settings=None
class app_config():
    """
    class for app info instance
    """
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
    _is_persistent_schema=None
    _persistent_schema = None

    def __init__(self,config):
        # type: (dict) -> app_config
        """
        Create new instance for app_info
        :param config:including 'path', 'host' and name
        """

        if type(config)==tuple and config.__len__()>0:
            config=config[0]
        if not config.has_key("path"):
            raise(Exception("'path' was not found"))
        if not config.has_key("host"):
            raise (Exception("'host' was not found"))
        path=config["path"]



        get_package_name = lambda x: x.split('/')[x.split('/').__len__() - 1]
        get_dir = lambda x, y: os.getcwd()+os.sep + x[0:x.__len__() - y.__len__() - 1]
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
        self.host_dir=(lambda x:x if x!="default" else "")(config["host"])
        self.name= config["name"]
        self.template_dir = config.get("templates", os.path.join(path, "templates"))
        self.client_static=config.get("client_static",path+ "/static")
        self.static=config.get("static_dir",os.path.join(path, "static"))
    def get_static_urls(self):
        """
        get static url of application for client
        :return:
        """
        if self.host_dir == "":
            return url(r'^' + self.name + '/static/(?P<path>.*)$', 'django.views.static.serve',
                       {'document_root': self.get_server_static(), 'show_indexes': True})
        else:
            return url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                       {'document_root': self.get_server_static(), 'show_indexes': True})

    def get_urls(self):
        """
        Buil list of urls
        :return:
        """
        if self.urls==None:
            self.urls=[]
        if self.host_dir=="":
            self.urls=url(r'^(?i)', include(self.package_name+".urls"))
        else:
            self.urls = url(r'^(?i)' + self.host_dir + "/", include(self.package_name + ".urls"))
        return [self.urls,self.get_static_urls()]
    def get_client_static(self):
        """
        get relative client path at server
        :return:
        """
        return self.client_static
    def is_persistent_schema(self):
        if self._is_persistent_schema == None:
            self._is_persistent_schema=hasattr(self.mdl.settings, "DEFAULT_DB_SCHEMA")
        return self._is_persistent_schema
    def get_persistent_schema(self):
        if self._persistent_schema == None:
            self._persistent_schema=""
            if self.is_persistent_schema():
                self._persistent_schema=self.mdl.settings.DEFAULT_DB_SCHEMA

        return self._persistent_schema



    def get_server_static(self):
        """
        get full server static path
        :return:
        """
        _path= (self.static).replace("/",os.path.sep)
        return os.getcwd()+os.path.sep+_path
    def get_login_url(self):
        """
        get login url from settings of app in settings.py
        :return:
        """
        import threading

        if hasattr(threading.currentThread(), "tenancy_code"):
            if hasattr(self.mdl.settings, "login_url"):
                if self.mdl.settings.login_url[0:1] == '/':
                    self.mdl.settings.login_url = self.mdl.settings.login_url[
                                                  1:self.mdl.settings.login_url.__len__()]
                if not self.is_persistent_schema():

                    if self.host_dir == "":
                        return "/" + threading.currentThread().request_tenancy_code + "/" + self.mdl.settings.login_url
                    else:
                        return "/" + threading.currentThread().request_tenancy_code + "/" + self.host_dir + "/" + self.mdl.settings.login_url
                else:
                    if self.host_dir == "":
                        setattr(threading.currentThread(), "request_tenancy_code", self.get_persistent_schema())
                        return  "/" + self.mdl.settings.login_url
                    else:
                        setattr(threading.currentThread(),"request_tenancy_code",self.get_persistent_schema())
                        return "/" + self.host_dir + "/" + self.mdl.settings.login_url

        else:
            if hasattr(self.mdl.settings, "login_url"):
                if self.host_dir == "":
                    return "/" + self.mdl.settings.login_url
                else:
                    return "/" + self.host_dir + "/" + self.mdl.settings.login_url