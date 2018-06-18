from .. import models
def data_access_domain():
    ret= models.HCSSYS_DataDomain()
    ret=ret.aggregate()
    ret.lookup(models.SYS_ValueList(),"access_mode","values.value","SYS_ValueList")
    ret.match("SYS_ValueList.list_name=={0}","AccessDomain")
    ret.unwind("SYS_ValueList")
    ret.unwind("SYS_ValueList.values")
    ret.project(
        dd_code = 1,
        dd_name = 1,
        access_mode = 1,
        description = 1,
        created_on = 1,
        detail = 1,
        display_access_mode="switch(case(SYS_ValueList.values.custom!='',SYS_ValueList.values.custom),SYS_ValueList.values.caption)"
        )
    print ret._pipe
        
    return ret