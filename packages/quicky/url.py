import re
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
settings=None
def build_urls(module_name,*args,**kwargs):
    """
    buil full url
    :param module_name:
    :param args:
    :param kwargs:
    :return:
    """
    from . import get_tenancy_code_regex
    host_dir=None
    from . import get_django_settings_module
    global settings
    if settings == None:
        settings = get_django_settings_module()
    if hasattr(settings, "HOST_DIR"):
        host_dir = settings.HOST_DIR
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
                    if host_dir==None:
                        ret = applications.load_app(app)
                        if ret.host_dir == "":
                            _apps_.urlpatterns.append(url(r"^(?i)", include(ret.mdl.__name__ + ".urls")))
                        else:
                            _apps_.urlpatterns.append(
                                url(r"^(?i)" + ret.host_dir + "/", include(ret.mdl.__name__ + ".urls")))
                    else:
                        ret = applications.load_app(app)
                        if ret.host_dir == "":
                            _apps_.urlpatterns.append(url(r"^(?i)"+host_dir+"/", include(ret.mdl.__name__ + ".urls")))
                        else:
                            _apps_.urlpatterns.append(
                                url(r"^(?i)"+host_dir+"/" + ret.host_dir + "/", include(ret.mdl.__name__ + ".urls")))
                except Exception as ex:
                    raise (Exception("error in '{0}', detail\n {1}".format(ret.mdl.__name__ + ".urls",ex)))
        else:
            lst_urls=[]
            default_app=None
            default_urls=[]
            #build static urls
            # static url is the same for every schema

            # def set_ord_app(x,list):
            #     if x.get('schema',None) != None:
            #         return  -1
            #     elif x.get('host','default') =="default" or x.get('host','default') == "":
            #         x["ord"] = 0
            #     else:
            #         x["ord"] =list.index(x)+2
            #     return x


            app_dicts={}
            for x in args[0]:
                app_dicts.update({
                    x["host"]:x
                })
            list_of_apps_with_persistent_schema=[x for x in args[0] if x.has_key("schema")]
            list_of_apps_with_public = [x for x in args[0] if x.get("host",None)== "" or x.get("host",None) == "default" or x.get("host",None) == None]
            # list_of_remain_apps=[x for x in args[0] if list_of_apps_with_persistent_schema.count(x) ==0 and list_of_apps_with_public.count(x) == 0]

            list_of_key_of_apps_with_persistent_schema=[x.get("host") for x in list_of_apps_with_persistent_schema]
            list_of_key_of_apps_with_public = [x.get("host") for x in list_of_apps_with_public]
            list_of_key_remain_apps = [x.get("host") for x in args[0] if list_of_key_of_apps_with_persistent_schema.count(x.get("host")) ==0 and list_of_key_of_apps_with_public.count(x.get("host")) == 0]

            list_of_key_of_apps_with_public.sort()
            list_of_key_of_apps_with_persistent_schema.sort()
            list_of_key_remain_apps.sort()



            list_of_apps=[]

            for x in list_of_key_of_apps_with_persistent_schema:
                list_of_apps.append(app_dicts[x])
            for x in list_of_key_of_apps_with_public:
                list_of_apps.append(app_dicts[x])
            for x in list_of_key_remain_apps:
                list_of_apps.append(app_dicts[x])






            for app in list_of_apps:
                ret = applications.load_app(app)
                if app.has_key("schema"):
                    setattr(ret.settings,"DEFAULT_DB_SCHEMA",app.get("schema"))
                if app.has_key("login"):
                    setattr(ret.settings, "login_url", app.get("login"))
                if app.has_key("authenticate"):
                    try:
                        _authenticate= importlib.import_module(app.get("authenticate"))
                        if not callable(_authenticate):
                            raise (Exception("'{0}' is callable. Please, check application with name '{1}' in settings.py".format(app.get("authenticate"),app.get("name"))))
                        setattr(ret.settings, "authenticate", app.get("login"))
                    except Exception as ex:
                        msg ="Can not import '{0}'. Please, check application with name '{1}' in settings.py ".format(app.get("authenticate"),app.get("name"))
                        raise (Exception(msg))

                url_items=importlib.import_module(ret.mdl.__name__ + ".urls").urlpatterns

                static_urls=[x for x in url_items if x.default_args.has_key("document_root") ]
                if ret.host_dir == "":
                    root_doc = static_urls[0].default_args["document_root"]
                    reg_ex = static_urls[0].regex.pattern
                    if host_dir!=None:
                        reg_ex =reg_ex.replace("^","^"+host_dir+"/")

                    _apps_.urlpatterns.append(
                        url(
                            reg_ex.replace("^","^(?i)"),
                            'django.views.static.serve',
                            {
                                'document_root': root_doc,
                                "show_indexes": static_urls[0].default_args.get("show_indexes", False)
                            }
                        )

                    )
                else:
                    root_doc=static_urls[0].default_args["document_root"]
                    reg_ex=static_urls[0].regex.pattern
                    reg_ex=reg_ex.replace("^", "^" + ret.host_dir + "/")
                    if host_dir!=None:
                        reg_ex = reg_ex.replace("^", "^" + host_dir + "/")
                    _apps_.urlpatterns.append(
                        url(
                            reg_ex.replace("^","^(?i)"),
                            'django.views.static.serve',
                            {
                                'document_root': root_doc,
                                "show_indexes": static_urls[0].default_args.get("show_indexes", False)
                            }
                        )

                    )
            #build url
            for app in list_of_apps:
                ret = applications.load_app(app)
                is_use_default_schema = hasattr(ret.settings, "DEFAULT_DB_SCHEMA")
                url_items=importlib.import_module(ret.mdl.__name__ + ".urls").urlpatterns
                for url_item in url_items:
                    if hasattr(url_item,"default_args"):
                        if not url_item.default_args.has_key("document_root"):
                            if ret.host_dir == "":

                                default_urls.append(url_item)
                                url_regex=url_item.regex.pattern
                                if host_dir==None:

                                    url_regex=url_regex.replace("^","^(?i)(?P<tenancy_code>"+get_tenancy_code_regex()+")/")
                                else:
                                    url_regex = url_regex.replace("^", "^(?i)"+host_dir+"/(?P<tenancy_code>"+get_tenancy_code_regex()+")/")
                                if url_item.callback!=None:
                                    map_url=url(
                                        url_regex,
                                        url_item.callback
                                    )
                                    _apps_.urlpatterns.append(map_url)
                                else:
                                    map_url = url(
                                        url_regex,
                                        url_item._callback_str
                                    )
                                    _apps_.urlpatterns.append(map_url)

                            elif not is_use_default_schema:
                                url_regex = url_item.regex.pattern
                                if host_dir == None:
                                    url_regex = url_regex.replace("^",
                                                                  "^(?i)(?P<tenancy_code>"+get_tenancy_code_regex()+")/" + ret.host_dir + "/")
                                else:
                                    url_regex = url_regex.replace("^",
                                                              "^(?i)"+host_dir+"/(?P<tenancy_code>"+get_tenancy_code_regex()+")/" + ret.host_dir + "/")

                                map_url = url(
                                    url_regex,
                                    url_item.callback
                                )
                                _apps_.urlpatterns.append(map_url)
                            else:
                                url_regex = url_item.regex.pattern
                                if host_dir == None:
                                    url_regex = url_regex.replace("^",
                                                                  "^" + ret.host_dir + "/")
                                else:
                                    url_regex = url_regex.replace("^",
                                                                  "^/" + ret.host_dir + "/")

                                map_url = url(
                                    url_regex,
                                    url_item.callback
                                )
                                _apps_.urlpatterns.append(map_url)
                    else:
                        f=url_item



            for url_item in default_urls:
                url_regex = url_item.regex.pattern
                if host_dir!=None:
                    url_regex=url_regex.replace("^","^"+host_dir+"/")


                class obj_exec_request():
                    url_item=None
                    def __init__(self,url_item):
                        self.url_item=url_item
                    def exec_request(self,request, *args, **kwargs):
                        setattr(request,"not_inclue_tenancy_code",True)
                        return self.url_item.callback(
                            request,
                            get_django_settings_module().MULTI_TENANCY_DEFAULT_SCHEMA,
                            *args,
                            **kwargs)

                fx=obj_exec_request(url_item)
                map_url = url(
                    url_regex,
                    fx.exec_request
                )
                _apps_.urlpatterns.append(map_url)




    x=_apps_.urlpatterns











