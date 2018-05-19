import os
import datetime
def authenticate(request):
    if not request.user.is_anonymous() and \
            (request.user.is_superuser or \
        request.user.is_staff) and \
        request.user.is_active:
        return True
    else:
        return False

    # request.user.is_superuser
    # login_info=membership.validate_session(request.session.session_key)
    # if login_info==None:
    #     return False
    # user = login_info.user;
    # if not user.isSysAdmin:
    #     return user.isStaff
    # else:
    #     return True

def on_begin_request(request):
    setattr(request,"begin_time",datetime.datetime.now())
    print(request)

def on_end_request(request):
    print("time is :{0} in {1}".format((datetime.datetime.now()-request.begin_time).microseconds,request.path_info))

Database_=dict(
    host="172.16.7.63",
    name="lv01_lms",
    port=27017,
    user="sys",
    password="123456"
)
Database=dict(
    host="localhost",
    name="hrm",
    port=27017,
    user="root",
    password="123456"
)
login_url="login"
import json_db_sync
json_db_sync.set_connect(Database)
json_db_sync.sync_json_data_from_file(
    os.path.dirname(__file__)+os.sep+"functionlist.json",
    "SYS_FunctionList",
    keys=[
        "function_id"
    ]
)