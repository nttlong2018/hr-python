from .. import models
def data_access_domain():
    ret=models.SYS_ValueList().aggregate().match("list_name == {0}", "LAccessDomain")
    ret.unwind("values")
    ret.join(models.HCSSYS_DataDomain(),"values.value","access_mode","dd")
    ret.project(
        _id = "dd._id",
        dd_code="dd.dd_code",
        dd_name="dd.dd_name",
        access_mode="dd.access_mode",
        description="dd.description",
        created_on="dd.created_on",
        detail="dd.detail",
        display_access_mode="switch(case(values.custom!='',values.custom),values.caption)"
        )
    #ret= models.HCSSYS_DataDomain()
    #ret=ret.aggregate()
    #ret.lookup(models.SYS_ValueList(),"access_mode","values.value","SYS_ValueList")
    #ret.match("SYS_ValueList.list_name=={0}","AccessDomain")
    #ret.unwind("SYS_ValueList")
    #ret.unwind("SYS_ValueList.values")
    #ret.project(
    #    dd_code = 1,
    #    dd_name = 1,
    #    access_mode = 1,
    #    description = 1,
    #    created_on = 1,
    #    detail = 1,
    #    display_access_mode="switch(case(SYS_ValueList.values.custom!='',SYS_ValueList.values.custom),SYS_ValueList.values.caption)"
    #    )
    #ret.group("dd_code")
        
    return ret