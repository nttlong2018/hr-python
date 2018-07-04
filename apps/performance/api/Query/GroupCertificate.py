from .. import models
def display_list_group_cer():
    ret=models.HCSLS_GroupCertificate().aggregate()
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.project(
        _id = "_id",
        group_cer_code="group_cer_code",
        group_cer_name="group_cer_name",
        group_cer_name2="group_cer_name2",
        group_cer_type="group_cer_type",
        group_cer_by="group_cer_by",
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