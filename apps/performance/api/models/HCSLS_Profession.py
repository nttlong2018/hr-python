from config import database, helpers, db_context
import base
_hasCreated=False
def HCSLS_Profession():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "HCSLS_Profession",
            "base",
            [["profession_code"]],
            profession_code=helpers.create_field("text", True),
            profession_name=helpers.create_field("text", True),
            note=helpers.create_field("text"),
            ordinal=helpers.create_field("numeric"),
            lock=helpers.create_field("bool"),
            profession_name2=helpers.create_field("text"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
        )
        _hasCreated=True
    ret = db_context.collection("HCSLS_Profession")

    return ret