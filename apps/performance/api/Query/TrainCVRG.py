from .. import models
def display_list_train_cvrg():
    ret=models.HCSLS_TrainCVRG().aggregate()
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.project(
        _id = "_id",
        train_cvrg_code="train_cvrg_code",
        train_cvrg_name="train_cvrg_name",
        train_cvrg_name2="train_cvrg_name2",
        #is_lang="is_lang",
        #is_bhld="is_bhld",
        domain_code="domain_code",
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