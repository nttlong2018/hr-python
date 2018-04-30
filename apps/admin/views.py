from django.http import HttpResponse
from django.shortcuts import redirect
import argo
from argo import applications
import membership
import urllib
from . import menu_loader
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
from bson.objectid import ObjectId
import json
import importlib
import sqlalchemy
import authorization
application=applications.get_app_by_file(__file__)
from datetime import date, datetime
import quicky
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif type(obj) is ObjectId:
        return obj.__str__()
    elif type(obj) is sqlalchemy.orm.state.InstanceState:
        return  None
    return obj.__str__()
@argo.template("index.html")
def index(request):
    return request.render({
        "menu_items": menu_loader.load_menu_items()
    })

@argo.template("login.html")
def login(request):

    membership.sign_out(request.session.session_key)


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

        try:
            user = membership.validate_account(_login["username"], _login["password"])
            login = membership.sign_in(_login["username"],
                                       request.session._get_or_create_session_key(), _login["language"])

            if not user.isSysAdmin and not user.isStaff:
                ret_model = {
                    "is_error": True,
                    "error_message": request.get_global_res("This application require sys admin user")
                }
                _login.update({
                    "error": ret_model
                })
                return request.render(_login)
            request.set_auth({
                "user": {
                    "id": login.user.userId,
                    "username": login.user.username,
                    "email": login.user.email,
                    "isSysAdmin":login.user.isSysAdmin,
                    "isStaff":login.user.isStaff
                }
            })
            return redirect("/")



        except membership.models.exception as ex:
            ret_model={
                "is_error":True,
                "error_message":request.get_global_res("Username or Password is incorrect")
            }
            _login.update({
                "error":ret_model
            })
            return request.render(_login)
        # except Exception as ex:
        #     ret_model = {
        #         "is_error": True,
        #         "error_message": ex.message
        #     }
        #     _login.update({
        #         "error": ret_model
        #     })
        #     return request.render(_login)

    return request.render(_login)
# @argo.template(file="simple_login",
#                is_login_page=True)
def login_to_template(request):
    print request
    return request.render({})
@argo.template(
    file="dynamic.html",
    is_public=True

)
def load_page(request,path):
    return  request.render({
        "path":path.lower()
    })
@require_http_methods(["POST"])
@csrf_exempt
def api(request):
    user=request.user
    if user.is_anonymous():
        return HttpResponse('401 Unauthorized', status=401)
    if not user.is_staff and not user.is_superuser:
        return HttpResponse('401 Unauthorized', status=401)
    post_data=json.loads(request.body)
    if not post_data.has_key("path"):
        raise Exception("Api post without using path")
    path=post_data["path"]
    view=post_data["view"]
    if post_data["path"].split("/").__len__()!=2:
        raise Exception("'{0}' is invalid path, path must be */*")

    view_privileges=authorization.get_view_of_user(
        view_id=view,
        user_id=user.id
    )
    if user.is_superuser:
        view_privileges={"is_public":True}


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
                ret=getattr(mdl,method_path)(
                    {
                        "privileges":view_privileges,
                        "data":post_data.get("data",{}),
                        "user":user
                    })
            else:
                ret = getattr(mdl, method_path)(
                    {
                        "privileges":view_privileges,
                        "user":user
                    })

        except Exception as ex:
            raise Exception("Call  '{0}' in '{1}' encountered '{2}'".format(method_path, module_path, ex))
    ret_data=quicky.serilize.to_json(ret)

    return HttpResponse(ret_data)




