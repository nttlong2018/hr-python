from . import *
import expr
from filter_expression import filter_expression
def filter(expression,*args,**kwargs):
    ret = filter_expression(expression,*args,**kwargs)
    return ret