from . import applications
import imp
import sys
import posixpath
from django.conf.urls.static import static
from app_info import app_config
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

        # info=applications.get_urls(app)
        _apps_.urlpatterns.append(ret.get_urls())
        _apps_.urlpatterns.append(ret.get_static_urls())








