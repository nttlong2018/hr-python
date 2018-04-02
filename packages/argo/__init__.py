from . import config
from  . import utilities as utils
from . import models
__cache_app__={}
def get_application(file):
    global __cache_app__
    if not __cache_app__.has_key(file):
        ret_data=models.app_info()
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
            request.__dict__.update({"template_file":file})
            return fn(request)
        return  exec_request
    return template_decorator


