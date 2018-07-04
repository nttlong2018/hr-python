from .. import models
def display_list_nation():
    ret=models.HCSLS_Nation().aggregate()
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.project(
        _id = "_id",
        nation_code="nation_code",
        nation_name="nation_name",
        nation_name2="nation_name2",
        org_nation_code="org_nation_code",
        continents="continents",
        note="note",
        ordinal="ordinal",
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
        lock="lock"
        )
    ret.sort(dict(
        ordinal = 1
        ))

    return ret