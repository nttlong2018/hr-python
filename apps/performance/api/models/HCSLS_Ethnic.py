from config import database, helpers, db_context
import base
_hasCreated=False
def HCSLS_Ethnic():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "HCSLS_Ethnic",
            "base",
            [["ethnic_code"]],
            ethnic_code=helpers.create_field("text", True),
            ethnic_name=helpers.create_field("text", True),
            range=helpers.create_field("numeric"),
            ordinal=helpers.create_field("numeric"),
            note=helpers.create_field("text"),
            lock=helpers.create_field("bool"),
            ethnic_name2=helpers.create_field("text"),
            is_ethnic_minority=helpers.create_field("bool"),
            created_on=helpers.create_field("text"),
            created_by=helpers.create_field("date"),
            modified_on=helpers.create_field("text"),
            modified_by=helpers.create_field("date")
        )
        _hasCreated=True
    ret = db_context.collection("HCSLS_Ethnic")

    return ret