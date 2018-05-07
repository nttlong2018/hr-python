from django.http import HttpResponse
from django.shortcuts import redirect



import urllib
from . import menu_loader
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as request_login# from django.http import JsonResponse
from bson.objectid import ObjectId
import json
import importlib
import sqlalchemy
import authorization

from datetime import date, datetime
import quicky
application=quicky.applications.get_app_by_file(__file__)
import forms
import logging
logger = logging.getLogger(__name__)
@quicky.view.template("index.html")
def index(request):
    return request.render({
        "menu_items": menu_loader.load_menu_items()
    })

@quicky.view.template("login.html")
def login(request):
    _login = {
        "username":"",
        "password":"",
        "language":"en",
        "next":""
    }
    _login["language"] = request._get_request().get("language", "en")
    if request.GET.has_key("next"):
        _login["next"] = request.GET.get("next",request.get_app_url(""))
    request.session["language"] = _login["language"]
    if request._get_post().keys().__len__() > 0:

        _login["username"] = request._get_post().get("username","")
        _login["password"] = request._get_post().get("password","")
        _login["language"] = request._get_post().get("language", "en")
        user=authenticate(username=request._get_post().get("username",""),
                          password=request._get_post().get("password",""))
        if user==None:
            _login.update(dict(
                error=dict(
                    message=request.get_global_res("Username or Password is incorrect")
                )
            ))
            return request.render(_login)
        else:
            request_login(request,user)
            return redirect(_login["next"])


    return request.render(_login)
# @argo.template(file="simple_login",
#                is_login_page=True)
def login_to_template(request):
    print request
    return request.render({})

@quicky.view.template("category.html")
def load_categories(request,path):
    form = getattr(forms, path)
    return request.render({
        "path": path.lower(),
        "columns":form.layout.get_table_columns()
    })
@quicky.view.template(
    file="dynamic.html",
    is_public=True

)
def load_page(request,path):
    return  request.render({
        "path":path.lower()
    })




