from .. import models
def qr_customers():
    ret=models.sys_multi_tenancy().aggregate()
    ret.lookup(models.sys_customers(),"code","code","customer")
    ret.unwind("customer")
    return ret


