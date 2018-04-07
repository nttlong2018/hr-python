from django.http import HttpResponse
from django.shortcuts import redirect
import argo

application=argo.get_application(__file__)

@argo.template({
    "file":"index.html",
    "auth":"admin.auth.verify_user",
    "login":"admin/login"
})
def index(request):
    if request.get_auth()["user"]==None:
        return redirect(request.get_app_url("login"))
    if not request.get_auth()["user"].get("IsSysAdmin",False):
        return redirect(request.get_app_url("login"))
    else:
         return  request.render({})
@argo.template("login.html")
def login(request):
    return request.render({})