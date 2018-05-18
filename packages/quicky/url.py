
from . import applications
import imp
import importlib
import sys
import posixpath
from django.conf.urls.static import static
from django.conf.urls import include, patterns, url
from app_info import app_config
import logging
logger=logging.getLogger(__name__)
_apps_=None
def build_urls(module_name,*args,**kwargs):
    from . import get_django_settings_module
    is_multi_tenancy=get_django_settings_module().__dict__.get("USE_MULTI_TENANCY",False)
    global _apps_
    if _apps_==None:
        _apps_=imp.new_module(module_name)
        sys.modules.update({
            module_name:_apps_
        })
        setattr(_apps_,"urlpatterns",[])
        if not is_multi_tenancy:
            for app in args[0]:
                try:
                    ret = applications.load_app(app)
                    if ret.host_dir == "":
                        _apps_.urlpatterns.append(url(r"^(?i)", include(ret.mdl.__name__ + ".urls")))
                    else:
                        _apps_.urlpatterns.append(url(r"/^(?i)" + ret.host_dir + "/", include(ret.mdl.__name__ + ".urls")))
                except Exception as ex:
                    raise (Exception("error in '{0}', detail\n {1}".format(ret.mdl.__name__ + ".urls",ex)))
        else:
            lst_urls=[]
            for app in args[0]:
                ret = applications.load_app(app)
                url_items=importlib.import_module(ret.mdl.__name__ + ".urls").urlpatterns
                dynamic_urls=[x for x in url_items if not x.default_args.has_key("document_root") ]
                static_urls=[x for x in url_items if x.default_args.has_key("document_root") ]

                # for url_item in url_items:
                #     if ret.host_dir == "":
                #         lst_urls.append(url_item)
                if ret.host_dir == "":
                    _apps_.urlpatterns.append(url(r"^(?i)", include(static_urls)))
                    _apps_.urlpatterns.append(url(r"^(?i)(?P<tenancy_code>.*)/", include(dynamic_urls)))
                else:
                    _apps_.urlpatterns.append(url(r"/^(?i)" + ret.host_dir + "/", include(static_urls)))
                    _apps_.urlpatterns.append(
                        url(r"^(?i)(?P<tenancy_code>.*)/" + ret.host_dir + "/", include(dynamic_urls)))

            x=_apps_.urlpatterns



    # for app in args[0]:
    #
    #     try:
    #         if ret.host_dir == "":
    #             _apps_.urlpatterns.append(url(r"^(?i)", include(ret.mdl.__name__ + ".urls")))
    #             # if not is_multi_tenancy:
    #             #     _apps_.urlpatterns.append(url(r"^(?i)", include(ret.mdl.__name__ + ".urls")))
    #             # else:
    #             #     _apps_.urlpatterns.append(url(r"^(?i)(?P<tenancy_code>.*)/", include(ret.mdl.__name__ + ".urls")))
    #
    #
    #         else:
    #             if not is_multi_tenancy:
    #                 _apps_.urlpatterns.append(url(r"/^(?i)" + ret.host_dir + "/", include(ret.mdl.__name__ + ".urls")))
    #             else:
    #                 _apps_.urlpatterns.append(url(r"^(?i)(?P<tenancy_code>.*)/" + ret.host_dir + "/", include(ret.mdl.__name__ + ".urls")))
    #         x=_apps_.urlpatterns
    #     except Exception as ex:
    #         logger.debug(ex)
    #         raise ex











