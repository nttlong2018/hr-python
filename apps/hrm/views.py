# -*- coding: utf-8 -*-

from . import menu
import importlib
import json
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from quicky import layout_view
import forms
import logging

import quicky
logger = logging.getLogger(__name__)


logger = logging.getLogger(__name__)
@quicky.view.template("index.html")

def index(request):

    menu_items=[]
    return request.render(
        dict(
            menu_items=menu.menu_items
        )
    )



@quicky.view.template("category.html")

def load_categories(request,path):
    form = getattr(forms, path)
    return request.render({
        "path": path.lower(),
        "columns":form.layout.get_table_columns()
    })

@quicky.view.template("category-editor.html")

def load_category(request,path):
    form = getattr(forms, path)
    return request.render({
        "path": path.lower(),
        "form": form.layout.get_form(),
        "get_col": form.layout.get_form_col
    })

@quicky.view.template("dynamic.html")

def load_page(request,path):

    return request.render({
        "path": path.lower()
    })
@require_http_methods(["POST"])
@csrf_exempt
def api(request):
    user=request.user
    post_data=json.loads(request.body)
    if not post_data.has_key("path"):
        raise Exception("Api post without using path")
    path=post_data["path"]
    view=post_data["view"]
    if post_data["path"].split("/").__len__()!=2:
        raise Exception("'{0}' is invalid path, path must be */*")

    view_privileges=quicky.get_settings().AUTHORIZATION_ENGINE.get_view_of_user(
        view_id=view,
        user_id=user.id
    )
    if user.is_superuser:
        view_privileges={"is_public":True}
    if view_privileges==None and not login_info.user.isSysAdmin:
        return HttpResponse('401 Unauthorized', status=401)

    module_path=path.split("/")[0]
    method_path=path.split('/')[1]
    mdl=None
    try:
        mdl = importlib.import_module("hrm.bll."+module_path)
    except Exception as ex:
        logger.debug(ex)

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
                        "user":user,
                        "view":view
                    })
            else:
                ret = getattr(mdl, method_path)(
                    {
                        "privileges":view_privileges,
                        "user":user,
                        "view":view
                    })

        except Exception as ex:
            raise Exception("Call  '{0}' in '{1}' encountered '{2}'".format(method_path, module_path, ex))
    ret_data=quicky.serilize.to_json(ret)
    return HttpResponse(ret_data)