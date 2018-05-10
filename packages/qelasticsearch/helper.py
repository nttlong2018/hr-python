from elasticsearch import Elasticsearch
import query
_es=None
def connect(*args,**kwargs):
    global _es
    if _es==None:
        params=args
        if args==():
            params=kwargs
        else:
            params=args[0]
        _es = Elasticsearch(params)
    return query.query(_es)