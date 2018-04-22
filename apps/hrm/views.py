# -*- coding: utf-8 -*-
import argo
from . import menu
import importlib
import json
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from quicky import layout_view
import forms

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
    form = getattr(forms, path)
    return request.render({
        "path": path.lower(),
        "columns":form.layout.get_table_columns()
    })
@argo.template("category-editor.html")
def load_category(request,path):
    form = getattr(forms, path)
    return request.render({
        "path": path.lower(),
        "form": form.layout.get_form(),
        "get_col": form.layout.get_form_col
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

    view_privileges=argo.get_settings().AUTHORIZATION_ENGINE.get_view_of_user(
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
        mdl = importlib.import_module("hrm.bll."+module_path)
    except Exception as ex:
        raise Exception("import '{0}' encountered '{1}'".format(module_path,ex.message))

    ret=None

    if mdl!=None:
        if not hasattr(mdl,method_path):
            raise (Exception("'{0}' was not found in '{1}'".format(method_path,"hrm.bll."+module_path)))
        try:
            if post_data.has_key("data"):
                ret=getattr(mdl,method_path)(
                    {
                        "privileges":view_privileges,
                        "data":post_data.get("data",{}),
                        "user":login_info.user,
                        "view":view
                    })
            else:
                ret = getattr(mdl, method_path)(
                    {
                        "privileges":view_privileges,
                        "user":login_info.user,
                        "view":view
                    })

        except Exception as ex:
            raise Exception("Call  '{0}' in '{1}' encountered '{2}'".format(method_path, module_path, ex))
    ret_data=argo.utilities.to_json(ret)
    return HttpResponse(ret_data)