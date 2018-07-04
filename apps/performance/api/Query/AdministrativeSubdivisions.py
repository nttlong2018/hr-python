from .. import models
from .. import common

def get_province():
    ret=models.HCSLS_Province().aggregate()
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.project(
        _id = "_id",
        province_code="province_code",
        province_name="province_name",
        province_name2="province_name2",
        type_code="type_code",
        region_code="region_code",
        nation_code="nation_code",
        ordinal="ordinal",
        note="note",
        lock="lock",
        org_province_code="org_province_code",
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
        )
    ret.sort(dict(
        ordinal = 1
        ))

    return ret

    return list(ret)

def get_district():
    ret=models.HCSLS_District().aggregate()
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.project(
        _id = "_id",
        district_code="district_code",
        province_code="province_code",
        district_name="district_name",
        district_name2="district_name2",
        type_code="type_code",
        ordinal="ordinal",
        note="note",
        lock="lock",
        org_district_code="org_district_code",
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
        )
    ret.sort(dict(
        ordinal = 1
        ))

    return ret

def get_ward():
    ret=models.HCSLS_Ward().aggregate()
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.project(
        _id = "_id",
        ward_code="ward_code",
        district_code="district_code",
        ward_name="ward_name",
        ward_name2="ward_name2",
        type_code="type_code",
        ordinal="ordinal",
        note="note",
        lock="lock",
        org_ward_code="org_ward_code",
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
        )
    ret.sort(dict(
        ordinal = 1
        ))

    return ret

def get_hamlet():
    ret=models.HCSLS_Hamlet().aggregate()
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.project(
        _id = "_id",
        hamlet_code="hamlet_code",
        ward_code="ward_code",
        hamlet_name="hamlet_name",
        hamlet_name2="hamlet_name2",
        type_code="type_code",
        ordinal="ordinal",
        note="note",
        lock="lock",
        org_hamlet_code="org_hamlet_code",
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
        )
    ret.sort(dict(
        ordinal = 1
        ))

    return ret