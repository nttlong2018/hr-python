from config import database, helpers, db_context
import base
_hasCreated=False
def HCSLS_TrainTypeDetail():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "HCSLS_TrainTypeDetail",
            "base",
            [["train_detail_code"]],
            train_detail_code=helpers.create_field("text", True),
            train_detail_name=helpers.create_field("text", True),
            train_detail_name2=helpers.create_field("text"),
            ordinal=helpers.create_field("numeric"),
            note=helpers.create_field("text"),
            lock=helpers.create_field("bool"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
            #department_code=helpers.create_field("text")
        )
        _hasCreated=True
    ret = db_context.collection("HCSLS_TrainTypeDetail")

    return ret