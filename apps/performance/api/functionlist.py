from . import models

def get_list(args):
    items = models.SYS_FunctionList().aggregate().project(
        sorting              = 1,
        description          = 1,
        custom_name          = 1,
        style_class          = 1,
        url                  = 1,
        image                = 1,
        default_name         = 1,
        height               = 1,
        parent_id            = 1,
        active               = 1,
        function_id          = 1,
        type                 = 1,
        width                = 1,
        icon                 = 1,
        app                  = 1,
        level_code           = 1
        ).match("app == {0}", "PERF").sort({"sorting":1})
    
    return items.get_list()

def get_tree(args):
    items = models.SYS_FunctionList().aggregate().project(
        function_id      = 1,
        parent_id        = 1,
        default_name     = 1,
        app              = 1
        ).match("app == {0}", "PERF")
    
    return items.get_list()