from . import *
import expr
def get_param_kw(*args,**kwargs):
    print args
    print kwargs
    
    if type(args) is tuple and args.__len__()>0 and type(args[0]) is dict:
        return args[0]
    if type(args) is tuple and args.__len__()>0 and not type(args[0]) is dict:
       return list(args)

class filter_expression():
    _pipe={}
    def __init__(self,expression,*args,**kwargs):
        params = get_param_kw(*args,**kwargs)
        if type(params) is list:
            self._pipe=expr.parse_expression_to_json_expression(expression, *params)
        else:
            self._pipe=expr.parse_expression_to_json_expression(expression, params)
    def And(self,expression,*args,**kwargs):
        params = get_param_kw(*args,**kwargs)
        ret=None
        if type(params) is list:
            ret=self._pipe=expr.parse_expression_to_json_expression(expression, *params)
        else:
            ret=self._pipe=expr.parse_expression_to_json_expression(expression, params)
        
        self._pipe.update({
            "$and":ret
        })
        return self
    def Or(self,expression,*args,**kwargs):
        params = get_param_kw(*args,**kwargs)
        ret=None
        if type(params) is list:
            ret=self._pipe=expr.parse_expression_to_json_expression(expression, *params)
        else:
            ret=self._pipe=expr.parse_expression_to_json_expression(expression, params)
        self._pipe.update({
            "$or": ret
        })
        return self
    def get_filter(self):
        return self._pipe

