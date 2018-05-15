import view
import applications
import authorize
import language
import sys
import caller
import sql_db
import os
import layout_view #use for boostrap layout definition
import url
import datetime
import threading
def get_static_server_path(file,path):
    return os.getcwd() + os.sep + os.path.dirname(file) + os.sep +path
def get_django_settings_module():
    "get all settings of current project"
    setting_name=os.environ.get("DJANGO_SETTINGS_MODULE",None)
    if setting_name==None:
        return None
    else:
        if not sys.modules.has_key(setting_name):
            return None
        else:
            return sys.modules[setting_name]

def to_server_local_time(val):
     return val+(datetime.datetime.utcnow() - datetime.datetime.now())
def to_client_time(val):
    return val - datetime.timedelta(minutes=threading.current_thread().client_offset_minutes)
def get_client_offset_minutes():
    return threading.current_thread().client_offset_minutes