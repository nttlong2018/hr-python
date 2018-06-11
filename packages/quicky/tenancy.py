import threading
def get_schema():
    "Get tenancy schema"
    if hasattr(threading.currentThread(),"tenancy_code"):
        return threading.currentThread().tenancy_code
    else:
        return None

def get_customer_code():
    if hasattr(threading.currentThread(),"request_tenancy_code"):
        return threading.currentThread().request_tenancy_code
    else:
        return None
    

     