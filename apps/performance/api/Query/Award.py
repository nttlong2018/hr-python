from .. import models

def get_award():
    ret=models.SYS_ValueList().aggregate()
    ret=models.SYS_ValueList().aggregate().match("list_name == {0}", "LAwardType")
    ret.unwind("values")
    ret.join(models.HCSLS_Award(),"values.value","award_type","aw")
    ret.left_join(models.HCSLS_AwardLevel(), "aw.award_level_code", "award_level_code", "awl")
    ret.left_join(models.auth_user_info(), "aw.created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "aw.modified_by", "username", "um")
    ret.project(
        _id = "aw._id",
        award_code="aw.award_code",
        award_name="aw.award_name",
        award_name2="aw.award_name2",
        award_level_code="aw.award_level_code",
        award_place_code="aw.award_place_code",
        award_type="aw.award_type",
        is_team="aw.is_team",
        ordinal="aw.ordinal",
        note="aw.note",
        lock="aw.lock",
        display_award_level_code="awl.award_level_name",
        display_award_type="switch(case(values.custom!='',values.custom),values.caption)",
        created_by="uc.login_account",
        created_on="aw.created_on",
        modified_on="switch(case(aw.modified_on!='',aw.modified_on),'')",
        modified_by="switch(case(aw.modified_by!='',um.login_account),'')",
        )
    ret.sort(dict(
        ordinal = 1
        ))

    return ret

def get_award_level():
    ret=models.HCSLS_AwardLevel().aggregate()
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.project(
        _id = "_id",
        award_level_code="award_level_code",
        award_level_name="award_level_name",
        award_level_name2="award_level_name2",
        max_times_per_year="max_times_per_year",
        ordinal="ordinal",
        note="note",
        lock="lock",
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
        )
    ret.sort(dict(
        ordinal = 1
        ))

    return ret

def get_award_place():
    ret=models.HCSLS_AwardPlace().aggregate()
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.project(
        _id = "_id",
        award_place_code="award_place_code",
        award_place_name="award_place_name",
        award_place_name2="award_place_name2",
        ordinal="ordinal",
        note="note",
        lock="lock",
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
        )
    ret.sort(dict(
        ordinal = 1
        ))

    return ret