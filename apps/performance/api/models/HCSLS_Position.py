from config import database, helpers, db_context
import datetime
import base
import threading
_hasCreated=False
def HCSLS_Position():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "HCSLS_Position",
            "base",
            [["job_pos_code"]],
            job_pos_code=helpers.create_field("text",True),
            job_pos_name=helpers.create_field("text", True),
            job_pos_name2=helpers.create_field("text"),
            man_level=helpers.create_field("numeric", True),
            ordinal=helpers.create_field("numeric"),
            note=helpers.create_field("text"),
            is_fix=helpers.create_field("numeric"),
            coeff=helpers.create_field("numeric"),
            begin_date_cal=helpers.create_field("numeric"),
            lock=helpers.create_field("bool"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text"),
            details=helpers.create_field("list",False,dict(
                rec_id = helpers.create_field("text"),
                seniority_from = helpers.create_field("numeric"),
                seniority_to = helpers.create_field("numeric"),
                coefficient = helpers.create_field("numeric"),
                salary = helpers.create_field("numeric"),
                created_on=helpers.create_field("date"),
                created_by=helpers.create_field("text"),
                modified_on=helpers.create_field("date"),
                modified_by=helpers.create_field("text")
            ))
        )
        _hasCreated=True
        #def on_before_insert(data):
        #    before_process

        #def on_before_update(data):
        #    before_process(data)

        #def before_process(data):
        #    data.update({
        #        "detail": [{
        #                "department_code":x['_id'],
        #                } for x in data.get('detail',[])]
        #        })

        #helpers.events("HCSLS_Acadame").on_before_insert(on_before_insert).on_before_update(on_before_update)
    ret = db_context.collection("HCSLS_Position")

    return ret