# -*- coding: utf-8 -*-
from config import database, helpers, db_context
import datetime
import base
import threading
_hasCreated=False
def HCSLS_Acadame():
    global _hasCreated
    if not _hasCreated:
        
        """
        #is_fix: Hệ số cố định
        #coeff: #Thiết lập theo
        #coeff: #Ngày bắt đầu tính thâm niên
        """
        helpers.extent_model(
            "HCSLS_Acadame",
            "base",
            [["train_level_code"]],
            train_level_code=helpers.create_field("text",True),
            train_level_name=helpers.create_field("text"),
            range=helpers.create_field("numeric"),
            ordinal=helpers.create_field("numeric"),
            note=helpers.create_field("text"),
            #train_cof=helpers.create_field("numeric"),
            is_fix=helpers.create_field("numeric"), 
            coeff=helpers.create_field("numeric"), 
            begin_date_cal=helpers.create_field("numeric"),
            lock=helpers.create_field("bool"),
            train_level_name2=helpers.create_field("text"),
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
    ret = db_context.collection("HCSLS_Acadame")

    return ret