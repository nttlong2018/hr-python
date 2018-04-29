# from django.http import HttpResponse, HttpResponseRedirect
#
import os
from django.shortcuts import get_object_or_404, render
import membership
from django.http import HttpResponse
from django.shortcuts import redirect


from . import models
import argo
from argo import applications
from models import Login
from  argo import membership
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
application=applications.get_app_by_file(__file__)
# from django.urls import reverse
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@argo.template("index.html")
def index(request):
    try:
        sys_user=User.objects.get(username="sys")
    except ObjectDoesNotExist as ex:
        user = User.objects.create_user('sys', '', '123456')
        user.save()
    if request.user.is_anonymous():
        return redirect(request.get_app_url("login"))

    model=argo.models.base()
    user=membership.get_user("sys")
    if request.get_auth()["user"]==None:
        return redirect(request.get_app_url("login"))
    return request.render(model)

def admin(request):
    return render(request, 'admin.html')
@argo.template("login.html")
def login(request):
    _login=models.Login()
    _login.language=request._get_request().get("language","en")
    if request.GET.has_key("next"):
        _login.url_next=request.GET["next"]
    request.session["language"] = _login.language
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
            if request._get_post().has_key("url_next") \
                    and request._get_post()["url_next"]!="":
                return redirect(request._get_post()["url_next"])
            else:
                return  redirect("/")


        except membership.models.exception as ex:
            _login.is_error=True
            _login.error_message=request.get_global_res("Username or Password is incorrect")
            return request.render(_login)
        except Exception as ex:
            _login.is_error = True
            _login.error_message = ex.message
            return request.render(_login)

    return request.render(_login)
def load_page(request,path):
    try:
        return request.render({})
    except:
        return HttpResponse("page was not found")
@argo.template("sign_out.html")
def sign_out(request):
    membership.sign_out(request.session.session_key)
    request.session.clear()
    return redirect("/")
