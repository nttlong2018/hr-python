from . import applications
import imp
import sys
_apps_=None
def build_urls(module_name,*args,**kwargs):
    global _apps_
    if _apps_==None:
        _apps_=imp.new_module(module_name)
        sys.modules.update({
            module_name:_apps_
        })
    if not _apps_.__dict__.has_key("urlpatterns"):
        _apps_.__dict__.update(dict(urlpatterns=[]))
    for app in args[0]:
        urls=applications.get_urls(app)
        _apps_.urlpatterns.append(urls)


