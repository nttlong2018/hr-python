from  . import utilities
class base:
    def res(self,key,**caption):
        return key
class app_info:
    name=""
    static_dir=""
    template_dir=""
    client_static=""
    host=""
    def render(self,config):
        config.update({"templates": self.template_dir})
        config.update({"static": self.client_static})
        return utilities.render(config)

