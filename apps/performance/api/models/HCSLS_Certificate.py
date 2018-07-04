from config import database, helpers, db_context
import base
_hasCreated=False
def HCSLS_Certificate():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "HCSLS_Certificate",
            "base",
            [["cer_code"]],
            cer_code=helpers.create_field("text", True),
            cer_name=helpers.create_field("text", True),
            cer_name2=helpers.create_field("text"),
            expired_time=helpers.create_field("numeric"),
            group_cer_code=helpers.create_field("text"),
            cers_time_limit=helpers.create_field("numeric"),
            scer_code=helpers.create_field("text"),
            cers_replace_code=helpers.create_field("text"),
            ordinal=helpers.create_field("numeric"),
            note=helpers.create_field("text"),
            lock=helpers.create_field("bool"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
        )
        _hasCreated=True
    ret = db_context.collection("HCSLS_Certificate")

    return ret