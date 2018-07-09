from .. import models
def display_list_employee_type():
    ret=models.SYS_ValueList().aggregate().match("list_name == {0}", "LEmployeeType")
    ret.unwind("values")
    ret.join(models.HCSLS_EmployeeType(),"values.value","true_type","el")
    ret.left_join(models.auth_user_info(), "el.created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "el.modified_by", "username", "um")
    ret.project(
        _id = "el._id",
        emp_type_code="el.emp_type_code",
        emp_type_name="el.emp_type_name",
        emp_type_name2="el.emp_type_name2",
        true_type="el.true_type",
        rate_main_sal="el.rate_main_sal",
        rate_soft_sal="el.rate_soft_sal",
        ordinal="el.ordinal",
        created_by="uc.login_account",
        created_on="el.created_on",
        modified_on="switch(case(el.modified_on!='',el.modified_on),'')",
        modified_by="switch(case(el.modified_by!='',um.login_account),'')",
        lock="el.lock",
        display_true_type="switch(case(values.custom!='',values.custom),values.caption)"
        )
    ret.sort(dict(
        ordinal = 1
        ))

    return ret