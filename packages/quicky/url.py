from . import applications
import imp
import sys
import posixpath
from django.conf.urls.static import static
from django.conf.urls import include, patterns, url
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
        if ret.host_dir=="":
            _apps_.urlpatterns.append(url(r"^",include(ret.mdl.__name__+".urls")))
        else:
            _apps_.urlpatterns.append(url(r"^" + ret.host_dir+"/" , include(ret.mdl.__name__ + ".urls")))
        # _apps_.urlpatterns.append(ret.get_static_urls())
        #url(r'^lv_admin/', include('lv_admin.urls'))








