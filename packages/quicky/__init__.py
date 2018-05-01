import view
import applications
import authorize
import language
import serilize
import caller
import sql_db
import os
import layout_view
import url
from db import database as mongodb


def get_static_server_path(file,path):
    return os.getcwd() + os.sep + os.path.dirname(file) + os.sep +path