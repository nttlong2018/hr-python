import models

def get_list(args):
    items = models.SYS_FunctionList().get_list()
    return items