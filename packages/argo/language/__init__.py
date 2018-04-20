import importlib
_instance=None
def load(*args,**kwargs):
    global _instance
    if _instance==None:
        _instance=importlib.import_module(kwargs["provider"])
        _instance.load(kwargs)

    print args
def get_language_item(language,app,view,key,caption):
    return _instance.get_language_item(language,app,view,key,caption)