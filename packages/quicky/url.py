from . import applications
import imp
import sys
import posixpath
from django.conf.urls.static import static
from django.conf.urls import include, patterns, url
from app_info import app_config
import logging
logger=logging.getLogger(__name__)
_apps_=None
def build_urls(module_name,*args,**kwargs):
    global _apps_
    if _apps_==None:
        _apps_=imp.new_module(module_name)
        sys.modules.update({
            module_name:_apps_
        })
        setattr(_apps_,"urlpatterns",[])
    for app in args[0]:
        ret=applications.load_app(app)
        try:
            if ret.host_dir == "":
                _apps_.urlpatterns.append(url(r"^(?i)", include(ret.mdl.__name__ + ".urls")))
            else:
                _apps_.urlpatterns.append(url(r"^(?i)" + ret.host_dir + "/", include(ret.mdl.__name__ + ".urls")))
        except Exception as ex:
            logger.debug(ex)
            raise ex











