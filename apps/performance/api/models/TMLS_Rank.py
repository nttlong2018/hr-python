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
            rank_code = helpers.create_field('text', True),
            rank_name = helpers.create_field('text', True),
            rank_content = helpers.create_field('text'),
            total_from = helpers.create_field('numeric'),
            total_to = helpers.create_field('numeric'),
            is_change_object = helpers.create_field('bool'),
            ordinal = helpers.create_field('numeric'),
            lock = helpers.create_field('bool'),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text"),
            #TMLS_RankSub
            details=helpers.create_field("list",False,dict(
                rec_id = helpers.create_field('text', True),
                rank_code = helpers.create_field('text', True),
                change_object = helpers.create_field('numeric', True),
                object_level = helpers.create_field('numeric'),
                object_code = helpers.create_field('text', True),
                object_name = helpers.create_field('text'),
                priority_no = helpers.create_field('numeric'),
                total_from = helpers.create_field('numeric'),
                total_to = helpers.create_field('numeric'),
                created_on=helpers.create_field("date"),
                created_by=helpers.create_field("text"),
                modified_on=helpers.create_field("date"),
                modified_by=helpers.create_field("text")
            ))
        )
        _hasCreated=True

    ret = db_context.collection("TMLS_Rank")

    return ret