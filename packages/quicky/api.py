from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import uuid
from django.http import HttpResponse
import json
import importlib
import logging
import serilize
import applications
import sys
import threading
global lock
lock = threading.Lock()
logger = logging.getLogger(__name__)
_cache_id={}
_cache_id_revert={}


@require_http_methods(["POST"])
@csrf_exempt
def call(request):
    try:
        user = request.user
        if user.is_anonymous():
            return HttpResponse('401 Unauthorized', status=401)
        if not user.is_staff and not user.is_superuser:
            return HttpResponse('401 Unauthorized', status=401)
        post_data = json.loads(request.body)
        if not post_data.has_key("path"):
            raise Exception("Api post without using path")
        path = post_data["path"]
        view = post_data["view"]
        path = get_api_path(path)

        view_privileges = applications.get_settings().AUTHORIZATION_ENGINE.get_view_of_user(
            view=view,
            username=user.username
        )
        if user.is_superuser:
            view_privileges = {"is_public": True}



        method_path = path.split("/")[path.split("/").__len__() - 1]
        module_path = path[0:path.__len__() - method_path.__len__()-1]
        mdl = None
        try:
            mdl = importlib.import_module(module_path.replace("/","."))
        except ImportError as ex:
            logger.debug(Exception("import {0} is error or not found".format(module_path)))
            raise Exception("import {0} is error or not found".format(module_path))

        except Exception as ex:
            raise Exception("import '{0}' encountered '{1}'".format(module_path, ex.message))

        ret = None

        if mdl != None:
            try:
                if post_data.has_key("data"):
                    ret = getattr(mdl, method_path)(
                        {
                            "privileges": view_privileges,
                            "data": post_data.get("data", {}),
                            "user": user,
                            "request": request
                        })
                else:
                    ret = getattr(mdl, method_path)(
                        {
                            "privileges": view_privileges,
                            "user": user,
                            "request": request
                        })

            except Exception as ex:
                raise Exception("Call  '{0}' in '{1}' encountered '{2}'".format(method_path, module_path, ex))
        ret_data = serilize.to_json(ret)

        return HttpResponse(ret_data)
    except Exception as ex:
        logger.debug(ex)
        raise ex
def get_api_key(path):
    global _cache_id
    global _cache_id_revert
    if not _cache_id.has_key(path):
        lock.acquire()
        try:
            id = uuid.uuid4().__str__()
            _cache_id.update({
                path: id
            })
            _cache_id_revert.update({
                id: path
            })
            lock.release()

        except Exception as ex:
            lock.release()
            logger.debug(ex)
            raise ex
    return _cache_id[path]
def get_api_path(id):
    if not _cache_id_revert.has_key(id):
        logger.debug("'{0}' was not found".format(id))
        raise Exception("'{0}' was not found".format(id))
    return _cache_id_revert[id]
def logout(request):
    request.session.clear()
    from django.contrib.auth import logout
    user=request.user
    logout(request)



