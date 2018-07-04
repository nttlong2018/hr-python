from config import database, helpers, db_context
import base
_hasCreated=False
def HCSLS_QuitJob():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "HCSLS_QuitJob",
            "base",
            [["quit_job_code"]],
            quit_job_code=helpers.create_field("text", True),
            quit_job_name=helpers.create_field("text", True),
            quit_type=helpers.create_field("numeric"),
            ordinal=helpers.create_field("numeric"),
            note=helpers.create_field("text"),
            lock=helpers.create_field("bool"),
            quit_job_name2=helpers.create_field("text"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
        )
        _hasCreated=True
    ret = db_context.collection("HCSLS_QuitJob")

    return ret