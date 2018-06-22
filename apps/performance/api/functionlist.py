from . import models

def get_list(args):
    items = models.SYS_FunctionList().get_list()
    return items

def get_tree(args):
    items = models.SYS_FunctionList().aggregate().project(
        function_id      = 1,
        parent_id        = 1,
        default_name     = 1
        )
    
    return items.get_list()