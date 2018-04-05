from . import config
from  . import utilities as utils
from . import models
__cache_app__={}
__cache_app__by_module_name__={}
def get_application_by_module_name(module_name):
    global __cache_app__by_module_name__
    if not __cache_app__by_module_name__.has_key(module_name):
        ret_data = models.app_info()
        app=config.get_app_info_by_name(module_name)
        ret_data.name = app["NAME"]
        ret_data.template_dir = app["DIR"] + "/templates"
        ret_data.client_static = "default/static/"
        ret_data.host = app["HOST"]
        if ret_data.name != "default":
            ret_data.client_static = ret_data.host + "/static/"
        __cache_app__by_module_name__.update({
            file: ret_data
        })
    return __cache_app__by_module_name__[file]
def get_application(file):
    global __cache_app__
    global __cache_app__by_module_name__
    if not __cache_app__.has_key(file):
        ret_data=models.app_info()
        __cache_app__by_module_name__[config.get_app_info(file)["MODULE"].__name__]=ret_data
        ret_data.name=config.get_app_info(file)["NAME"]
        ret_data.template_dir=config.get_app_info(file)["DIR"]+"/templates"
        ret_data.client_static="default/static/"
        ret_data.host=config.get_app_info(file)["HOST"]
        if ret_data.name!="default":
            ret_data.client_static = ret_data.host+"/static/"
        __cache_app__.update({
            file:ret_data
        })
    return __cache_app__[file]
def template(file):

    def template_decorator(fn):
        def exec_request(request):
            app=get_application(fn.func_code.co_filename)
            def render(model):
                return utils.render({
                    "app_name":app.name,
                    "request":request,
                    "language":"",
                    "file":file,
                    "model":model,
                    "templates":app.template_dir,
                    "file":file,
                    "static":app.client_static,
                    "application":app

                })
            request.__dict__.update({"render":render})
            return fn(request)
        return  exec_request
    return template_decorator


