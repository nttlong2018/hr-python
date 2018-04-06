from . import config
from . import utilities as utils
from . import models
import membership
import logging
logger = logging.getLogger(__name__)
__cache_app__={}
__cache_app__by_module_name__={}
__session_cache__={}
def get_application_by_module_name(module_name):
    try:
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
    except Exception as ex:
        logger.error(ex)
        raise Exception("Error in {0} with {1}".format(module_name,ex.message))

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
            def set_auth(data):
                global __session_cache__

                if not data.has_key("user"):
                    raise Exception("Please set 'user' info {id:string,username:string}")
                __session_cache__.update({
                    request.session._get_session_key(): data
                })
                request.session["authenticate"] = {
                    "user": data
                }
            def get_auth():
                global __session_cache__
                login_info = membership.validate_session(request.session._get_or_create_session_key())
                if login_info==None:
                    request.session["authenticate"]={
                        "user":None
                    }
                    __session_cache__.update({
                        request.session._get_session_key():{
                            "user":None
                        }
                    })

                else:
                    request.session["authenticate"] = {
                        "user": {
                                "user_id": login_info.user.userId,
                                "username": login_info.user.username,
                                "email": login_info.user.email
                            }
                    }
                    __session_cache__.update({
                        request.session._get_session_key(): {
                            "user": {
                                "user_id": login_info.user.userId,
                                "username": login_info.user.username,
                                "email": login_info.user.email
                            }
                        }
                    })

                return __session_cache__[request.session._get_session_key()]



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
                    "application":app,
                    "get_auth":get_auth

                })
            request.__dict__.update({"render":render})
            request.__dict__.update({"set_auth": set_auth})
            request.__dict__.update({"get_auth": get_auth})
            return fn(request)
        return  exec_request
    return template_decorator


