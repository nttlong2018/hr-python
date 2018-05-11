from . import *
from . import expr
from filter_expression import filter_expression
from  aggregate_expression import aggregate_expression
def filter(expression,*args,**kwargs):
    ret = filter_expression(expression,*args,**kwargs)
    return ret
def aggregate():
    ret=aggregate_expression()
    return ret
def find(*args,**kwargs):
    pass