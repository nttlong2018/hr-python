def register(func):
    """
    register controller
    :param func:
    :return:
    """
    if not callable(func) :
        raise (Exception("The param must be a function"))


    print (func.name)