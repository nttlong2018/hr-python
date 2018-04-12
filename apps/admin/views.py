from django.http import HttpResponse
from django.shortcuts import redirect
import argo
import membership
import urllib
from . import menu_loader

application=argo.get_application(__file__)

@argo.template("index.html")
def index(request):
    if request.get_auth()["user"]==None:
        return redirect(request.get_abs_url()+"/login?next="+urllib.quote(request.get_abs_url()+"/"+request.get_app_host(), safe='~()*!.\''))
    if not request.get_auth()["user"].get("IsSysAdmin",False):
        user=membership.get_user(request.get_auth()["user"]["username"])
        request.get_auth()["user"].update({"IsSysAdmin":user.isSysAdmin})
        if not user.isSysAdmin:
            return redirect(request.get_abs_url()+"/login")
        else:
            return request.render({
                "menu_items":menu_loader.load_menu_items()
            })
    else:
         return  request.render({
             "menu_items": menu_loader.load_menu_items()
         })
@argo.template("login.html")
def login(request):
    return request.render({})
@argo.template("index.html")
def load_page(request,path):
    print (path)
