# from django.http import HttpResponse, HttpResponseRedirect
#
import os
from django.shortcuts import get_object_or_404, render
import membership
from django.http import HttpResponse
from django.shortcuts import redirect
import utilities
# from django.urls import reverse
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def res(txt):
    return "hello "+txt

def index(request):

    user=membership.get_user("sys")
    if user==None:
        membership.create_user("sys","sys",None)
        membership.active_user("sys")
    login_info=membership.validate_session(request.session._get_session_key())
    if login_info==None:
        return redirect("login")

    # membership.validate_account("sys", "sys")
    # membership.sign_in("sys",request.session.session_key,"vn")
    # return render(request, 'index.html',{
    #     "data":{
    #         "username":login_info.user.username
    #     },
    #     res:res
    #
    # })
    return utilities.render("index.html",{})

def admin(request):
    return render(request, 'admin.html')
def login(request):
    if request._get_post().keys().__len__()>0:
        username=request._get_post().get("username")
        password=request._get_post().get("password")
        try:
            user=membership.validate_account(request._get_post().get("username"),request._get_post().get("password"))
            login=membership.sign_in(request._get_post().get("username"),request.session._get_session_key(),"vn")

            return  redirect("/")


        except membership.models.exception:
            return render(request, 'login.html',{
                "message":"Login fail",
                "isError":True,
                "data":{
                    "username":username
                }
            })
    return render(request, 'login.html')
def load_page(request,path):
    try:
        return render(request, path+'.html')
    except:
        return HttpResponse("page was not found")
