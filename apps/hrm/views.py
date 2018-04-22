# -*- coding: utf-8 -*-
import argo
from . import menu
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from . import list_config
@argo.template("index.html")
def index(request):
    txt=request.get_app_res("Tỉnh thành")
    menu_items=[]
    return request.render(
        dict(
            menu_items=menu.menu_items
        )
    )
@argo.template("category.html")
def load_categories(request,path):

    return request.render({
        "path": path.lower(),
        "columns":list_config.get_columns(path)
    })
@argo.template("dynamic.html")
def load_page(request,path):
    return request.render({
        "path": path.lower()
    })
@require_http_methods(["POST"])
@csrf_exempt
def api(request):
    login_info=argo.get_settings().MEMBERSHIP_ENGINE.validate_session(request.session.session_key)
    if login_info==None:
        return HttpResponse('401 Unauthorized', status=401)
    if not login_info.user.isSysAdmin:
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
        user_id=login_info.user.userId
    )
    if login_info.user.isSysAdmin:
        view_privileges={"is_public":True}
    if view_privileges==None and not login_info.user.isSysAdmin:
        return HttpResponse('401 Unauthorized', status=401)

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
                        "user":login_info.user
                    })
            else:
                ret = getattr(mdl, method_path)(
                    {
                        "privileges":view_privileges,
                        "user":login_info.user
                    })

        except Exception as ex:
            raise Exception("Call  '{0}' in '{1}' encountered '{2}'".format(method_path, module_path, ex))
    if type(ret) is list:
        if ret.__len__()==0:
            ret_data="[]"
        else:
            if type(ret[0]) is dict:
                ret_data=json.dumps(ret)
            else:
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