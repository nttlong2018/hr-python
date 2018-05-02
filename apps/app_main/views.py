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
from django.contrib.auth import authenticate,login as form_login
import quicky
application=applications.get_app_by_file(__file__)
# from django.urls import reverse
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@quicky.view.template("index.html")
def index(request):
    try:
        sys_user=User.objects.get(username="sys")
    except ObjectDoesNotExist as ex:
        user = User.objects.create_user('sys', '', '123456')
        user.save()
    if request.user.is_anonymous():
        return redirect(request.get_app_url("login"))
    else:
        model = argo.models.base()
        return request.render(model)

def admin(request):
    return render(request, 'admin.html')
@quicky.view.template("login.html")
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
            ret=authenticate(username=request._get_post().get("username"), password=request._get_post().get("password"))
            form_login(request,ret)
            return redirect("/")
        except membership.models.exception as ex:
            _login.is_error=True
            _login.error_message=request.get_global_res("Username or Password is incorrect")
            return request.render(_login)
    return request.render(_login)
def load_page(request,path):
    try:
        return request.render({})
    except:
        return HttpResponse("page was not found")
@quicky.view.template("sign_out.html")
def sign_out(request):
    membership.sign_out(request.session.session_key)
    request.session.clear()
    return redirect("/")
