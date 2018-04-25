from . import extens
from . import applications
from . import authorize
import threading
lock = None
global lock
lock=threading.Lock()
_cache_view={}
def template_uri(fn):
    def layer(*args, **kwargs):
        def repl(f):
            return fn(f,*args, **kwargs)
        return repl
    return layer
@template_uri
def template(fn,*_path,**kwargs):
    if _path.__len__()==1:
        _path=_path[00]
    if _path.__len__()==0:
        _path=kwargs


    app=applications.get_app_by_file(fn.func_code.co_filename)
    def exec_request(request, **kwargs):
        is_allow=True
        is_public=False
        authenticate=None
        if hasattr(app.settings, "is_public"):
            is_public = getattr(app.settings,"is_public")
        if hasattr(app.settings,"authenticate"):
            authenticate=getattr(app.settings,"authenticate")
        # if not is_public or callable(authenticate):


        extens.apply(request,_path,app)
        if not _cache_view.has_key(app.name):
            lock.acquire()
            _cache_view.update({app.name:{}})
            lock.release()
        if not _cache_view[app.name].has_key(request.get_view_path()):
            try:
                lock.acquire()

                ret=authorize.register_view(
                    app=app.name,
                    view=request.get_view_path()
                )
                _cache_view[app.name].update({
                    request.get_view_path(): ret
                })
                lock.release()
            except Exception as ex:
                lock.release()
                raise ex

        return fn(request, **kwargs)
    return exec_request