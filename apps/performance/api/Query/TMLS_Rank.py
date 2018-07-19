from .. import models
def display_list_rank():
    ret=models.TMLS_Rank().aggregate()
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.project(
        _id = "_id",
        rank_code="rank_code",
        rank_name="rank_name",
        rank_content="rank_content",
        total_from="total_from",
        total_to="total_to",
        is_change_object="is_change_object",
        ordinal="ordinal",
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

def get_details(args):
    pass

def insert_details(args):
    pass

def remove_details(args):
    pass