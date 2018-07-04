from config import database, helpers, db_context
import base
_hasCreated=False
def HCSLS_Marital():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "HCSLS_Marital",
            "base",
            [["marital_code"]],
            marital_code=helpers.create_field("text", True),
            marital_name=helpers.create_field("text", True),
            ordinal=helpers.create_field("numeric"),
            note=helpers.create_field("text"),
            lock=helpers.create_field("bool"),
            marital_name2=helpers.create_field("text"),
            created_on=helpers.create_field("text"),
            created_by=helpers.create_field("date"),
            modified_on=helpers.create_field("text"),
            modified_by=helpers.create_field("date")
        )
        _hasCreated=True
    ret = db_context.collection("HCSLS_Marital")

    return ret