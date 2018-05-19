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
system_settings=None
def get_static_server_path(file,path):
    return os.getcwd() + os.sep + os.path.dirname(file) + os.sep +path
def get_django_settings_module():
    global system_settings
    if system_settings!=None:
        return system_settings
    "get all settings of current project"
    setting_name=os.environ.get("DJANGO_SETTINGS_MODULE",None)
    ret=None
    if setting_name==None:
        return None
    else:
        if not sys.modules.has_key(setting_name):
            return None
        else:
            system_settings=sys.modules[setting_name]
            if hasattr(system_settings,"USE_MULTI_TENANCY") and system_settings.USE_MULTI_TENANCY:
                if not hasattr(system_settings,"MULTI_TENANCY_DEFAULT_SCHEMA"):
                    raise (Exception("It look like you have used 'USE_MULTI_TENANCY'.\n"
                                     "But you forgot set 'MULTI_TENANCY_DEFAULT_SCHEMA' in '{0}'.\n"
                                     "What is default schema?\n"
                                     "Serving multiple tenants under same database,\n"
                                     "where each tenant has its own sets of tables grouped with schema as required by tenant.\n"
                                     "default schema will be used, if the system can not determine schema of user transaction".format(
                        system_settings.__file__
                    )))
                if not hasattr(system_settings,"MULTI_TENANCY_CONFIGURATION"):
                    raise (Exception("It look like you have used 'USE_MULTI_TENANCY'.\n"
                                     "But you forgot set 'MULTI_TENANCY_CONFIGURATION' in '{0}'.\n"
                                     "What is 'MULTI_TENANCY_CONFIGURATION'?\n"
                                     "'MULTI_TENANCY_CONFIGURATION' is include bellow information:\n"
                                     "host=[host data base name]\n"
                                     "port=[mongodb port]\n"
                                     "user=[user name]\n"
                                     "password=[password]\n"
                                     "name=[database name]\n"
                                     "collection=[manage muti tenant collection name]".format(
                        system_settings.__file__
                    )))



def to_server_local_time(val):
     return val+(datetime.datetime.utcnow() - datetime.datetime.now())
def to_client_time(val):
    return val - datetime.timedelta(minutes=threading.current_thread().client_offset_minutes)
def get_client_offset_minutes():
    return threading.current_thread().client_offset_minutes