from config import database, helpers, db_context
import base
_hasCreated=False
def HCSLS_Discipline():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "HCSLS_Discipline",
            "base",
            [["disc_code"]],
            disc_code=helpers.create_field("text", True),
            disc_name=helpers.create_field("text", True),
            is_due_salary=helpers.create_field("bool"),
            ordinal=helpers.create_field("numeric"),
            note=helpers.create_field("text"),
            lock=helpers.create_field("bool"),
            disc_name2=helpers.create_field("text"),
            created_on=helpers.create_field("text"),
            created_by=helpers.create_field("date"),
            modified_on=helpers.create_field("text"),
            modified_by=helpers.create_field("date")
        )
        _hasCreated=True
    ret = db_context.collection("HCSLS_Discipline")

    return ret