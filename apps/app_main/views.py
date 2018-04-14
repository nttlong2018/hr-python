# from django.http import HttpResponse, HttpResponseRedirect
#
import os
from django.shortcuts import get_object_or_404, render
import membership
from django.http import HttpResponse
from django.shortcuts import redirect


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
        user=membership.create_user("sys","sys",None)
        membership.active_user("sys")
        user.isSysAdmin=True
        membership.update_user(user)
    else:
        membership.active_user("sys")

        user.isSysAdmin = True
        user.description="Ci la test thoi"
        user.displayName="System administrator"
        membership.update_user(user)
    # login_info=membership.validate_session(request.session._get_or_create_session_key())
    if request.get_auth()["user"]==None:
        return redirect("login")
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
