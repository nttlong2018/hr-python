from .. import models
def display_list_cer():
    ret=models.HCSLS_Certificate().aggregate()
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.project(
        _id = "_id",
        cer_code="cer_code",
        cer_name="cer_name",
        cer_name2="cer_name2",
        expired_time="expired_time",
        group_cer_code="group_cer_code",
        cers_time_limit="cers_time_limit",
        scer_code="scer_code",
        cers_replace_code="cers_replace_code",
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