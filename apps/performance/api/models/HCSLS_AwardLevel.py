# -*- coding: utf-8 -*-
from config import database, helpers, db_context
import datetime
import base
import threading
_hasCreated=False
def HCSLS_AwardLevel():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "HCSLS_AwardLevel",
            "base",
            [["award_level_code"]],
            award_level_code = helpers.create_field("text", True),
            award_level_name = helpers.create_field("text", True),
            award_level_name2 = helpers.create_field("text"),
            ordinal = helpers.create_field("numeric"),
            note = helpers.create_field("text"),
            lock=helpers.create_field("bool"),
            max_times_per_year=helpers.create_field("numeric"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
        )
        _hasCreated=True

    ret = db_context.collection("HCSLS_AwardLevel")

    return ret