import view
import applications
import authorize
import language
import serilize
import caller
import sql_db
import os
import layout_view
import m_query
class mongo():
    aggregation=_aggregation
    match=_match
def get_static_server_path(file,path):
    return os.getcwd() + os.sep + os.path.dirname(file) + os.sep +path