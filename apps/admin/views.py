from django.http import HttpResponse
from django.shortcuts import redirect
import argo
import membership
import urllib
from . import menu_loader
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import importlib
application=argo.get_application(__file__)
from datetime import date, datetime
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    return None
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
@argo.template("dynamic.html")
def load_page(request,path):
    return  request.render({
        "path":path.lower()
    })
@require_http_methods(["POST"])
@csrf_exempt
def api(request):
    post_data=json.loads(request.body)
    if not post_data.has_key("path"):
        raise Exception("Api post without using path")
    path=post_data["path"]
    if post_data["path"].split("/").__len__()!=2:
        raise Exception("'{0}' is invalid path, path must be */*")
    module_path=path.split("/")[0]
    method_path=path.split('/')[1]
    mdl=None
    try:
        mdl = importlib.import_module(module_path)
    except Exception as ex:
        raise Exception("import '{0}' encountered '{1}'".format(module_path,ex.message))

    ret=None

    if mdl!=None:
        try:
            if post_data.has_key("data"):
                ret=getattr(mdl,method_path)(post_data.get("data",{}))
            else:
                ret = getattr(mdl, method_path)()

        except Exception as ex:
            raise Exception("Call  '{0}' in '{1}' encountered '{2}'".format(method_path, module_path, ex))
    if type(ret) is list:
        ret_data=json.dumps([r.__dict__ for r in ret],default=json_serial)
    else:
        if ret==None:
            ret_data=None
        else:
            if type(ret) is dict:
                ret_data = json.dumps(ret, default=json_serial)
            else:
                ret_data = json.dumps(ret.__dict__, default=json_serial)
    x=ret_data
    return HttpResponse(ret_data)




