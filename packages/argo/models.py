from  . import utilities
from  . import config as argo_config
class base:
    def res(self,key,**caption):
        return key
class app_info:
    name=""
    static_dir=""
    template_dir=""
    client_static=""
    host=""
    login=None
    auth=None
    def render(self,config):
        request=None
        if not type(config) is dict:
            request=config
            config={}
            config.update({
                "request":request
            })

        if not config.has_key("request"):
            raise Exception("'request' is emty")
        if not config.has_key("file"):
            config.update({
                "file":config["request"].__dict__["template_file"]
            })
        if config["request"].session.get("language",None) != None:
            config.update({
                "language": config["request"].session["language"]
            })
        else:
            config.update({
                "language": argo_config.get_default_language()
            })
        config.update({"templates": self.template_dir})
        config.update({"static": self.client_static})
        config.update({"host": self.host})
        config.update({"app_name": self.name})
        return utilities.render(config)

