from config import database, helpers, db_context
import base
_hasCreated=False
def HCSLS_Religion():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "HCSLS_Religion",
            "base",
            [["religion_code"]],
            religion_code=helpers.create_field("text", True),
            religion_name=helpers.create_field("text", True),
            ordinal=helpers.create_field("numeric"),
            note=helpers.create_field("text"),
            lock=helpers.create_field("bool"),
            religion_name2=helpers.create_field("text"),
            created_on=helpers.create_field("text"),
            created_by=helpers.create_field("date"),
            modified_on=helpers.create_field("text"),
            modified_by=helpers.create_field("date")
        )
        _hasCreated=True
    ret = db_context.collection("HCSLS_Religion")

    return ret