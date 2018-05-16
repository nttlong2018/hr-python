from . import *
import expr
class filter_expression():
    _pipe={}
    def __init__(self,expression,*args,**kwargs):
        params = args
        if args == ():
            params = kwargs
        self._pipe=expr.parse_expression_to_json_expression(expression, params)
    def And(self,expression,*args,**kwargs):
        params=args
        if args==():
            params=kwargs
        ret=expr.parse_expression_to_json_expression(expression, params)
        self._pipe.update({
            "$and":ret
        })
        return self
    def Or(self,expression,*args,**kwargs):
        params = args
        if args == ():
            params = kwargs
        ret = expr.parse_expression_to_json_expression(expression, params)
        self._pipe.update({
            "$or": ret
        })
        return self
    def get_filter(self):
        return self._pipe

