# -*- coding: utf-8 -*-
from config import database, helpers, db_context
import datetime
import base
import threading
_hasCreated=False
def TMLS_Rank():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "TMLS_Rank",
            "base",
            [["rank_code"]],
            rec_id = helpers.create_field('text'),
            valuelist_key = helpers.create_field('numeric'),
            change_object = helpers.create_field('numeric'),
            change_object_name = helpers.create_field('text'),
            priority_no = helpers.create_field('text'),
            note = helpers.create_field('numeric'),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
        )
        _hasCreated=True

    ret = db_context.collection("TMLS_Rank")

    return ret
rec_id   int x
valuelist_key    string  x
change_object    int x
change_object_name    string  
priority_no  int x
note    string  
