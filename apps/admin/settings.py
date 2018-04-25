import membership
import datetime
def authenticate(request):
    login_info=membership.validate_session(request.session.session_key)
    if login_info==None:
        return False
    user = login_info.user;
    if not user.isSysAdmin:
        return user.isStaff
    else:
        return True
def on_begin_request(request):
    setattr(request,"begin_time",datetime.datetime.now())
    print(request)
def on_end_request(request):

    print("time is :{0} in {1}".format((datetime.datetime.now()-request.begin_time).microseconds,request.path_info))