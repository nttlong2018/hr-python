from .. import models
from .. import common
def display_list_position():
    ret=models.HCSLS_Position().aggregate()
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.project(
        _id = "_id",
        job_pos_code="job_pos_code",
        job_pos_name="job_pos_name",
        job_pos_name2="job_pos_name2",
        man_level="man_level",
        ordinal="ordinal",
        note="note",
        is_fix="is_fix",
        coeff="coeff",
        begin_date_cal="begin_date_cal",
        lock="lock",
        details="details",
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')"
    )
    ret.sort(dict(
        ordinal = 1
    ))

    return ret

def display_list_postion_detail(pos_code):
    col=models.HCSLS_Position().aggregate().match("job_pos_code == {0}", pos_code)
    col.unwind("details", False)
    col.join(models.auth_user_info(), "created_by", "username", "uc")
    col.left_join(models.auth_user_info(), "modified_by", "username", "um")
    col.project(
        rec_id = "details.rec_id",
        seniority_from = "details.seniority_from",
        seniority_to = "details.seniority_to",
        coefficient = "details.coefficient",
        salary = "details.salary",
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(details.modified_on!='',details.modified_on),'')",
        modified_by="switch(case(details.modified_by!='',um.login_account),'')"
        )

    return col

def remove_details(args):
    collection  =  common.get_collection('HCSLS_Position')
    ret = collection.update(
                        {
                            "job_pos_code": args['data']['job_pos_code']
                        },
                        {
                            '$pull':{"details" :{ "rec_id": {'$in': args['data']['rec_id']}}}
                        }, 
                        True
                        )
    return ret

def insert_details(args, details):
    collection  =  common.get_collection('HCSLS_Position')
    ret = collection.update(
                          { "job_pos_code": args['data']['job_pos_code'] },
                          {
                            '$push': {
                              "details": details
                            }
                          }
                        )
    return ret

def update_details(args, details):
    collection  =  common.get_collection('HCSLS_Position')
    ret = collection.update(
        {
            "job_pos_code": args['data']['job_pos_code'],
            "details":{
                "$elemMatch":{
                    "rec_id":args['data']['details']["rec_id"]
                    }
                }
        },
        {
            "$set": {
                'details.$.salary': details['salary'],
                'details.$.coefficient': details['coefficient'],
                'details.$.seniority_from': details['seniority_from'],
                'details.$.seniority_to': details['seniority_to'],
                'details.$.modified_by': details['modified_by'],
                'details.$.modified_on': details['modified_on']
                }
        })
    return ret