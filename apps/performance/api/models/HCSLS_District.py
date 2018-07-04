from config import database, helpers, db_context
import datetime
import base
import threading
_hasCreated=False
def HCSLS_District():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "HCSLS_District",
            "base",
            [["district_code"], ['province_code']],
            district_code = helpers.create_field("text", True),
            province_code = helpers.create_field("text", True),
            district_name = helpers.create_field("text", True),
            district_name2 = helpers.create_field("text"),
            type_code = helpers.create_field("text"),
            ordinal=helpers.create_field("numeric"),
            note=helpers.create_field("text"),
            lock=helpers.create_field("bool"),
            org_district_code=helpers.create_field("text"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
        )
        _hasCreated=True

    ret = db_context.collection("HCSLS_District")

    return ret