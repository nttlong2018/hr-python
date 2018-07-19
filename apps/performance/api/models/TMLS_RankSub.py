# -*- coding: utf-8 -*-
from config import database, helpers, db_context
import datetime
import base
import threading
_hasCreated=False
def TMLS_RankSub():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "TMLS_RankSub",
            "base",
            [["rank_code"]],
            rec_id = helpers.create_field('text'),
            rank_code = helpers.create_field('text'),
            change_object = helpers.create_field('numeric'),
            object_level = helpers.create_field('numeric'),
            object_code = helpers.create_field('text'),
            object_name = helpers.create_field('text'),
            priority_no = helpers.create_field('numeric'),
            total_from = helpers.create_field('numeric'),
            total_to = helpers.create_field('numeric'),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
        )
        _hasCreated=True

    ret = db_context.collection("TMLS_RankSub")

    return ret