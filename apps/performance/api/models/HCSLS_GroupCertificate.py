from config import database, helpers, db_context
import base
_hasCreated=False
def HCSLS_GroupCertificate():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "HCSLS_GroupCertificate",
            "base",
            [["group_cer_code"]],
            group_cer_code=helpers.create_field("text", True),
            group_cer_name=helpers.create_field("text", True),
            group_cer_type=helpers.create_field("numeric"),
            group_cer_by=helpers.create_field("text"),
            group_cer_name2=helpers.create_field("text"),
            ordinal=helpers.create_field("numeric"),
            lock=helpers.create_field("bool"),
            note=helpers.create_field("text"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
        )
        _hasCreated=True
    ret = db_context.collection("HCSLS_GroupCertificate")

    return ret