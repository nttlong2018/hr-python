# from django.http import HttpResponse, HttpResponseRedirect
#
import os
from django.shortcuts import get_object_or_404, render
import membership
from django.http import HttpResponse
from django.shortcuts import redirect
import utilities
import configuration
from . import models
import argo

from models import Login
application=argo.get_application(__file__)
# from django.urls import reverse
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@argo.template("index.html")
def index(request):


    model=argo.models.base()
    user=membership.get_user("sys")
    if user==None:
        membership.create_user("sys","sys",None)
        membership.active_user("sys")
    # login_info=membership.validate_session(request.session._get_or_create_session_key())
    if request.get_auth()["user"]==None:
        return redirect("login")
    return request.render(model)


def admin(request):
    return render(request, 'admin.html')
@argo.template("login.html")
def login(request):
    _login=models.Login()
    if request._get_post().keys().__len__()>0:
        username=request._get_post().get("username")
        password=request._get_post().get("password")
        try:
            user=membership.validate_account(request._get_post().get("username"),request._get_post().get("password"))
            login=membership.sign_in(request._get_post().get("username"),request.session._get_or_create_session_key(),"vn")
            request.set_auth({
                "user":{
                    "id":login.user.userId,
                    "username":login.user.username,
                    "email":login.user.email
                }
            })

            return  redirect("/")


        except membership.models.exception:
            return request.render({
                "message":"Login fail",
                "isError":True,
                "data":{
                    "username":username
                }})
        except Exception as ex:
            return request.render({
                    "message": ex.message,
                    "isError": True})

    return request.render(Login)
def load_page(request,path):
    try:
        return request.render({})
    except:
        return HttpResponse("page was not found")
@argo.template("sign_out.html")
def sign_out(request):
    request.sign_out()
    return request.render({})