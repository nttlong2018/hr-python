from  . import utilities
class base:
    def res(self,key,**caption):
        return key
class app_info:
    name=""
    static_dir=""
    template_dir=""
    client_static=""
    def render(self,config):
        return utilities.render(config)

