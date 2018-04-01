from . import config
from  . import utilities as utils
from . import models
__cache_app__={}
def get_application(file):
    if __cache_app__.has_key(file):
        ret_data=models.app_info()
        ret_data.name=config.get_app_info(file)["NAME"]
        __cache_app__.update({
            file:ret_data
        })


